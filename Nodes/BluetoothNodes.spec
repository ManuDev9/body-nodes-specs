
MIT License

Copyright (c) 2024 Manuel Bottini

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

BluetoothNode Specification Version 1.0

This document describes the main characteristics of the Bodynodes BluetoothNode.
Please open an Issue in case the document is ambiguous or missing information.

The BluetoothNode is the Bluetooth node that collects movement information and sends it as Peripheral
device to the Central device (host application). It also listens for actions from the Central device.
As a note this is a 1-to-1 connection, the Bluetooth node can connect to only one Central device at
a time.

The Central device (Bodynode Host with Bluetooth capabilities) will be the one to try to connect to
the BluetoothNode. It is suggested for the BluetoothNode to advertise itself as BluetoothNode to make
it simpler to find.

The BodynodesSensor app has the same specs indicated in this document.

A BluetoothNode has only one internal sensor.

The BluetoothNode has two LEDs: a green LED and a red LED. The green LED indicates the status of the connection
(Bluetooth), while the red LED indicates the status of the communication with the internal sensor.

Red LED ON: There is a problem communicating with the sensor
Red LED BLINKING: the sensor is not calibrated yet
Red LED OFF: The sensor is correctly communicating

Green LED OFF: The BluetoothNode is not connected to any Central device
Green LED BLINKING: The BluetoothNode is connecting with a Central device
Green LED ON: The BluetoothNode is connected to the Central devices and it is now sending data

If the internal sensor gets temporarily disconnected the red LED will turn ON. The BluetoothNode will the
try to keep pinging the internal sensor until it becomes available again. As soon as the communication with
the internal sensor re-establishes the red LED turns OFF.  

The internal sensor calibration is always checked before any read and the Red LED status is updated accordingly.
Therefore if the sensor turns out not calibrated the Red LED will start blinking and no data will be sent.
The movement information the node sends and supported body parts are defined in the following document:
    - https://github.com/ManuDev9/body-specs-sensor/blob/master/Messages.spec

The data is read from the sensor every 30 milliseconds.

The read data is then checked with the previously sent data. If read data exceeds the a specific range of
the previous data, it is sent and becomes new previous sent data. If it does not exceed the new data is not
sends and previous data does not change. For digital values any change is sent because the possible values
are 0 and 1, so any change is meaningful.

The actions the node can receive is defined in the following document:
    - https://github.com/ManuDev9/body-nodes-specs/blob/master/Actions.spec

Action is also checked every 30 milliseconds usually after reading the sensor.


