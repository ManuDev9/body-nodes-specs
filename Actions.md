
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

# Action Development Specification v1.0

This document describes the structure and encoding of action messages received by **Bodynodes** nodes.

> **Note:** Please open an Issue if this document is ambiguous or missing information.

---

## 1. Supported Actions

The system supports the following actions:
- `Haptic` (`haptic`)
- `EnableSensor` (`enable_sensor`)
- `SetPlayer` (`set_player`)
- `SetBodypart` (`set_bodypart`)
- `SetWifi` (`set_wifi`)

---

## 2. Body Part Targeting & Action Filtering Rules

When the Host dispatches an action payload, nodes determine whether to execute the action based on the target `bodypart` field and their own configured body part mode:

### Rule 1: Single Body Part Node receiving an Action
* **Exact Single Match:** The node executes the action **only** if the action's `bodypart` field matches its exact assigned body part (e.g., `"hand_right"`) or `"all"`.
* **Composite Target Ignored:** If the action specifies a composite suit target (e.g., `"uppersuit"`, `"fullsuit"`, `"lowersuit"`), a single body part node **will not execute** the action—even if its physical placement falls inside that suit definition. An exact match or `"all"` is strictly required.

### Rule 2: Composite Suit Node receiving an Action
* **Composite Match:** If the action's `bodypart` targets a composite suit name (e.g., `"uppersuit"`) matching the node's configured suit (or `"all"`), the node executes the action across all relevant sensors/actuators it manages.
* **Single Body Part Target (Sub-Targeting):** If the action targets a specific single body part (e.g., `"lowerarm_left"`):
  * **Member Part:** If the target single body part is contained within the composite suit's member list, the composite node **executes** the action (e.g., triggering haptics on that segment or toggling that segment's telemetry stream).
  * **Non-Member Part:** If the target single body part is not part of the suit (e.g., `"foot_left"` sent to an `"uppersuit"` node), the node **ignores** the action.

---

> **Caller Responsibility & State Recovery Note:**
> The caller / host application is responsible for dispatching actions correctly according to the target node's capabilities. 
> 
> Executing structural modification actions with invalid parameter combinations—for example, invoking `set_bodypart` on a composite node with an incompatible or non-suit body part—may cause the node to enter an degraded or unresponsive state where telemetry fails to format as expected.
> 
> Nodes are required to handle such misconfigurations gracefully and must be capable of recovering full normal operation once a valid configuration action (e.g., resetting `set_bodypart` back to a valid composite suit like `"uppersuit"`) is issued.

## 3. Communication Protocols & Encoding

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
Actions are sent sequentially using raw ASCII key-value strings (`<key>:<value>`) written to a dedicated Action characteristic within the **Bodynode BLE Service**:

| Object | Identifier / Name | UUID | Direction | GATT Property |
| :--- | :--- | :--- | :--- | :--- |
| **Service** | Bodynode BLE Service | `0x0000CCA0-0000-1000-8000-00805F9B34FB` | — | — |
| **Characteristic** | Action Write Endpoint | `0x0000CC9F-0000-1000-8000-00805F9B34FB` | Host -> Node | `Write` |

- **Framing Sequence:**
  1. `"start:true"`
  2. Sequential `<key>:<value>` string writes
  3. `"end:true"`

> **Note:** Over BLE, only `Haptic`, `EnableSensor`, `SetPlayer`, and `SetBodypart` are supported (`SetWifi` is omitted). Currently, there is no timeout mechanism if `"end:true"` is omitted; the action simply will not execute.

---

## 4. Action Field Specifications

### 4.1 Haptic Action (`haptic`)

Triggers a haptic feedback pulse on a specified body part or composite suit segment.

| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `type` | `string` | Must be `"haptic"` | `"type": "haptic"` |
| `player` | `string` | Target player identifier | `"player": "user1"` |
| `bodypart` | `string` | Target body part (`"hand_right"`, `"uppersuit"`, `"all"`) | `"bodypart": "lowerarm_left"` |
| `duration_ms` | `uint8` | Pulse duration in milliseconds (`0`–`255`) | `"duration_ms": 250` |
| `strength` | `uint8` | Pulse intensity (`0`–`255`) | `"strength": 200` |

---

### 4.2 Set Player Action (`set_player`)

Reassigns a node (or composite suit node) to a new player identifier.

| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `type` | `string` | Must be `"set_player"` | `"type": "set_player"` |
| `player` | `string` | Current target player identifier | `"player": "user1"` |
| `bodypart` | `string` | Target body part or composite suit | `"bodypart": "all"` |
| `new_player` | `string` | New player identifier to assign | `"new_player": "mario"` |

---

### 4.3 Set Body Part Action (`set_bodypart`)

Reassigns a node to a different single body part or composite suit.

| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `type` | `string` | Must be `"set_bodypart"` | `"type": "set_bodypart"` |
| `player` | `string` | Target player identifier | `"player": "user1"` |
| `bodypart` | `string` | Current body part location to change | `"bodypart": "foot_left"` |
| `new_bodypart` | `string` | New body part location or composite suit | `"new_bodypart": "lowersuit"` |

---

### 4.4 Enable Sensor Action (`enable_sensor`)

Enables or disables a specific sensor stream on a single node or segment of a composite suit.

| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `type` | `string` | Must be `"enable_sensor"` | `"type": "enable_sensor"` |
| `player` | `string` | Target player identifier | `"player": "user1"` |
| `bodypart` | `string` | Target body part or composite suit | `"bodypart": "uppersuit"` |
| `sensortype` | `string` | Target sensor type (see *Sensor Types* doc) | `"sensortype": "orientation_abs"` |
| `enable` | `boolean` | Set `true` to enable, `false` to disable | `"enable": true` |

---

### 4.5 Set Wi-Fi Action (`set_wifi`) *(Wi-Fi & Bluetooth Serial only)*

Configures Wi-Fi credentials and multicast group settings on the node.

| Field | Type | Constraints | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `type` | `string` | Exact match | Must be `"set_wifi"` | `"type": "set_wifi"` |
| `player` | `string` | Standard ID | Target player identifier | `"player": "user1"` |
| `bodypart` | `string` | Standard ID | Target body part or composite suit | `"bodypart": "all"` |
| `ssid` | `string` | Max 32 chars | Wi-Fi network SSID | `"ssid": "MyWifi"` |
| `password` | `string` | Max 64 chars | Wi-Fi network password | `"password": "12345678"` |
| `multicast_group` | `string` | Standard ID | Multicast group name for listening | `"multicast_group": "bn"` |

---

## 5. Examples

### Sub-targeting Haptic Action Example
A `haptic` action targeting `"lowerarm_left"` sent to an `"uppersuit"` node:

#### Wi-Fi / Bluetooth JSON Payload:
```json
{
  "type": "haptic",
  "player": "morty",
  "bodypart": "lowerarm_left",
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