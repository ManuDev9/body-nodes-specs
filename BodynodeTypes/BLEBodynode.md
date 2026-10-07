
MIT License

Copyright (c) 2024-2025 Manuel Bottini

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

# BLE Bodynode Development Specification Version 1.1

This document describes the operational characteristics, network behavior, and GATT structure of a generic **BLE Bodynode**.  
*Please open an Issue if this document is ambiguous or missing information.*

---

## 1. Overview & Connection Model

A BLE Bodynode is a BLE Peripheral that collects single-sensor movement information and streams it to a single Central device (Host application). 

* **Topology:** 1-to-1 connection. A BLE Bodynode connects to only one Central device at a time.
* **Discovery:** Upon power-up, the Bodynode enters advertising mode broadcasting as `"Bodynode"`. The Central scans for this name and initiates the connection.
* **Connection Speed:** To sustain 30ms sensor sampling without buffer bloat, the node requests a fast BLE Connection Interval (7.5 ms – 15 ms) upon connection.
* **Protocol Reference:** See [`EstablishAConnection.spec`](https://github.com/ManuDev9/body-nodes-specs/blob/master/EstablishAConnection.spec).

---

## 2. Hardware Diagnostics (LED Status)

The BLE Bodynode features a **Green LED** (BLE Status) and a **Red LED** (Sensor Status):

| LED State | Green LED (BLE) | Red LED (Sensor) | Node Operation |
| :--- | :--- | :--- | :--- |
| **OFF / OFF** | Disconnected | Communicating OK | Standby / Advertising |
| **BLINK / OFF**| Connecting | Communicating OK | Establishing GATT connection |
| **ON / OFF** | Connected | Communicating OK | Fully operational; streaming data |
| **ON / ON** | Connected | Sensor Disconnected | Pinging sensor; BLE stays connected; no data sent |
| **ON / BLINK**| Connected | Uncalibrated | Calibration check failed; BLE stays connected; no data sent |

> **Note on Fault Recovery:** Sensor failures or uncalibrated states **do not** drop the BLE connection. Action execution remains functional even if sensor reads fail.

---

## 3. Data Sampling & Threshold Filtering

1. **Sampling Rate:** Internal sensor data is read every **30 ms** (~33.3 Hz).
2. **Delta Suppression:**
   * **Analog/Continuous Data:** Read values are compared against previously transmitted values. Data is transmitted *only* if the delta exceeds the defined threshold range.
   * **Digital Values:** Any state change (`0` $\leftrightarrow$ `1`) triggers an immediate transmission.
3. **Heartbeat:** Transport-level link integrity is maintained via standard BLE Supervision Timeout.

---

## 4. Complete GATT Service & Characteristics Table

All metadata, sensor data streams, and action execution characteristics reside within the single **Bodynode BLE Service** (`0x0000CCA0-0000-1000-8000-00805F9B34FB`):

| Characteristic Name | Characteristic UUID | Direction / Access | GATT Property | Description / Payload |
| :--- | :--- | :--- | :--- | :--- |
| **Action Write Endpoint** | `0x0000CC9F-0000-1000-8000-00805F9B34FB` | Host $\rightarrow$ Node | `Write` | Sequenced ASCII key-value pairs (`"start:true"`, `<key>:<value>`, `"end:true"`). |
| **Player Identifier** | `0x0000CCA1-0000-1000-8000-00805F9B34FB` | Node $\rightarrow$ Host | `Read` | Assigned player ID string. |
| **Body Part Mapping** | `0x0000CCA2-0000-1000-8000-00805F9B34FB` | Node $\rightarrow$ Host | `Read` | Assigned body part string. |
| **Orientation Abs Value** | `0x0000CCA3-0000-1000-8000-00805F9B34FB` | Node $\rightarrow$ Host | `Read`, `Notify` | Absolute orientation / IMU quaternion payload. |
| **Acceleration Rel Value** | `0x0000CCA4-0000-1000-8000-00805F9B34FB` | Node $\rightarrow$ Host | `Read`, `Notify` | Relative acceleration vector payload. |
| **Glove Value** | `0x0000CCA5