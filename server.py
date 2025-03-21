import sys
import threading
from rdt import RDT_Receiver

def receive_file(save_filename, local_addr):
    receiver = RDT_Receiver(local_addr)
    recv_thread = threading.Thread(target=receiver.listen)
    recv_thread.start()

    recv_thread.join()  # Wait explicitly for EOF

    receiver.close()

    data = receiver.get_data()
    with open(save_filename, 'wb') as f:
        f.write(data)
    print(f"File saved as {save_filename}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python server.py <save_filename> <local_port>")
        sys.exit(1)
    save_filename = sys.argv[1]
    local_port = int(sys.argv[2])
    local_addr = ('localhost', local_port)
    receive_file(save_filename, local_addr)
