import sys
import socket
from rdt import RDT_Sender

def send_file(filename, local_addr, remote_addr):
    with open(filename, 'rb') as f:
        file_data = f.read()
    sender = RDT_Sender(local_addr, remote_addr)
    sender.send(file_data)
    sender.close()
    print("File transfer complete.")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python client.py <filename> <local_port> <remote_port>")
        sys.exit(1)
    filename = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_port = int(sys.argv[3])
    local_addr = ('localhost', local_port)
    remote_addr = ('localhost', remote_port)
    send_file(filename, local_addr, remote_addr)
