MIT License

Copyright (c) 2019-2021 Manuel Bottini

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

This document describes the protocol to enstablish properly a communication within the Bodynodes Network.
Please open an Issue in case the document is ambiguous or missing information.

---------------------------------------------------------
Wifi Communication
---------------------------------------------------------

This section describes the protocol used to connect with Wifi Nodes
As of now only the following are the types of nodes considered:
	- WifiNodes

The messages are sent using UDP which is a protocol that does provide performace in exchange of reliability.
Therefore the packets are sent but there is not insurance that all will reach the server.

As of now no encryption is considered for the data.

There can be 3 actors in the communication:
	- Node: which gathers movement information from its own sensor and send it to the Host
	- Host: which listens for Nodes and makes data available to the Main Application

This document assumes that Node and Host are already connected on the same Wifi and they know each other IP Address and Port.

The port used by Host is 12345.
The port used by Node is 12345.

The following is the communication flow:
  1 - The Host keep sending a multicast UDP packets with the message “ACKH” every 5 seconds to all the devices on the network
  2 - The Node waits for an ACKH message
  3 - The Node receives the ACKH message and sends the ACKN UDP message to the Host
  4 - Afterwards the Node starts sending movement information
  5 - The Host receives movement information and uses them

Actions are sent via UDP:
  - from Host to Nodes

When an action is sent, the sender expects an ACKN in return to indicate that the actions has been properly received.
The sender will keep sending the last action it has to send till the ACKN is received. The main reason is that Node
have way less computational power and they tend to lose incoming packets more easily.

The receiver when receives an action, is expected to act on it and send back an ACKN.

This process is important to make sure actions are confirmed since UDP is an unreliable protocol.

A final note is about how to keep a connection. The UDP protocol does not check if the other end got terminated and does not receive/send anymore.
It is up to the Node to send a small sequence of ACKN every 30 seconds. The Host will keep sending ACKH every 5 seconds.
If the Node does not receive an ACKH for more than 1 minute, it will consider ifself as disconnected and will stop sending data.
The Host will consider the Node as disconnected if it does not receive data or any ACKN from the Node for more than 1 minute.
