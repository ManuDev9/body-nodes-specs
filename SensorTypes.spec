MIT License

Copyright (c) 2021-2022 Manuel Bottini

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

Sensor Types Development Specification Version 1.0

This document details the Sensor Types supported by Bodynodes.
Please open an Issue in case the document is ambiguous or missing information.

---------------------------------------------------------
Sensor Types
---------------------------------------------------------
These are the supported sensor types:
- "orientation_abs" : Absolute orientation
  - The value is an array representing a Quaternion with four floating points (w, x, y, z):
    - example: [ 0.3, 0.3, 0.3, 0.3 ]
- "acceleration_rel" : Relative acceleration
  - The value is an array representing a Vector with three floating points (x, y, z):
    - example: [ 0.3, 0.3, 0.3 ]
- "glove" : Glove sensor data type
  - The value is an array representing a Vector with 5 integers (a1, a2, a3, a4, a5, d1, d2, d3 ,d4):
	- "a1" is an indication of the angle of the little finger
	- "a2" is an indication of the angle of the fourth finger
	- "a3" is an indication of the angle of the middle finger
	- "a4" is an indication of the angle of the index finger
	- "a5" is an indication of the angle of the thumb
	- "d1" indicates if little finger is in contact with the thumb
	- "d2" indicates if fourth finger is in contact with the thumb
	- "d3" indicates if middle finger is in contact with the thumb
	- "d4" indicates if index finger is in contact with the thumb
    - example: [ 20, 45, 45, 90, 90, 1, 0, 0, 0 ]
- "shoe" : Shoe sensor data type
  - The value is an array representing a Vector with 1 integer (d1)
    - "d1" indicates if the shoes is currently stepping on the ground
