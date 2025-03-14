import socket
import threading
import random
import time
"""
A simple network simulator that can introduce packet loss, corruption, and delay.
"""
class NetworkSimulator:
    def __init__(self, listen_addr, forward_addr, loss_rate=0.1, corruption_rate=0.1, delay_rate=0.1):
        self.listen_addr = listen_addr
        self.forward_addr = forward_addr
        self.loss_rate = loss_rate          # Fraction of packets to drop
        self.corruption_rate = corruption_rate  # Fraction of packets to corrupt
        self.delay_rate = delay_rate        # Fraction of packets to delay
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(listen_addr)

    def start(self):
        print(f"Simulator started on {self.listen_addr}, forwarding to {self.forward_addr}")
        while True:
            data, addr = self.socket.recvfrom(4096)
            # Simulate packet loss
            if random.random() < self.loss_rate:
                print("Simulated packet loss.")
                continue

            # Simulate packet corruption
            if random.random() < self.corruption_rate:
                print("Simulated packet corruption.")
                data = bytearray(data)
                # Flip a random byte
                index = random.randint(0, len(data) - 1)
                data[index] = (data[index] + 1) % 256
                data = bytes(data)

            # Simulate delay (and possible reordering)
            if random.random() < self.delay_rate:
                delay = random.uniform(0.5, 2.0)
                print(f"Simulated delay of {delay:.2f} seconds.")
                threading.Timer(delay, self.forward, args=(data,)).start()
            else:
                self.forward(data)

    def forward(self, data):
        self.socket.sendto(data, self.forward_addr)

if __name__ == '__main__':
    # Example usage:
    # Simulator listens on localhost:9000 and forwards to localhost:9001
    sim = NetworkSimulator(('localhost', 9000), ('localhost', 9001),
                           loss_rate=0.1, corruption_rate=0.1, delay_rate=0.1)
    sim.start()
