import socket
import threading
import time
import struct
import hashlib

HEADER_FORMAT = '!I32s?'
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
TIMEOUT = 1.0
WINDOW_SIZE = 5

class Packet:
    def __init__(self, seq_num, data, ack=False):
        self.seq_num = seq_num
        self.data = data
        self.ack = ack
        self.checksum = self.calculate_checksum()

    def calculate_checksum(self):
        m = hashlib.sha256()
        m.update(struct.pack('!I?', self.seq_num, self.ack))
        m.update(self.data)
        return m.digest()

    def to_bytes(self):
        header = struct.pack(HEADER_FORMAT, self.seq_num, self.checksum, self.ack)
        return header + self.data

    @staticmethod
    def from_bytes(bytes_data):
        header = bytes_data[:HEADER_SIZE]
        data = bytes_data[HEADER_SIZE:]
        seq_num, checksum, ack = struct.unpack(HEADER_FORMAT, header)
        pkt = Packet(seq_num, data, ack)
        pkt.checksum = checksum
        return pkt

    def is_valid(self):
        return self.checksum == self.calculate_checksum()

class RDT_Sender:
    def __init__(self, local_addr, remote_addr):
        self.remote_addr = remote_addr
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(local_addr)
        self.socket.settimeout(0.5)
        self.socket.connect(self.remote_addr)

        self.lock = threading.Lock()
        self.base = 0
        self.next_seq_num = 0
        self.window = {}
        self.timer = None

    def send(self, data):
        chunk_size = 1024
        chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
        total_chunks = len(chunks)
        self.base = 0
        self.next_seq_num = 0

        recv_thread = threading.Thread(target=self._recv_ack_thread, args=(total_chunks,))
        recv_thread.start()

        while self.base < total_chunks:
            with self.lock:
                while self.next_seq_num < self.base + WINDOW_SIZE and self.next_seq_num < total_chunks:
                    pkt = Packet(self.next_seq_num, chunks[self.next_seq_num])
                    self.window[self.next_seq_num] = pkt
                    self.socket.send(pkt.to_bytes())
                    print(f"Sent packet {self.next_seq_num}")
                    if self.base == self.next_seq_num:
                        self._start_timer()
                    self.next_seq_num += 1
            time.sleep(0.1)

        recv_thread.join()

    def _start_timer(self):
        if self.timer:
            self.timer.cancel()
        self.timer = threading.Timer(TIMEOUT, self._timeout_handler)
        self.timer.start()

    def _timeout_handler(self):
        with self.lock:
            print("Timeout occurred, retransmitting window")
            for seq in range(self.base, self.next_seq_num):
                if seq in self.window:
                    self.socket.send(self.window[seq].to_bytes())
            self._start_timer()

    def _recv_ack_thread(self, total_chunks):
        while self.base < total_chunks:
            try:
                data = self.socket.recv(4096)
                pkt = Packet.from_bytes(data)
                if pkt.ack and pkt.is_valid():
                    with self.lock:
                        print(f"Received ACK for packet {pkt.seq_num}")
                        if pkt.seq_num >= self.base:
                            self.base = pkt.seq_num + 1
                            if self.base < self.next_seq_num:
                                self._start_timer()
                            else:
                                self.timer.cancel()
            except socket.timeout:
                continue
            except Exception as e:
                print("Error receiving ACK:", e)

    def close(self):
        if self.timer:
            self.timer.cancel()
        self.socket.close()

class RDT_Receiver:
    def __init__(self, local_addr):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(local_addr)
        self.socket.settimeout(0.5)
        self.expected_seq = 0
        self.received_data = {}
        self.running = True

    def listen(self):
        while self.running:
            try:
                data, addr = self.socket.recvfrom(4096)
                pkt = Packet.from_bytes(data)
                if not pkt.is_valid():
                    print("Received corrupted packet, discarding.")
                    continue

                if pkt.seq_num == self.expected_seq and not pkt.ack:
                    print(f"Received expected packet {pkt.seq_num}")
                    self.received_data[pkt.seq_num] = pkt.data
                    self._send_ack(pkt.seq_num, addr)
                    self.expected_seq += 1
                else:
                    print(f"Received out-of-order packet {pkt.seq_num} (expected {self.expected_seq}).")
                    self._send_ack(self.expected_seq - 1, addr)
            except socket.timeout:
                continue
            except OSError:
                if not self.running:
                    break
                raise

    def _send_ack(self, seq_num, addr):
        ack_pkt = Packet(seq_num, b'', ack=True)
        self.socket.sendto(ack_pkt.to_bytes(), addr)
        print(f"Sent ACK for packet {seq_num}")

    def get_data(self):
        data = b''.join(self.received_data[i] for i in sorted(self.received_data.keys()))
        return data

    def close(self):
        self.running = False
        self.socket.close()
