
MIT License

Copyright (c) 2024-2025 Manuel Bottini

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

Bluetooth Bodynode Development Specification Version 1.0

This document describes the main characteristics of a generic Bluetooth Bodynode.
Please open an Issue if the document is ambiguous or missing information.
The BodynodesSensor app has the same specifications indicated in this document.

A Bluetooth Bodynode is a Bluetooth node that collects movement information and sends it as
a Peripheral device to a Central device (host application). It also listens for actions from
the Central device. Note that this is a 1-to-1 connection; the Bluetooth node can connect to
only one Central device at a time.

The Central device (Bodynode Host with Bluetooth capabilities) will be responsible for
initiating the connection to the Bluetooth Bodynode. To simplify this process, which is not
straightforward with Classic Bluetooth, it is recommended to scan, identify the Bluetooth
address, and pair with your Bluetooth Bodynode peripheral devices. The Bluetooth Bodynode
should support a simple pairing procedure, which can also be made automatic. When the Bluetooth
Bodynode starts up, it should initially set up to listen over the Bluetooth channel. As soon
as a connection request is received, the Bodynode will accept it and begin communication.
More information in this document:
- https://github.com/ManuDev9/body-nodes-specs/blob/master/EstablishAConnection.spec



A Bluetooth Bodynode has only one internal sensor.

The Bluetooth Bodynode has two LEDs: a green LED and a red LED. The green LED indicates the
status of the Bluetooth connection, while the red LED indicates the status of communication
with the internal sensor.
- Red LED ON: There is a problem communicating with the sensor.
- Red LED BLINKING: The sensor is not calibrated yet.
- Red LED OFF: The sensor is communicating correctly.
- Green LED OFF: The Bluetooth Bodynode is not connected to any Central device.
- Green LED BLINKING: The Bluetooth Bodynode is connecting with a Central device.
- Green LED ON: The Bluetooth Bodynode is connected to the Central device and is now sending data.

If the internal sensor becomes temporarily disconnected, the red LED will turn ON. The Bluetooth
Bodynode will then attempt to keep pinging the internal sensor until it becomes available again.
As soon as communication with the internal sensor is re-established, the red LED will turn OFF.

The internal sensor's calibration is always checked before any read, and the red LED status
is updated accordingly. Therefore, if the sensor is not calibrated, the red LED will start
blinking, and no data will be sent. Movement information and supported body parts are defined
in the following document:
    - https://github.com/ManuDev9/body-specs-specs/blob/master/Messages.spec

The data is read from the sensor every 30 milliseconds.

The read data is then compared with the previously sent data. If the read data exceeds a specific
range of the previous data, it is sent and becomes the new previous sent data. If it does not
exceed the range, the new data is not sent, and the previous data remains unchanged. For digital
values, any change is sent because the possible values are 0 and 1, so any change is meaningful.

The actions the node can receive are defined in the following document:
    - https://github.com/ManuDev9/body-nodes-specs/blob/master/Actions.spec

Actions are also checked every 30 milliseconds, usually after reading the sensor.