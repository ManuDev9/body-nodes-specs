MIT License

Copyright (c) 2019 Manuel Bottini

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
The underlying protocol used is UDP. Let's assume two actors in the communication:
	- Node: which gathers movement information and send it to the server
	- Host: which listens for nodes and uses the data somehow

This document assumes that Node and Host are already connected on the same WiFi and they know each other IP Address and Port.

The port used by Node and Host is 12345.

The Node starts the communication by sending a UDP packet with the message “ACK”  every 1 second.

When Node receives a UDP packet with message “ACK”, it starts sending movement information.

The Host opens the port waiting for UDP packets.

When Host receives a UDP packet with message “ACK”, it sends back a UDP packet with message “ACK” and passively waits for movement information.
