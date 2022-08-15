MIT License

Copyright (c) 2019-2022 Manuel Bottini

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

This document describes the protocol to establish properly a communication within the Bodynodes Network.
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

There can be 2 actors in the communication:
	- Node: which gathers movement information from its own sensor and send it to the Host
	- Host: which listens for Nodes and makes data available to the Main Application

This document assumes that Node and Host are all connected on the same Wifi. Using the UDP Multicast protocol
it is possible for the Host to signal to the whole subnetwork that it is a Bodynode Host and Nodes can connect
to it.

The port used by both Host and Node is 12345.
The multicast port used by both Host and Node is 12346.
The UDP multicast group used by both Host and Node is 239.192.1.99.
Ports and IP addresses have been chosen randomly.

The following is the communication flow:
  1 - The Host keep sending a multicast UDP packets with the message “BN” (default) every 5 seconds to all the
      devices on the network
  2 - The Node waits for a "BN" message on the multicast group
  3 - The Node receives the "BN" message and sends the "ACKN" UDP message to the Host and waits
  4 - The Host receives the "ACKN" message and sends back a "ACKH" UDP message to the Node and starts listening
  5 - The Node receives the "ACKH" and starts sending movement information
  6 - The Host receives movement information and uses them

Actions are sent via UDP:
  - from Host to Nodes

When the Host send an action, it expects an "ACKN" in return to indicate that the actions has been properly
received. The Host will keep sending the last action until an "ACKN" from the Node is received.

The Node after receiving an action is expected to "do it" and send back an "ACKN". This is important to make
sure actions are confirmed (since UDP is an unreliable protocol).

A final note is about how to keep a connection. The UDP protocol does not check if the other end got terminated
and does not receive/send anymore. It is up to the Node to send a small sequence of ACKN every 30 seconds.
If the Node does not receive an "ACKH" for more than 1 minute, it will consider ifself as disconnected and will
stop sending data. The Host will consider the Node as disconnected if it does not receive data or any "ACKN"
from the Node for more than 1 minute.
