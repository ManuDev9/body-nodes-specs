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

This document describes the type of messages the BodyNodes nodes send.

The type of messages are:
	- Movement information:
		- A Quaternion of 4 values [w, x, y, z] which corresponds to the absolute orientation in space of the Node


Depending on the communication technology the messages are encoded in different ways. The communication technologies considered are:
	- WiFi
	- BLE
	- Bluetooth/Serial

The suggested body parts are the following:
	- "head"
	- "hand_left"
	- "forearm_left"
	- "upperarm_left"
	- "body"
	- "forearm_right"
	- "upperarm_right"
	- "hand_right"
	- "lowerleg_left"
	- "upperleg_left"
	- "shoe_left"
	- "lowerleg_right"
	- "upperleg_right"
	- "shoe_right"
	- "untagged"
	- "katana"
	- "upperbody"
	- "lowerbody"

Any other name can be used, the library will report them as is to the user. Therefore it is up to the application to properly accept them.

---------------------------------------------------------
WiFi Communication
---------------------------------------------------------

The WiFi node data is send to the server and it has the following format:
A JSON containing as keys
	- “bodypart” which will contain a string indicating the bodypart 
	- “type” which will contain the type of message, supported values are
		- “orientation”
	- “value” which will contain the value of the message
		- For “orientation” the value it is a string representing a Quaternion with four floating points with 4-5 decimal precision separated by “|” : 
			- W|X|Y|Z

Example:

bodypart = forearm_right
type = orientation
message = 0.36791|-0.4545|-0.1150|-0.8029

Json = { 
	“bodypart” : “forearm_right”,
	”type”:”orientation”,
	”message”: ”0.36791|-0.4545|-0.1150|-0.8029” 
}



---------------------------------------------------------
BLE Communication
---------------------------------------------------------

BLE works with services and characteristics which are identified by UUIDs. The only rule about the UUID is that it should start with:
	- “0000CC”

All the services and characteristics starting as indicated will be read and considered. There are 2 type of characteristics:
	- Orientation Characteristic
	- Action Characteristic

In this document only Orientation Characteristics are considered.

The characteristic has the following properties:
	- Can be read
	- Can notify

When reading the characteristic will return the name of the bodypart it refers to.

The application should subscribe to the notification feature in order to receive orientation information. The data the characteristic notifies has the following format:
	- The 16-bytes array contains 4 bytes floating point representation of the four dimensions of a Quaternion:
		- Bytes of index 0 1 2 3 contains W
		- Bytes of index 4 5 6 7 contains X
		- Bytes of index 8 9 10 11 contains Y
		- Bytes of index 12 13 14 15 contains Z




---------------------------------------------------------
Bluetooth/Serial Communication
---------------------------------------------------------

Each message type will be considered separately.

Movement information is send using 22 bytes in total:
	- Bytes of index 0 1 indicating start of packet: 0xFFFF
	- Bytes of index 2 3 indicating the type of the packet:
		- orientation		0x0000
	- Bytes of index 4 5 indicating the body part:
		- "head"			0xCCC1
		- "hand_left"		0xCCC2
		- "forearm_left"	0xCCC3
		- "upperarm_left"	0xCCC4
		- "body"			0xCCC5
		- "forearm_right"	0xCCC6
		- "upperarm_right"	0xCCC7
		- "hand_right"		0xCCC8
		- "lowerleg_left"	0xCCC9
		- "upperleg_left"	0xCCCA
		- "shoe_left"		0xCCCB
		- "lowerleg_right"	0xCCCC
		- "upperleg_right"	0xCCCD
		- "shoe_right"		0xCCCE
		- "untagged"		0xCCCF
		- "katana"			0xCCD0
		- "upperbody"		0xCCD1
		- "lowerbody"		0xCCD2

	- 16-bytes containing 4 bytes floating point representation of the four values of a Quaternion:
		- Bytes of index  6  7  8  9 contains W
		- Bytes of index 10 11 12 13 contains X
		- Bytes of index 14 15 16 17 contains Y
		- Bytes of index 18 19 20 21 contains Z
