
MIT License

Copyright (c) 2019-2025 Manuel Bottini

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

------------------------------------------------

EnstablishAConnection Development Specification Version 1.0

This document describes the protocol for establishing communication within the Bodynodes Network.
Please open an Issue if the document is ambiguous or missing information.

---------------------------------------------------------
Wifi Communication
---------------------------------------------------------

This section describes the protocol used for communication via WiFi. Currently, only the following
type of node is considered:
	- WiFi Bodynode ( also called WiFi Nodes )

Messages are sent using UDP, which provides performance at the expense of reliability. Therefore,
packets are sent without a guarantee that all will reach the server.

Encryption is not considered for the data at this time.

There are two actors in the communication:
- Node: Gathers movement information from its internal sensor and sends it to the Host.
- Host: Listens for Nodes and makes data available to the Main Application.

This document assumes that both Node and Host are connected to the same WiFi network. Using the UDP
multicast protocol, the Host can signal the entire subnet that it is a Bodynode Host, allowing Nodes
to connect to it.

The port used by both Host and Node is 12345.
The multicast port used by both Host and Node is 12346.
The UDP multicast group used by both Host and Node is 239.192.1.99.
Ports and IP addresses have been chosen randomly.

The communication flow is as follows:
- The Host continuously sends multicast UDP packets with the message "BN" (default) every 5 seconds
  to all devices on the network.
- The Node listens for the "BN" message on the multicast group.
- Upon receiving the "BN" message, the Node sends an "ACKN" UDP message to the Host and waits.
- The Host receives the "ACKN" message and responds with an "ACKH" UDP message to the Node, then
  starts listening.
- The Node receives the "ACKH" and begins sending movement information.
- The Host receives the movement information and processes it.

Actions are sent via UDP from the Host to the Nodes:
- When the Host sends an action, it expects an "ACKN" in return to confirm that the action has been
  properly received. The Host will continue sending the last action until an "ACKN" is received from
  the Node.
- After receiving an action, the Node is expected to execute it and send back an "ACKN" to confirm
  the action.

To maintain the connection, the Node sends a small sequence of "ACKN" every 30 seconds. If the Node does
not receive an "ACKH" for more than 1 minute, it considers itself disconnected and will stop sending data.
Similarly, the Host considers the Node disconnected if it does not receive data or any "ACKN" from the
Node for more than 1 minute.

---------------------------------------------------------
Bluetooth Communication
---------------------------------------------------------

This section describes the protocol used for communication via Bluetooth.
Currently, only the following type of node is considered:
- Bluetooth Bodynode (also called Bluetooth Nodes)

Messages are sent via the serial port created over the Bluetooth communication channel.

Encryption is not considered for the data at this time.

There are two actors in the communication:
- Node: Gathers movement information from its internal sensor and sends it to the Host.
- Host: Listens for Nodes and makes data available to the Main Application.

This document assumes that the Nodes and Host have been paired, and that the Host knows the Bluetooth
addresses of the Nodes it wants to connect to. It also assumes that the Host and Nodes are within range
for Bluetooth communication.

The Node should advertise itself as "Bodynode" to facilitate identification. Pairing should be done manually
or via an external routine before starting the Bluetooth Bodynode Host. The User or external routine will
then provide the Host with the target Nodes' Bluetooth addresses. The Bluetooth Bodynode Host will only be
responsible for connecting and exchanging information. Not all Bluetooth libraries support all operations on
Bluetooth devices.

The UUID that the Bluetooth Bodynode should register its service to is: 00001101-0000-1000-8000-00805f9b34fb
This UUID is also used by other common Bluetooth boards like the HC-05.

The communication flow is as follows:
- The Node creates the UUID service, starts advertising itself, and listens for incoming Bluetooth connections.
- The Host receives the list of Bluetooth devices to connect to and starts a Bluetooth connection with each of them.
- The Node accepts the incoming Bluetooth connection request, sends an "ACKN" message to the Host, and waits.
- The Host receives the "ACKN" message, responds with an "ACKH" message to the Node, and starts listening.
- The Node receives the "ACKH" and begins sending movement information.
- The Host receives the movement information and processes it.

Actions are sent via the serial port created on the Bluetooth channel:
- When the Host sends an action, it expects an "ACKN" in return to confirm that the action has been properly
  received. The Host will continue sending the last action until an "ACKN" is received from the Node.
- After receiving an action, the Node is expected to execute it and send back an "ACKN" to confirm the action.

To maintain the connection, the Node sends a small sequence of "ACKN" every 30 seconds. If the Node does not
receive an "ACKH" for more than 1 minute, it considers itself disconnected and will stop sending data. Similarly,
the Host considers the Node disconnected if it does not receive data or any "ACKN" from the Node for more than
1 minute.


---------------------------------------------------------
BLE Communication
---------------------------------------------------------

This section describes the protocol used for communication via BLE.
Currently, only the following type of node is considered:
- BLE Bodynode (also called BLE Nodes)

Messages are sent via the BLE communication channel.

Encryption is not considered for the data at this time.

There are two actors in the communication:
- Node: Gathers movement information from its internal sensor and sends it to the Host.
- Host: Listens for Nodes and makes data available to the Main Application.

This document assumes that the Nodes and Host are already connected. It also assumes that the Host and Nodes
are within range for BLE communication.

The Node should advertise itself as "Bodynode" to facilitate identification. The Host will connect immediately
and will check its MAC address to decide if it is a node of interest or not. If it is it will then read
the other fields: "player", "bodypart", "values".

The UUID that the Bluetooth Bodynode should register the Messages Service to is:
0x0000CCA0-0000-1000-8000-00805F9B34FB

The communication flow is as follows:
- The Node creates the UUID service, starts advertising itself, and listens for incoming BLE connections.
- The Host receives the list of free BLE "Bodynodes" devices to connect to and starts a connection with each of them.
- The Node accepts the incoming Bluetooth connection request and let the Host read its characteristics.
- The Host decides if it wants to communicate with the Node depending on the MAC address of the Node
- The Host reads player, bodypart, sensortypes information and subscribe to the values notifications it wants.

Actions are currently NOT defined and expected for BLE bodynodes.
