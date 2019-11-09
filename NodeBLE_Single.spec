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

BLE_node is the Bluetooth Low Energy node that collect movement information and sets its own characteristics accordingly, to be read. It also keep checking the action characteristic for actions to be performed.

The Device Name, which is the one seen in the advertisement is:
	- "BLE_node"

BLE_node has only one sensor.

The Local Name depends on the body part assigned to the BLE_node.

The BLE_node has two LEDs: a green LED and a red LED. The green LED indicates the status of the connection, while the red LED indicates the status of the communication with the sensor

	- Red LED ON: There is a problem communicating with the sensor
	- Red LED BLINKING: ANY or ALL of the sensors are not yet calibrated 
	- Red LED OFF: The sensor is correctly communicating

	- Green LED OFF: The BLE_node is not connected to anything
	- Green LED ON: The BLE_node is connected to the BLE_central

If the sensor gets temporarily disconnected the red LED will turn ON, and the BLE_node will keep pinging the sensor till it becomes again available. As soon as the communication with the sensor re-establishes the red LED turns OFF.  

The sensor calibration is always checked before any read and the Red LED status is updated accordingly. Therefore if the sensor turns out not calibrated the Red LED will start blinking and no data will be sent.
The movement information the node sends and UUIDs body parts assigned is defined in the following document:
https://github.com/ManuDev9/body-nodes-specs/blob/master/Messages_Bodyparts.spec

The data is notified from the sensor:
	- every 30 ms on Android 
	- every 60 ms on Win10
		- Win10 cannot handle faster notification speed

Action is also checked after read sensor 

The read data is then check with the previous send data:
If read data exceeds the +-0.01 range of the previous data, it is send and becomes new previous send data
If it does not exceed, previous data does not change


The actions the node can receive is defined in the following document
https://github.com/ManuDev9/body-nodes-specs/blob/master/Actions.spec




