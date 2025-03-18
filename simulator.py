import socket
import threading
import random

class NetworkSimulator:
    def __init__(self, client_listen, server_addr, loss_rate=0.1, corruption_rate=0.1, delay_rate=0.1):
        self.client_listen = client_listen  # port 9000 (client sends here)
        self.server_addr = server_addr      # port 9001 (server listens here)
        self.loss_rate = loss_rate
        self.corruption_rate = corruption_rate
        self.delay_rate = delay_rate

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.client_listen)

    def start(self):
        print(f"Simulator running on {self.client_listen}, forwarding to {self.server_addr}")
        while True:
            data, addr = self.socket.recvfrom(4096)

            if addr[1] == 8000:
                direction = "Client → Server"
                forward_addr = self.server_addr
            else:
                direction = "Server → Client"
                forward_addr = ('localhost', 8000)

            if random.random() < self.loss_rate:
                print(f"[{direction}] Dropped packet.")
                continue

            if random.random() < self.corruption_rate:
                print(f"[{direction}] Corrupted packet.")
                data = bytearray(data)
                data[random.randint(0, len(data)-1)] ^= 0xFF
                data = bytes(data)

            if random.random() < self.delay_rate:
                delay = random.uniform(0.5, 2.0)
                print(f"[{direction}] Delayed packet by {delay:.2f}s.")
                threading.Timer(delay, self.socket.sendto, args=(data, forward_addr)).start()
            else:
                self.socket.sendto(data, forward_addr)

if __name__ == '__main__':
    simulator = NetworkSimulator(
        client_listen=('localhost', 9000),  # listens from both client & server
        server_addr=('localhost', 9001),
        loss_rate=0.1, corruption_rate=0.1, delay_rate=0.1
    )
    simulator.start()
