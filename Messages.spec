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

Messages Development Specification Version 1.0

This document describes the type of messages the Bodynodes nodes send.
Please open an Issue in case the document is ambiguous or missing information.

The type of messages are:
- Movement information:
  - Absolute Orientation: a Quaternion of 4 values [w, x, y, z] which corresponds to the absolute orientation in space of the Node
  - Relative Acceleration: a Vector of 3 values [x, y, z] which corresponds to the acceleration of the Node respect to the local axis (the axis of the sensor in the node). It is usually the raw acceleration coming from the sensor with no reorientation of any sort.
- Positioning:
  - Gloves: an array of 9 values [ a1, a2, a3, a4, a5, d1, d2, d3, d4 ]. 5 analogue values corresponding to the angle of each finger (0 is straigth finger, 90 is closed finger). Then there are 4 digitavl values indicating if the finger is touching the thumb (1) or not (0)

NOTE: typically only hand_left ad hand_right have "gloves" sensor data type information

Depending on the communication technology the messages are encoded in different ways. The communication technologies considered are:
- Wifi

The message has to identify a "player", indicating from which group of bodynodes the sending node belongs to.
Think about a game with multiple players and each with its own bodynodes suit. The player field is in use at application level.

The supported sensor types are the following:
- “orientation_abs”
- “acceleration_rel”
- "gloves"

Any other name can be used, the library will report them as is to the user. But it is up to the application to properly accept them.
Using not supported names means that the bodynode won't be able to communicate in standardized systems.

The specification is made to accomodate Bodynodes with multiple sensors on it, or Bodynodes receiving information from others and acting as a bridge.
In order to uniquely identify a sensor on the Local Bodynodes Network in place, the conjunction <player> + <bodypart> + <sensortype> is used.
Therefore it is not expected to different sensors in the network with same <player> + <bodypart> + <sensortype> combination.

---------------------------------------------------------
Wifi Communication
---------------------------------------------------------

The Wifi Node sends messages to the host server via the UDP protocol.
The messages from the Node are encoded in UDP packets which are a sequence of bytes.
The bytes will represent a string of a JSON array containing 1 or more JSON objects.


A single JSON Message object is composed by the following fields:
- "player" indicating the player, example:
  - "player" : "user1"
- "sensortype" indicating the sensor type. Check in the "Sensor Types" document for what sensor types are defined
- "bodypart" indicating the bodypart. Check the "Body Parts Names" section in the "Bodyparts" document for the values to use. Example:
  - "bodypart" : "lowerbody"
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
