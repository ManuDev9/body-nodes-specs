
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

------------------------------------------------

# Action Development Specification v1.0

This document describes the structure and encoding of action messages received by **Bodynodes** nodes.

> **Note:** Please open an Issue if this document is ambiguous or missing information.

---

## Supported Actions

The system supports the following actions:
- `Haptic`
- `EnableSensor`
- `SetPlayer`
- `SetBodypart`
- `SetWifi`

---

## Communication Protocols & Encoding

Depending on the underlying transport technology, actions are encoded differently:

| Protocol | Transport | Format |
| :--- | :--- | :--- |
| **Wi-Fi** | UDP Packets | Stringified JSON object |
| **Bluetooth (Classic)** | Serial Port | Stringified JSON object |
| **BLE (Bluetooth Low Energy)** | Action Characteristic (`0xCC9F`) | Sequence of raw ASCII key-value strings |

### Protocol Details

#### Wi-Fi (UDP) & Bluetooth Serial
Actions are serialized into standard JSON strings and transmitted as byte payloads. Each action type maps to a specific JSON schema.

#### Bluetooth Low Energy (BLE)
For the general organization of BLE services and characteristics, refer to [`BodynodeTypes/BLEBodynode.spec`](BodynodeTypes/BLEBodynode.spec).

> **Note:** Over BLE, only `Haptic`, `EnableSensor`, `SetPlayer`, and `SetBodypart` are supported (`SetWifi` is omitted).

Actions are sent sequentially using raw ASCII key-value strings (`<key>:<value>`) written to a dedicated Action characteristic within the **Bodynode BLE Service**:

| Object | Identifier / Name | UUID | Direction | GATT Property |
| :--- | :--- | :--- | :--- | :--- |
| **Service** | Bodynode BLE Service | `0x0000CCA0-0000-1000-8000-00805F9B34FB` | — | — |
| **Characteristic** | Action Write Endpoint | `0x0000CC9F-0000-1000-8000-00805F9B34FB` | Host $\rightarrow$ Node | `Write` |

* **Framing Sequence:**
  1. `"start:true"`
  2. Sequential `<key>:<value>` string writes
  3. `"end:true"`

> **Note on Concurrency & Timeouts:**  
> Currently, there is no timeout mechanism if `"end:true"` is never received after `"start:true"`; in this scenario, the action will simply not execute. Concurrency management for multiple simultaneous BLE connections is deferred to a future revision.

---

## Action Field Specifications

### 1. Haptic Action (`haptic`)

Triggers a haptic feedback pulse on a specified body part.

| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `type` | `string` | Must be `"haptic"` | `"type": "haptic"` |
| `player` | `string` | Target player identifier | `"player": "user1"` |
| `bodypart` | `string` | Target body part (see *Bodyparts* doc) | `"bodypart": "hand_right"` |
| `duration_ms` | `uint8` | Pulse duration in milliseconds (`0`–`255`) | `"duration_ms": 255` |
| `strength` | `uint8` | Pulse intensity (`0`–`255`) | `"strength": 100` |

---

### 2. Set Player Action (`set_player`)

Reassigns a node to a new player identifier.

| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `type` | `string` | Must be `"set_player"` | `"type": "set_player"` |
| `player` | `string` | Current target player identifier | `"player": "user1"` |
| `bodypart` | `string` | Target body part (e.g., `"all"` or specific name) | `"bodypart": "all"` |
| `new_player` | `string` | New player identifier to assign | `"new_player": "mario"` |

---

### 3. Set Body Part Action (`set_bodypart`)

Reassigns a node to a different body part location.

| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `type` | `string` | Must be `"set_bodypart"` | `"type": "set_bodypart"` |
| `player` | `string` | Target player identifier | `"player": "user1"` |
| `bodypart` | `string` | Current body part location to change | `"bodypart": "foot_left"` |
| `new_bodypart` | `string` | New body part location (see *Bodyparts* doc) | `"new_bodypart": "lowerbody"` |

---

### 4. Enable Sensor Action (`enable_sensor`)

Enables or disables a specific sensor on the target node.

| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `type` | `string` | Must be `"enable_sensor"` | `"type": "enable_sensor"` |
| `player` | `string` | Target player identifier | `"player": "user1"` |
| `bodypart` | `string` | Target body part (see *Bodyparts* doc) | `"bodypart": "all"` |
| `sensortype` | `string` | Target sensor type (see *Sensor Types* doc) | `"sensortype": "orientation_abs"` |
| `enable` | `boolean` | Set `true` to enable, `false` to disable | `"enable": true` |

---

### 5. Set Wi-Fi Action (`set_wifi`) *(Wi-Fi & Bluetooth Serial only)*

Configures Wi-Fi credentials and multicast group settings on the node.

| Field | Type | Constraints | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `type` | `string` | Exact match | Must be `"set_wifi"` | `"type": "set_wifi"` |
| `player` | `string` | Standard ID | Target player identifier | `"player": "user1"` |
| `bodypart` | `string` | Standard ID | Target body part | `"bodypart": "all"` |
| `ssid` | `string` | Max 32 chars | Wi-Fi network SSID | `"ssid": "MyWifi"` |
| `password` | `string` | Max 64 chars | Wi-Fi network password | `"password": "12345678"` |
| `multicast_group` | `string` | Standard ID | Multicast group name for listening | `"multicast_group": "bn"` |

---

## Examples

### Haptic Action Example

#### Wi-Fi / Bluetooth JSON Payload:
```json
{
  "type": "haptic",
  "player": "morty",
  "bodypart": "hand_right",
  "duration_ms": 250,
  "strength": 200
}
```

#### BLE Sequential Sequence Writes:
1. `"start:true"`
2. `"type:haptic"`
3. `"player:morty"`
4. `"bodypart:hand_right"`
5. `"duration_ms:250"`
6. `"strength:200"`
7. `"end:true"`