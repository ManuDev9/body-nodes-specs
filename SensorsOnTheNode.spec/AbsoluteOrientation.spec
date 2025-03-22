
MIT License

Copyright (c) 2021-2025 Manuel Bottini

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

This specification works for all types of Bodynodes: SNodes, normal Nodes, BLE Nodes, WiFi Nodes, Bluetooth Nodes, etc...

The expected absolute orientation for a bodynode is in Quaternion. Therefore 4 values (W, X, Y, Z) representing an orientation are expected.

Note:
You can use any program that outputs the quanternion W, X, Y, Z values of the sensor.
You can use the "sensor_test" program and check the output of the IMU sensor from serial communication.

---------------------------------------------------------
PROCEDURE
---------------------------------------------------------

Open this Blender Project and modify it in order to make use of the correct Host for your Nodes configuration:
https://github.com/ManuDev9/body-nodes-host/tree/master/pc/blender/BlenderOrientationReference

You will need to clone locally the body-nodes-host repo:
https://github.com/ManuDev9/body-nodes-host/tree/master

Select the Scripting tab and you'll see a small panel with some python code, click on it and keep the mouse in
the area.

Now press the buttons ALT-P and the main script will be loaded which will add a new "Bodynodes Main" right panel.

Make sure your Node under test is connected to the Wifi, or advertising if BLE, or already paired if Bluetooth.
Also you want your Node to be set as player "1" and bodypart "katana".

Press Start and wait for the Host to connect to the Nodes.

Feel free to click on Window->Toggle System Console to check the output and see the logs

In a bunch of seconds the Node will connect and move the "katana" object in the 3D scene.

You want to align with the pointing part and make sure that the "katana" object rotates upwards/downwards,
left/right, clockwise/counterclockwise as you expect.

Note that the "katana" object initially points along the X axis of the Empty Frame Object XYZ.

You can readapt your Bodynodes Sensor via Hardware and/or via Software.

In order to readapt the Sensor via Hardware you can rotate the internal IMU sensor in a way that makes more
sense to you or aligns immediately with the "katana" object

You can also readapt the Sensor via code.

This is an example of code that you can use to "realign" your quaternion values (W, X, Y, Z)
	
// Device Specific Axis Configuration

#define OUT_AXIS_W 0
#define OUT_AXIS_X 1
#define OUT_AXIS_Y 2
#define OUT_AXIS_Z 3

#define MUL_AXIS_W -1
#define MUL_AXIS_X 1
#define MUL_AXIS_Y -1
#define MUL_AXIS_Z 1

// Realign function
imu::Quaternion realignQuat(imu::Quaternion sensor_quat){

  float values[4] = {
    sensor_quat.w(),
    sensor_quat.x(),
    sensor_quat.y(),
    sensor_quat.z()
  };

  float w = MUL_AXIS_W * values[OUT_AXIS_W];
  float x = MUL_AXIS_X * values[OUT_AXIS_X];
  float y = MUL_AXIS_Y * values[OUT_AXIS_Y];
  float z = MUL_AXIS_Z * values[OUT_AXIS_Z];
  
  imu::Quaternion quat = imu::Quaternion(w, x, y, z);
  return quat;
}

//// Code to read from sensor
imu::Quaternion sensor_quat = mBNO.getQuat();
imu::Quaternion quat = realignQuat(sensor_quat);


Alternatively feel free to use the BnReorientAxis implementations in https://github.com/ManuDev9/body-nodes-common.
The is the cbasic implementation as example:
https://github.com/ManuDev9/body-nodes-common/blob/main/cbasic/BnReorientAxis.h
https://github.com/ManuDev9/body-nodes-common/blob/main/cbasic/BnReorientAxis.c

