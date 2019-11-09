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

This document describes the type of action information the BodyNodes nodes can receive.

The actions supported are:
	- Haptic


Depending on the communication technology the movement information is encoded in different ways. The communication technologies considered are:
	- WiFi
	- BLE
	- Bluetooth


---------------------------------------------------------
WiFi Nodes
---------------------------------------------------------

The action is sent from the server to the WiFi node and it has the following format:
	- JSON, depending on the action it has different fields

Haptic action

Json composition of Haptic action:
	- Key “action”, with value:
		- “haptic”
	- Key “duration_ms” with value 
		- an unsigned integer of max 16 bits indicating the duration in ms example:
			- 500, indicating 500 ms
	- Key “strength” with value
		- An unsigned integer ranging from 0 (no vibration) to 255 (maximum), example:
			- 150, medium strength
	- (Optional) Key “bodypart”, with any string value. If not present all bodyparts should act. Single bodynodes will just ignore this field


Example 1:

action = haptic
duration_ms = 250
strength = 200

Json = {
	“action”:“haptic”,
	“duration_ms” : 250,
	“strength” : 200
}

Example 2:

action = haptic
bodypart = upperarm_left
duration_ms = 250
strength = 200

Json = {
	“action”:“haptic”,
	“duration_ms” : 250,
	“strength” : 200,
	“bodypart” : “upperarm_left” 
}



---------------------------------------------------------
BLE Nodes
---------------------------------------------------------

BLE works with services and characteristics which are identified by UUIDs. The only rule about the UUID is that it should start with:
“0000CC”

All the services and characteristics starting as indicated will be read and considered. There are 2 type of characteristics:
	- Orientation Characteristic
	- Action Characteristic

In this document only Action Characteristics are considered.

The characteristic has the following properties:
	- Can be read
	- Can be written

When reading the characteristic will return the action and the name of the bodypart the action will be applied. Each action will be described separately.

The action is sent from the application to the BLE node and it has the following format:
	- Array of bytes, depending on the action it has a different sequence of bytes

Haptic

When reading the characteristic will return a string composed of 2 elements: action tag and bodypart separated by a “:” character. In this case the action tag for haptic is:
	- “hap”
 
So, considering as bodypart “forearm_left”, reading the action characteristic will return:
	- “hap:forearm_left”

When written a haptic action characteristic has to have the following array format:
	- Bytes of index 0 1 indicating the haptic action:
		- 0x0001
	- Bytes of index 2 3 containing the unsigned integer representation of the duration in ms, example 255 ms:
		- 0x00FF
	- Byte of index 4 containing the unsigned integer representation of the strength in ms, example 100
		- 0x64


---------------------------------------------------------
Bluetooth Nodes
---------------------------------------------------------

The action is sent from the server to the bluetooth node and it has the following format:
	- Array of bytes, depending on the action it has a different sequence of bytes

Haptic action

Array format:
	- Bytes of index 0 1 indicating the start of the packet, fixed to:
		- 0x0000
	- Bytes of index 2 3 indicating the haptic action:
		- 0xCCD1
	- Bytes of index 4 5 containing the unsigned integer representation of the duration in ms, example 255 ms:
		- 0x00FF
	- Byte of index 6 containing the unsigned integer representation of the strength in ms, example 100
		- 0x64
	- Bytes of index 7 8 indicating the end of the packet, fixed to:
		- 0x0000


