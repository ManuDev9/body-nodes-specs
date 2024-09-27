
MIT License

Copyright (c) 2019-2024 Manuel Bottini

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

Messages Development Specification Version 1.0

This document describes the type of messages the Bodynodes nodes send.
Please open an Issue in case the document is ambiguous or missing information.

The type of messages are:
- Sensor Messages:
  - Absolute Orientation: a Quaternion of 4 values [w, x, y, z] which corresponds to the absolute orientation
    in space of the Node
  - Relative Acceleration: a Vector of 3 values [x, y, z] which corresponds to the acceleration of the Node
    respect to the local axis (the axis of the sensor in the node). It is usually the raw acceleration coming
	from the sensor with no reorientation of any sort.
  - Gloves: an array of 9 values [ a1, a2, a3, a4, a5, d1, d2, d3, d4 ]. 5 analogue values corresponding to the
    angle of each finger (0 is straigth finger, 90 is closed finger). Then there are 4 digitavl values indicating
	if the finger is touching the thumb (1) or not (0)
	NOTE: typically only hand_left ad hand_right could have "gloves" sensor data type information
  - Shoes: an array of 1 value [d1]. The value indicates if the foot is stepping on the floor (1) or if it is
    lifted (0)
	NOTE: typically only foot_left ad foot_right could have "shoes" sensor data type information
- Reset Messages: in some cases the Node might autorecalibrate, or the User might need to reset the position of the
  Node in the application. In these cases, the Node should be able to send a direct message to recalibrate to
  the Host. The message will just contain as value "reset"
  NOTE: typically only "orientation_abs" sensor types would send recalibrate messages

Depending on the communication technology the messages are encoded in different ways. The communication
technologies considered are:
- Wifi
- Bluetooth
- BLE

The message has to identify a "player", which indicates the group the node sending the message belongs to.
Consider a game with multiple players, each with its own bodynodes suit. The nodes will specify to which suit
they belong with "player".
The player field is in use at application level.

The supported sensor types are indicated in the "Sensor Types" document.

The specification is made to accommodate Bodynodes with multiple sensors on it, or Bodynodes receiving
information from others and acting as a bridge. In order to uniquely identify a sensor on the Local Bodynodes
Network, the conjunction <player> + <bodypart> + <sensortype> is used. Therefore different sensors  with same
<player> + <bodypart> + <sensortype> combination in the network are not expected.

---------------------------------------------------------
Message Format for Bluetooh and Wifi
---------------------------------------------------------

The Node sends messages to the Host via the created communication channel (can be via Wifi or Bluetooth).
The messages from the Node are encoded in a sequence of bytes UTF-8. The bytes will represent a string of
a JSON array containing 1 or more JSON objects.

A single JSON Message object is composed by the following fields:
- "player" indicating the player, example:
  - "player" : "user1"
- "bodypart" indicating the bodypart. Check the "Body Parts Names" section in the "Bodyparts" document for the
  values to use. Example:
  - "bodypart" : "lowerbody"
- "sensortype" indicating the sensor type. Check in the "Sensor Types" document what sensor types are defined
- "value" containing the value of the message. Check in the "Sensor Types" document for what values to expect

Example:

player = mario
bodypart = lowerleg_left
sensortype = acceleration_rel
value = [ -0.4545, -0.1150, -0.8029 ]

Message JSON = {
  "player" : "mario",
  "bodypart" : "forearm_right",
  "type" : "orientation",
  "value" : [ -0.4545, -0.1150, -0.8029 ]
}

---------------------------------------------------------
Message Format for BLE
---------------------------------------------------------

BLE is a different type of technology and needs a different way of sending data.
It is based on Services that Contains Characteristics with data. Characteristics can then send data
when read or a notification. Services and Characteristics are identified by UUID

A BLE Bodynode will thefore have a Bodynodes Service with this UUID:
0x0000CCA0-0000-1000-8000-00805F9B34FB

The Bodynodes Service will have the following Bodynodes Characteristics:
- "player" indicating the player, example:
  - "player" : "user1"
  - With UUID: 0x0000CCA1-0000-1000-8000-00805F9B34FB
- "bodypart" indicating the bodypart. Check the "Body Parts Names" section in the "Bodyparts" document for the
  values to use. Example:
  - "bodypart" : "lowerbody"
  - With UUID: 0x0000CCA2-0000-1000-8000-00805F9B34FB
- "sensortype1" indicating the sensor type. Check in the "Sensor Types" document what sensor types are defined
  - With UUID: 0x0000CCA3-0000-1000-8000-00805F9B34FB
- "value1" containing the value of the message. Check in the "Sensor Types" document for what values to expect
  - With UUID: 0x0000CCA4-0000-1000-8000-00805F9B34FB
...
- "sensortype<X>" indicating the sensor type. Check in the "Sensor Types" document what sensor types are defined
  - With UUID: 0x0000CCA<Y>  where Y = 2 + 2 * (X - 1) + 1 
- "value<X>" containing the value of the message as a group of 4 floats, tot (4 x 4) 16 bytes. Check in the
    "Sensor Types" document for what values to expect
  - With UUID: 0x0000CCA<Y>  where Y = 2 + 2 * (X - 1) + 2 


