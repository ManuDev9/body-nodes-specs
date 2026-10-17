
MIT License

Copyright (c) 2019-2026 Manuel Bottini

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

-----------------------------

# Establish A Connection Development Specification Version 1.0

This document describes the protocol for establishing communication, managing session state, and exchanging control/telemetry messages within the **Bodynodes** network across Wi-Fi, Bluetooth Classic (Serial), and Bluetooth Low Energy (BLE).

> **Note:** Please open an Issue if this document is ambiguous or missing information.

---

## 1. Network Actors

In all transport protocols, communication involves two primary actors:

* **Node:** Embedded hardware unit attached to a body part/suit. It gathers movement and telemetry data from local sensors and transmits it to the Host.
* **Host:** Central application/gateway that discovers Nodes, manages active connections, and exposes real-time sensor streams to the main application layer.

> **Security & Encryption Note:** Encryption is currently not implemented at the application protocol level across any transport mechanism.
>
> **Network Scope Note:** The current network architecture operates under a simplified assumption where sensors are non-overlapping. Each `<player>` + `<bodypart>` + `<sensortype>` combination exists at most once across the active local network.

---

## 2. Wi-Fi (UDP) Communication

Communication over Wi-Fi uses UDP for lightweight, high-frequency telemetry delivery. Packets are unacknowledged stream frames sent without delivery guarantees.

### 2.1 Connection Parameters

| Parameter | Value | Description |
| :--- | :--- | :--- |
| **Unicast Data Port** | `12345` | UDP port used for direct Node-to-Host telemetry stream and Host actions. |
| **Multicast Discovery Port** | `12346` | UDP multicast port used by the Host for discovery broadcasts. |
| **Multicast Group IPv4** | `239.192.1.99` | Local-scope multicast address for host beaconing. |

### 2.2 Connection Flow Sequence

1. **Host Discovery Beacon:** The Host continuously broadcasts a UDP multicast message `"BN"` to `239.192.1.99:12346` every **5 seconds**.
2. **Node Discovery:** A Node listening on the multicast group receives the `"BN"` beacon and extracts the Host's IP address.
3. **Node Handshake Request:** The Node sends a unicast UDP `"ACKN"` message to the Host on port `12345` and enters a waiting state.
4. **Host Handshake Response:** The Host receives `"ACKN"`, registers the Node's IP address, responds with a unicast UDP `"ACKH"` message on port `12345`, and begins listening for telemetry stream packets.
5. **Telemetry Stream Start:** Upon receiving `"ACKH"`, the Node transitions to the active state and begins streaming sensor JSON arrays to port `12345`.

### 2.3 Action Execution Flow

Actions (e.g., calibration, reset, parameter configuration) are initiated by the Host:

1. **Action Request:** The Host sends an action command frame to the Node's unicast address on port `12345`.
2. **Action Confirmation:** The Node executes the received action and sends back an `"ACKN"` frame to confirm receipt.
3. **Retry Mechanism:** The Host retransmits the active action payload continuously until an `"ACKN"` confirmation is received from the target Node.

### 2.4 Keep-Alive & Timeout Rules

* **Node Keep-Alive:** The Node sends a periodic `"ACKN"` pulse sequence every **30 seconds** during active streaming.
* **Node Disconnection Timeout:** If the Node does not receive an `"ACKH"` frame for more than **60 seconds**, it considers the connection lost and halts telemetry transmission.
* **Host Disconnection Timeout:** If the Host receives no data frames or `"ACKN"` pulses from a Node for more than **60 seconds**, it drops the Node from its active roster.

---

## 3. Bluetooth Classic (Serial Port Profile) Communication

Bluetooth Classic uses the Serial Port Profile (SPP) over RFCOMM to establish point-to-point bidirectional streams between the Host and Nodes.

### 3.1 Service Registration & Pairing

* **Service UUID:** `00001101-0000-1000-8000-00805F9B34FB` (Standard Serial Port Profile / SPP UUID).
* **Device Name Advertising:** Nodes advertise themselves as `"Bodynode"`.
* **Pairing Requirement:** Device discovery and pairing must be completed manually or via external OS routines prior to starting the Bodynode Host application. The Host is provided with target Bluetooth MAC addresses to initiate connections.

### 3.2 Connection Flow Sequence

