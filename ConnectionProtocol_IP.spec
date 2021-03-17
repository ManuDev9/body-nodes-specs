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

This document describes the protocol used to connect with nodes which uses the IP protocol (Wifi BodyNodes for example)

There are two types of nodes:
	- Secured Nodes
	- Unsecured Nodes
	
Secured nodes use the initial permission request mechanism via HTTPS. Afterwards they normally use the unsecured UDP connection for performance purposes.
The reason of exchanging data via an unsecure channel is that the network itself is defined to be local and not accessible from the outside.
Therefore security is only necessary to check the authenticity of the local network, and no other security measures are considered necessary.

Secured Nodes must always ask permission at the beginning. Permission will be exchanged via:
	- HTTPS
Once they receive the permission, Secured Nodes send the ACK.
Unsecured Nodes won't ask for permission, and they send the ACK directly.

The host has to reply to the ACK with another ACK. From this moment the Secured/Unsecured Node involved in the communication start sending movement data.

Data is exchanged only to permitted nodes via:
	- Unsecure UDP

------------------------------------------------
HTTPS
------------------------------------------------
The port used by the Host server is 443.

The Node starts the communication by sending a POST request at the following url:
/permission
JSON if you have the token:
{
	token : “xxxx”
}

The Host can reply in the following ways:
	- 200: Status OK, the Node has been authorized and can start POST data
	- 401: Unauthorized, the Node has not been authorized and cannot POST data

The Host will accept and forward data coming from authorized Nodes. It will disconnect not authorized Nodes and won’t accept data.

Permitted nodes should be recorded as IP Addresses on the Hotspot. Everytime permission is given the IP Address is registered till it disconnects.

The first permission request will be empty, the Hotspot will respond with a token that can be sent as JSON to the next permission requests to avoid asking the user every time the Node disconnects.

The Node will then use UDP to send data.

------------------------------------------------
Unsecure UDP
------------------------------------------------
The underlying protocol used is UDP. There can be 3 actors in the communication:
	- Node: which gathers movement information from its own sensor and send it to the Host or Super Node
	- Super Node: which gathers movement information from its own sensor and other Nodes and send it to the Host
	- Host: which listens for Nodes and Super Nodes and makes data available to the Main Application

This document assumes that Node and Host are already connected on the same WiFi and they know each other IP Address and Port.

The port used by Host is 12344 (as server) and 12345 (as server). So both ports should be open at the same time.
The port used by Super Node is 12344 (as client) and 12345 (as server).
The port used by Node is 12345 (as client) or 12344 (as client). So only one port should be open. 

Note 1: If you want to connect Node to Host directly you need to set up the Node to use port 12344
Note 2: If you want to connect Node to Host with Super Nodes as intermediate you need to set up the Node to use port 12345
Note 3: You might want to use Super Nodes to lower the number of Nodes/Super Nodes connected to the same Host.
Note 4: Some platforms have a limit on the maximum number of WiFi connections they can have.

The choice of ports ensures a simpler implementation of Nodes, Super Nodes, and Hosts.

The Node starts the communication by sending a UDP packet with the message “ACK”  every 1 second.

When Node receives a UDP packet with message “ACK”, it starts sending movement information.

The Host opens the port waiting for UDP packets.

When Host receives a UDP packet with message “ACK”, it sends back a UDP packet with message “ACK” and passively waits for movement information.

Actions are also sent via UDP:
	- from Host to Nodes and Super Nodes
	- from Super Nodes to Nodes

When an action is sent, the sender expects an ACK in return to indicate that the actions has been properly received.
The sender will keep sending the last action it has to send till the ACK is received.

The receiver when receives an action, is expected to act on it and send back an ACK. 

This process is important to make sure actions are done, since UDP is an unreliable protocol.
