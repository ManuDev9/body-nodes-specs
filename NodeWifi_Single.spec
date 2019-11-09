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

WIFI_node is the WiFi node that collects movement information and sends it as a client to the server (application). It also listens for actions from the server.

BodyNodeSensor app has the same specs indicated in this document.

The Device Name is:
"WIFI_node"

WIFI_node is connected with only one sensor.

The WIFI_node has two LEDs: a green LED and a red LED. The green LED indicates the status of the connection (WiFI AND Server), while the red LED indicates the status of the communication with the sensor

Red LED ON: There is a problem communicating with the sensor
Red LED BLINKING: ANY or ALL of the sensors are not yet calibrated 
Red LED OFF: The sensor is correctly communicating

Green LED OFF: The WIFI_node is not connected to the WiFi OR the Server is offline
Green LED BLINKING: The WiFi_node is trying to connect with the Server
Green LED ON: The WiFi_node is connected to the WiFi AND communicating with the Server

If the sensor gets temporarily disconnected the red LED will turn ON, and the BLE_node will keep pinging the sensor till it becomes again available. As soon as the communication with the sensor re-establishes the red LED turns OFF.  

The sensor calibration is always checked before any read and the Red LED status is updated accordingly. Therefore if the sensor turns out not calibrated the Red LED will start blinking and no data will be sent.
The movement information the node sends and supported body parts are defined in the following document
https://github.com/ManuDev9/body-specs-sensor/blob/master/Messages_Bodyparts.spec

The data is read from the sensor every 30 milliseconds

The read data is then check with the previous send data:
If read data exceeds the +-0.002 range of the previous data, it is send and becomes new previous send data
If it does not exceed, previous data does not change

The actions the node can receive is defined in the following document
https://github.com/ManuDev9/body-nodes-specs/blob/master/Actions.spec

Action is also checked every 30 milliseconds after read sensor

