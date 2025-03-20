Reliable Data Transfer (RDT) Protocol Implementation
====================================================

This project implements a basic reliable data transfer (RDT) protocol over UDP, simulating realistic network conditions such as packet loss, corruption, and delays.

Project Structure
--------------------

```
.
├── client.py
├── server.py
├── simulator.py
└── rdt.py
```

-   **client.py**: Reads and sends files to the server using RDT protocol.

-   **server.py**: Receives files and saves them to disk using RDT protocol.

-   **simulator.py**: Simulates network conditions (packet loss, corruption, delays).

-   **rdt.py**: Core RDT sender and receiver logic.

Requirements
----------------

-   Python 3.7+

How to Run (All Operating Systems)
-------------------------------------

Open three terminal or command prompt windows.

### 1\. Start the Network Simulator

```
python simulator.py
```

### 2\. Start the Server

```
python server.py <save_filename> <server_port>
```

**Example:**

```
python server.py received_file.txt 9001
```

### 3\. Start the Client

```
python client.py <file_to_send> <client_port> <simulator_port>
```

**Example:**

```
python client.py file_to_send.txt 8000 9000
```

* * * * *

Example Command-line Usage
------------------------------

**Terminal 1 (Simulator):**

```
python simulator.py
```

**Terminal 2 (Server):**

```
python server.py received_file.txt 9001
```

**Terminal 3 (Client):**

```
python client.py example.txt 8000 9000
```

This setup will:

-   Run the simulator on port **9000**

-   Have the client send data from port **8000** to the simulator on **port 9000**

-   Have the simulator forward the packets to the server on **port 9001** and ACKs back to the client
 
Verifying the Transfer
------------------------

After completion, verify that:

-   The server outputs the file: `received_file.txt`

-   The file content matches the original file sent from the client.

Notes
--------

-   Ensure no firewall or other software blocks UDP ports used (`8000`, `9000`, `9001`).

-   The simulator introduces random network conditions. Adjust parameters in `simulator.py` as needed.

 Customizing Simulator Behavior
---------------------------------

You can adjust the following parameters directly in `simulator.py`:

-   **loss_rate**: Fraction of packets randomly dropped.

-   **corruption_rate**: Fraction of packets randomly corrupted.

-   **delay_rate**: Fraction of packets randomly delayed.

**Example:**

```
simulator = NetworkSimulator(
    client_listen=('localhost', 9000),
    server_addr=('localhost', 9001),
    loss_rate=0.1,
    corruption_rate=0.1,
    delay_rate=0.1
)
```

Compatibility
----------------

Compatible with Windows, Linux, and macOS. Just ensure Python 3.7+ is installed and available on your system path.

* * * * *

Troubleshooting
------------------

-   **Address already in use:** Ensure ports are not already occupied by another process.

-   **Timeout issues:** Ensure the simulator ports match client and server expectations, as described above.