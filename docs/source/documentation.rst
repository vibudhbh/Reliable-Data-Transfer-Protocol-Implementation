Reliable Data Transfer (RDT) Protocol Documentation
===================================================

Overview
--------
The Reliable Data Transfer (RDT) protocol implementation ensures reliable transmission of data over UDP, providing mechanisms such as sequence numbering, acknowledgment packets, checksums for integrity verification, retransmissions, and a sliding window approach for efficiency.

Requirements
------------
- Python 3.7+
- Standard libraries: socket, threading, struct, hashlib

Usage
-----

client.py
^^^^^^^^^
.. code-block:: sh

   python client.py <file_to_send> <client_port> <simulator_port>

server.py
^^^^^^^^^
.. code-block:: sh

   python server.py <received_filename> <server_port>

simulator.py
^^^^^^^^^^^^
.. code-block:: sh

   python simulator.py

Command-Line Arguments
----------------------

client.py
^^^^^^^^^
.. list-table::
   :header-rows: 1

   * - Argument
     - Description
   * - ``<file_to_send>``
     - File path to the data to be sent to the server.
   * - ``<client_port>``
     - Local UDP port to bind the client socket.
   * - ``<simulator_port>``
     - UDP port where the simulator is listening.

server.py
^^^^^^^^^
.. list-table::
   :header-rows: 1

   * - Argument
     - Description
   * - ``<received_filename>``
     - Name of the file to save received data.
   * - ``<server_port>``
     - Local UDP port where the server listens for incoming packets.

Functionality
-------------

Packet Class
^^^^^^^^^^^^
- **Packet(seq_num, data, ack)**: Represents a packet with a sequence number, data payload, acknowledgment flag, and checksum.
  - **calculate_checksum()**: Generates SHA-256 checksum.
  - **to_bytes()**: Serializes the packet for sending over UDP.
  - **from_bytes(bytes_data)**: Deserializes bytes to reconstruct a packet.
  - **is_valid()**: Verifies packet integrity using checksum.

RDT_Sender Class
^^^^^^^^^^^^^^^^
- **send(data)**: Sends data reliably, managing a sliding window and retransmissions.
- **_start_timer()**: Starts a retransmission timer for packet timeouts.
- **_timeout_handler()**: Handles retransmissions when packets timeout.
- **_recv_ack_thread(total_chunks)**: Dedicated thread receiving ACK packets to advance the sliding window.
- **close()**: Closes socket and cancels retransmission timer.

RDT_Receiver Class
^^^^^^^^^^^^^^^^^^
- **listen()**: Listens continuously for incoming packets, handles acknowledgments, and stores data.
- **_send_ack(seq_num, addr)**: Sends acknowledgment for received packets.
- **get_data()**: Assembles and returns the received data in correct order.
- **close()**: Gracefully terminates the receiver.

NetworkSimulator Class
^^^^^^^^^^^^^^^^^^^^^^
- Simulates packet loss, corruption, and delays to test the robustness of the RDT implementation.
- Configurable parameters: ``loss_rate``, ``corruption_rate``, and ``delay_rate``.

Example Usage
-------------

1. Start the Simulator
^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: sh

   python simulator.py

Runs the simulator with default parameters (packet loss, delay, corruption).

2. Start the Server
^^^^^^^^^^^^^^^^^^^
.. code-block:: sh

   python server.py received_file.txt 9001

Starts the server to listen on port 9001 and save data as ``received_file.txt``.

3. Start the Client
^^^^^^^^^^^^^^^^^^^
.. code-block:: sh

   python client.py file_to_send.txt 8000 9000

Sends ``file_to_send.txt`` from client port 8000 through simulator at port 9000.

Notes
-----
- Ensure UDP ports 8000, 9000, and 9001 are open and not blocked by firewalls.
- Adjust simulator parameters to reflect different network conditions.

License
-------
This implementation is intended for educational and demonstration purposes. Always ensure you have permission for testing network communications.

Author: Vibudh Bhardwaj
Last Updated: 2025-03-18