1. **Node Listening:** The Node registers the SPP UUID service, enables Bluetooth discovery, and listens for incoming RFCOMM connections.
2. **Host Connection:** The Host iterates through its configured target Bluetooth MAC addresses and initiates RFCOMM socket connections.
3. **Node Handshake Request:** Upon accepting the incoming socket, the Node immediately transmits an `"ACKN"` text frame over the serial channel and waits.
4. **Host Handshake Response:** The Host receives `"ACKN"`, responds with an `"ACKH"` text frame, and opens its listening buffer.
5. **Telemetry Stream Start:** The Node receives `"ACKH"` and begins streaming UTF-8 JSON telemetry packets over the serial channel.

### 3.3 Action Execution Flow

* **Action Transmission:** The Host writes action commands directly to the serial stream.
* **Action Confirmation:** The Node receives and executes the command, responding with an `"ACKN"` frame over serial. The Host continues retransmitting the action command until `"ACKN"` is confirmed.

### 3.4 Keep-Alive & Timeout Rules

* **Node Keep-Alive:** The Node writes a periodic `"ACKN"` frame to the serial stream every **30 seconds**.
* **Node Disconnection Timeout:** If the Node receives no `"ACKH"` response for over **60 seconds**, it closes the serial channel and re-enters the advertising state.
* **Host Disconnection Timeout:** If the Host receives no serial data or `"ACKN"` frames for over **60 seconds**, it terminates the RFCOMM socket and attempts reconnection.

---

## 4. Bluetooth Low Energy (BLE) Communication

BLE communication follows a standard GATT server/client architecture using a custom primary service UUID and dedicated characteristics.

### 4.1 GATT Architecture & Service Identification

* **Primary Service UUID:** `0x0000CCA0-0000-1000-8000-00805F9B34FB`
* **Device Name Advertising:** BLE Nodes advertise under the device name `"Bodynode"`.

#### Characteristic Layout

| Characteristic Name | UUID | Access | Purpose / Content |
| :--- | :--- | :--- | :--- |
| **Action Endpoint** | `0x0000CC9F-0000-1000-8000-00805F9B34FB` | Write | Sequenced ASCII string actions (`start:true` -> `key:value` -> `end:true`). |
| **Player** | `0x0000CCA1-0000-1000-8000-00805F9B34FB` | Read | Identifies assigned player/user (e.g., `"mario"`). |
| **Bodypart** | `0x0000CCA2-0000-1000-8000-00805F9B34FB` | Read | Identifies body placement or suit (e.g., `"uppersuit"`). |
| **Orientation Abs Value** | `0x0000CCA3-0000-1000-8000-00805F9B34FB` | Read, Notify | Quaternion data array ($N \times 4$). |
| **Acceleration Rel Value** | `0x0000CCA4-0000-1000-8000-00805F9B34FB` | Read, Notify | Acceleration vector array ($N \times 3$). |
| **Glove Value** | `0x0000CCA5-0000-1000-8000-00805F9B34FB` | Read, Notify | Glove flex/touch array (9 values). |
| **Shoe Value** | `0x0000CCA6-0000-1000-8000-00805F9B34FB` | Read, Notify | Shoe pressure array (1 value). |
| **Angular Velocity Rel Value** | `0x0000CCA7-0000-1000-8000-00805F9B34FB` | Read, Notify | Gyroscope vector array ($N \times 3$). |

### 4.2 Connection & Discovery Flow Sequence

1. **Advertising State:** The Node initializes its local GATT table under `0xCCA0` and advertises as `"Bodynode"`.
2. **Host Scan & Connect:** The Host scans for advertising `"Bodynode"` peripheral devices and initiates a GATT connection.
3. **Identity Verification:** The Host checks the peripheral MAC address against its whitelist. If invalid or unassigned, the Host disconnects immediately.
4. **Metadata Discovery:** If validated, the Host reads the `Player` (`0xCCA1`) and `Bodypart` (`0xCCA2`) characteristics to register the node context.
5. **Notification Subscription:** The Host subscribes to Client Characteristic Configuration Descriptors (CCCD) for the specific sensor value characteristics it needs to receive notifications for (`0xCCA3`–`0xCCA7`).
6. **Telemetry Streaming:** The Node pushes GATT notifications automatically whenever new sensor measurements are available.

### 4.3 Actions & Control

Actions in BLE are issued by performing GATT write requests to the **Action Endpoint** characteristic (`0xCC9F`) using ASCII parameter strings wrapped in sequence delimiters (`start:true` -> `key:value` -> `end:true`).