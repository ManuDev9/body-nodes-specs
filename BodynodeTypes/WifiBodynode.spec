
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

Wifi Bodynode Development Specification Version 1.0

This document describes the main characteristics of a WiFi Bodynode.
Please open an Issue if the document is ambiguous or missing information.
The BodynodesSensor app has the same specifications indicated in this document.

The WiFi Bodynode collects movement information and sends it via WiFi as a client to the
WiFi Bodynodes Host. It also listens for actions from the server. Both the WiFi Bodynode
and the WiFi Bodynodes Host must be connected to the same WiFi network; otherwise, communication
cannot occur.

Initially, the Bodynode will not know the IP address of the Host. The Host will send broadcasts
to a multicast group. The Bodynode must register itself as a listener in the multicast group.
When the Bodynode receives a message, it will save the Host’s IP address and start using it.
If multiple Hosts are present in the network, the Bodynode will retain the IP address of the
first Host it finds. The Bodynode can be configured to connect to a Host broadcasting a specific
name.
More information can be found in this document:
- https://github.com/ManuDev9/body-nodes-specs/blob/master/EstablishAConnection.spec
  
The WiFi Bodynode has two LEDs: a green LED and a red LED. The green LED indicates the status of
the WiFi and server connection, while the red LED indicates the status of communication with the
sensor.
- Red LED ON: There is a problem communicating with the sensor.
- Red LED BLINKING: The sensor is not calibrated yet.
- Red LED OFF: The sensor is communicating correctly.
- Green LED OFF: The WiFi Bodynode is not connected to the WiFi, or the server is offline.
- Green LED BLINKING: The WiFi Bodynode is trying to connect to the server.
- Green LED ON: The WiFi Bodynode is connected to the WiFi and communicating with the server.

If the sensor becomes temporarily disconnected, the red LED will turn ON. The WiFi Bodynode
will continue to ping the sensor until it becomes available again. As soon as communication
with the sensor is re-established, the red LED will turn OFF.

The sensor’s calibration is always checked before any read, and the red LED status is updated
accordingly. Therefore, if the sensor is not calibrated, the red LED will blink, and no data
will be sent. The movement information the node sends and the supported body parts are defined
in the following document:
    - https://github.com/ManuDev9/body-nodes-specs/blob/master/Messages.spec

The data is read from the sensor every 30 milliseconds.

The read data is then compared with the previously sent data. If the read data exceeds a specific
range of the previous data, it is sent and becomes the new previous data. If it does not exceed
the range, the new data is not sent, and the previous data remains unchanged. For digital values,
any change is sent because the possible values are 0 and 1, so any change is meaningful.

The actions the node can receive are defined in the following document:
    - https://github.com/ManuDev9/body-nodes-specs/blob/master/Actions.spec

Actions are also checked every 30 milliseconds, usually after reading the sensor.

