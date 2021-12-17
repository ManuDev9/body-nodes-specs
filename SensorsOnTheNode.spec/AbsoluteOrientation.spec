MIT License

Copyright (c) 2021 Manuel Bottini

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

AbsoluteOrientation Specification Version 1.0

This document go through the axis configuration procedure to make a Node follow the Absolute Orientation specification.
Please open an Issue in case the document is ambiguous or missing information.

Any bodynode following this specification easily integrates with the system and return absolute orientation as the host (game etc...) expects.
The specification has been setup arbitrarily.

Anyone can configure its sensor node as he/she wants, but the node will then "rotate" differently than the "virtual" node in the system because the axis are not as the Bodynodes framework expects.

This specification works for all types of Bodynodes: SNodes, normal Nodes, BLE Nodes, WiFi Nodes, Serial Nodes, etc...

The expected absolute orientation for a bodynode is in Quaternion. Therefore 4 values (W, X, Y, Z) representing an orientation are expected.

Note:
You can use any program that outputs the quanternion W, X, Y, Z values of the sensor.
You can use the "sensor_test" program and check the output of the IMU sensor from serial communication.

---------------------------------------------------------
PROCEDURE
---------------------------------------------------------
Just follow the following procedure to configure your axis. Whatever quanternion W_sensor, X_sensor, Y_sensor, Z_sensor values your IMU outputs just made them match with the quanternion W_output, X_output, Y_output, Z_output outputs below

5 Positions Values:
 - Position 1 - Pointing North Direction:
		W_output = 0.04
		X_output = 1.00
		Y_output = 0.04
		Z_output = -0.06
 - Position 2 - From Position 1 point Upwards:
		W_output = -0.64
		X_output = 0.76
		Y_output = 0.09
		Z_output = -0.06
 - Position 3 - From Position 2 go to Position 1 and point West Direction rotating the sensor counterclockwise:
		W_output = 0.07
		X_output = 0.78
		Y_output = 0.62
		Z_output = -0.03
 - Position 4 - From Position 3 keep rotating counterclockwise and point South Direction:
		W_output = 0.02
		X_output = 0.22
		Y_output = 0.98
		Z_output = 0.00
 - Position 5 - From Position 4 rotate clocksise to Position 1 and rotate sensor Upside down clockwise:
		W_output = -0.09
		X_output = 0.12
		Y_output = -0.02
		Z_output = 0.99

This is an example of code that you can use to "realign" your quaternion values (W, X, Y, Z)
	
// Device Specific Axis Configuration
#define SENSOR_AXIS_W 0
#define SENSOR_AXIS_X 1
#define SENSOR_AXIS_Y 2
#define SENSOR_AXIS_Z 3

#define OUT_AXIS_W SENSOR_AXIS_Z
#define OUT_AXIS_X SENSOR_AXIS_Y
#define OUT_AXIS_Y SENSOR_AXIS_X
#define OUT_AXIS_Z SENSOR_AXIS_W

#define MUL_AXIS_W -1
#define MUL_AXIS_X 1
#define MUL_AXIS_Y -1
#define MUL_AXIS_Z 1

// Realign function
imu::Quaternion realignQuat(imu::Quaternion sensor_quat){
  float w = 0;
  float x = 0; 
  float y = 0;
  float z = 0;

  // Axis W
  #if OUT_AXIS_W == SENSOR_AXIS_W
  w = sensor_quat.w();
  #elif OUT_AXIS_W == SENSOR_AXIS_X
  w = sensor_quat.x();
  #elif OUT_AXIS_W == SENSOR_AXIS_Y
  w = sensor_quat.y();
  #elif OUT_AXIS_W == SENSOR_AXIS_Z
  w = sensor_quat.z();
  #endif

  // Axis X
  #if OUT_AXIS_X == SENSOR_AXIS_W
  x = sensor_quat.w();
  #elif OUT_AXIS_X == SENSOR_AXIS_X
  x = sensor_quat.x();
  #elif OUT_AXIS_X == SENSOR_AXIS_Y
  x = sensor_quat.y();
  #elif OUT_AXIS_X == SENSOR_AXIS_Z
  x = sensor_quat.z();
  #endif

  // Axis Y
  #if OUT_AXIS_Y == SENSOR_AXIS_W
  y = sensor_quat.w();
  #elif OUT_AXIS_Y == SENSOR_AXIS_X
  y = sensor_quat.x();
  #elif OUT_AXIS_Y == SENSOR_AXIS_Y
  y = sensor_quat.y();
  #elif OUT_AXIS_Y == SENSOR_AXIS_Z
  y = sensor_quat.z();
  #endif

  // Axis Z
  #if OUT_AXIS_Z == SENSOR_AXIS_W
  z = sensor_quat.w();
  #elif OUT_AXIS_Z == SENSOR_AXIS_X
  z = sensor_quat.x();
  #elif OUT_AXIS_Z == SENSOR_AXIS_Y
  z = sensor_quat.y();
  #elif OUT_AXIS_Z == SENSOR_AXIS_Z
  z = sensor_quat.z();
  #endif

  w = MUL_AXIS_W * w;
  x = MUL_AXIS_X * x;
  y = MUL_AXIS_Y * y;
  z = MUL_AXIS_Z * z;
  
  imu::Quaternion quat = imu::Quaternion(w, x, y, z);
  return quat;
}

//// Code to read from sensor
imu::Quaternion sensor_quat = mBNO.getQuat();
imu::Quaternion quat = realignQuat(sensor_quat);

Note: 
Before glueing the IMU sensor on the board, it is strongly suggested to check if the values are compatible. Then after having properly understood how to position the sensor on your module, you can glue it
If the IMU sensor is already included in the board module, then you need to apply some rotating function on the quaternion.