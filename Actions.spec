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

Action Development Specification Version 1.0

This document describes the type of action information the Bodynodes nodes can receive.
Please open an Issue in case the document is ambiguous or missing information.

The actions supported are:
- Haptic
- EnableSensor
- SetPlayer
- SetBodypart
- SetupWifi

Depending on the communication technology the movement information is encoded in different ways.

The communication technologies considered are:
- Wifi

---------------------------------------------------------
Wifi Communication
---------------------------------------------------------

The action is sent from the Host to the Wifi node with the UDP protocol.

Actions are encoded in UDP packets which are a sequence of bytes.
The bytes will represent a string of a JSON object.
Every action has a specific JSON.

Haptic action JSON fields:
- "type" indicating the haptic action with:
	- "type" : "haptic"
- "player" indicating the player. Example:
  - "player" : "user1"
- "bodypart" indicating the bodypart, check the "Body Parts Names" section in the "Bodyparts" document for the values to use. Example:
  - "bodypart" : "hand_right"
- "duration_ms" containing the unsigned integer representation of the duration in ms, example 255 ms:
  - "duration_ms" : 255
- "strength" containing the unsigned integer representation of the strength, example 100
  - "strength" : 100

SetPlayer action JSON fields:
- "type" indicating the set_player action:
  - "type" : "set_player"
- "player" indicating the player. Example:
  - "player" : "user1"
- "bodypart" indicating the bodypart to change. Check the "Body Parts Names" section in the "Bodyparts" document for the values to use. Example:
  - "bodypart" : "all"
- "new_player" indicating the new player to assign. Example:
  - "new_player" : "mario"

SetBodypart action JSON fields:
- "type" indicating the set_bodypart action:
  - "type" : "set_bodypart"
- "player" indicating the player. Example:
  - "player" : "user1"
- "bodypart" indicating the bodypart to change. Check the "Body Parts Names" section in the "Bodyparts" document for the values to use. Example:
  - "bodypart" : "foot_left"
- "new_bodypart" indicating the new bodypart to assign. Check the "Body Parts Names" section in the "Bodyparts" document for the values to use. Example:
  - "new_bodypart" : "lowerbody"

EnableSensor action JSON fields:
- "type" indicating the enable_sensor action:
  - "type" : "enable_sensor"
- "player" indicating the player. Example:
  - "player" : "user1"
- "bodypart" indicating the bodypart. Check the "Body Parts Names" section in the "Bodyparts" document for the values to use. Example:
  - "bodypart" : "all"
- "sensortype" indicating the sensor. Check the "SensorTypes" document for the values to use. Example:
  - "sensortype" : "orientation_abs"
- "enable" indicating if we want to enable or disable. Example:
  - "enable" : true

SetWifi action JSON fields:
- "type" indicating the set_wifi action:
  - "type" : "set_wifi"
- "player" indicating the player. Example:
  - "player" : "user1"
- "bodypart" indicating the bodypart. Check the "Body Parts Names" section in the "Bodyparts" document for the values to use. Example:
  - "bodypart" : "all"
- "ssid" indicating the SSID of the wifi to connect. Example:
  - "ssid" : "MyWifi"
- "password" indicating the password to connect to the wifi. Example:
  - "password" : "12345678"
- "multicast_group" indicating the name of the multicast group the node should listen to. Example:
  - "multicast_group" : "bn"
  
Example:

action = haptic
player = morty
bodypart = hand_right
duration_ms = 250
strength = 200

Action JSON =
{
	"action" : "haptic"
	"player" : "morty"
	"bodypart" : "hand_right"
	"duration_ms" : 250
	"strength" : 200 
}

