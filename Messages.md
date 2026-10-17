
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

# Messages Development Specification Version 1.0

This document describes the structure and encoding of messages sent by **Bodynodes** nodes.

> **Note:** Please open an Issue if this document is ambiguous or missing information.

---

## 1. Message Types & Data Payload Schemas

Bodynodes nodes transmit movement and sensor telemetry grouped into the following message types:

* **Absolute Orientation (`orientation_abs`)**
  * Quaternion vector of 4 values per body part: `[w, x, y, z]` representing the absolute spatial orientation of the node.
* **Relative Acceleration (`acceleration_rel`)**
  * Vector of 3 values per body part: `[x, y, z]` representing acceleration relative to the node's local sensor frame.
* **Relative Angular Velocity (`angularvelocity_rel`)**
  * Vector of 3 values per body part: `[x, y, z]` representing angular velocity (gyroscope) relative to the node's local sensor frame.
* **Glove Sensor (`glove`)**
  * Array of 9 values: `[a1, a2, a3, a4, a5, d1, d2, d3, d4]`
  * `a1`–`a5`: 5 analog values representing flex angles for each finger (`0` = straight, `90` = fully closed).
  * `d1`–`d4`: 4 digital contact flags indicating if a finger touches the thumb (`1` = contact, `0` = open).
  * *Note:* Typically reserved for `hand_left` and `hand_right` body parts.
* **Shoe Sensor (`shoe`)**
  * Array of 1 value: `[d1]`
  * `d1`: 1 digital flag indicating foot contact (`1` = stepping on ground, `0` = lifted).
  * *Note:* Typically reserved for `foot_left` and `foot_right` body parts.

---

## 2. Composite Body Parts & Vector Sizing

Bodynodes supports composite suits that aggregate sensor data from multiple anatomical body parts into a single message. When using a composite body part, the length of the data array scales proportionally based on the number of contained single body parts ($N$) multiplied by the dimension per part ($D$).

### Composite Suit Definitions

1. **`fullsuit`** (11 single body parts)
   * Contained parts in sequence:
     1. `head`
     2. `lowerarm_left`
     3. `upperarm_left`
     4. `lowerarm_right`
     5. `upperarm_right`
     6. `lowerleg_left`
     7. `upperleg_left`
     8. `lowerleg_right`
     9. `upperleg_right`
     10. `upperbody`
     11. `lowerbody`

2. **`uppersuit`** (7 single body parts)
   * Contained parts in sequence:
     1. `head`
     2. `lowerarm_left`
     3. `upperarm_left`
     4. `lowerarm_right`
     5. `upperarm_right`
     6. `upperbody`
     7. `lowerbody`

3. **`lowersuit`** (4 single body parts)
   * Contained parts in sequence:
     1. `lowerleg_left`
     2. `upperleg_left`
     3. `lowerleg_right`
     4. `upperleg_right`

### Data Payload Sizing & Value Extraction

* **Single Body Part:** Payload size = $1 \times D$
  * Example: Absolute Orientation for `lowerarm_left` = 4 values (`[w, x, y, z]`).
* **Composite Suit:** Payload size = $N \times D$
  * Example: Absolute Orientation for `uppersuit` ($7 \text{ parts} \times 4 \text{ values}$) = 28 values.
  * Example: Absolute Orientation for `fullsuit` ($11 \text{ parts} \times 4 \text{ values}$) = 44 values.
  * Example: Absolute Orientation for `lowersuit` ($4 \text{ parts} \times 4 \text{ values}$) = 16 values.

Values are assigned and extracted sequentially in the exact order defined above:
* For `uppersuit` absolute orientation (28 values total):
  * Elements `[0..3]` $\rightarrow$ `head` (`[w, x, y, z]`)
  * Elements `[4..7]` $\rightarrow$ `lowerarm_left` (`[w, x, y, z]`)
  * Elements `[8..11]` $\rightarrow$ `upperarm_left` (`[w, x, y, z]`)
  * Elements `[12..15]` $\rightarrow$ `lowerarm_right` (`[w, x, y, z]`)
  * Elements `[16..19]` $\rightarrow$ `upperarm_right` (`[w, x, y, z]`)
  * Elements `[20..23]` $\rightarrow$ `upperbody` (`[w, x, y, z]`)
  * Elements `[24..27]` $\rightarrow$ `lowerbody` (`[w, x, y, z]`)

---

## 3. Sensor & Node Identification

To uniquely identify a sensor source across the local Bodynodes network, the combination of **`<player>` + `<bodypart>` + `<sensortype>`** is used.

* **`player`**: Identifies the user or suit grouping at the application level (e.g., `"mario"`).
* **`bodypart`**: Anatomical placement or suit identifier (single body part or composite suit like `"uppersuit"`).
* **`sensortype`**: The category of movement or input being reported (refer to the `Sensor Types` document).

**Uniqueness Constraint:** Multiple active sensors sharing the exact same `<player>` + `<bodypart>` + `<sensortype>` tuple are not supported on the same network.

**Network Scope Note:** The current network architecture operates under a simplified assumption where sensors are non-overlapping. Each `<player>` + `<bodypart>` + `<sensortype>` combination exists at most once across the active local network.

**Improved Node Identification support:** It will be added in next releases as soon as the system is more widely used and we actually hit this problem. 

---

## 4. Communication Technologies & Encoding

### 4.1 Wi-Fi (UDP) & Bluetooth Serial
Messages are transmitted as UTF-8 encoded JSON objects inside a JSON array.

#### JSON Object Fields
* `"player"` *(string)*: Player identifier (e.g., `"user1"`).
* `"bodypart"` *(string)*: Anatomical body part or suit name (e.g., `"uppersuit"`).
* `"sensortype"` *(string)*: Sensor payload type string (e.g., `"orientation_abs"`).
* `"value"` *(array)*: Numerical array of size $N \times D$ matching the schema in Sections 1 & 2.

#### Example Payload (`uppersuit` Absolute Orientation - 28 values)
```json
[
  {
    "player": "mario",
    "bodypart": "uppersuit",
    "sensortype": "orientation_abs",
    "value": [
      1.0, 0.0, 0.0, 0.0,
      0.707, 0.0, 0.707, 0.0,
      1.0, 0.0, 0.0, 0.0,
      0.707, 0.0, -0.707, 0.0,
      1.0, 0.0, 0.0, 0.0,
      1.0, 0.0, 0.0, 0.0,
      1.0, 0.0, 0.0, 0.0
    ]
  }
]
```

---

### 4.2 Bluetooth Low Energy (BLE)
BLE uses GATT characteristics under a single primary service. Sensor types are identified implicitly by their Characteristic UUID.

* **Primary Service UUID:** `0x0000CCA0-0000-1000-8000-00805F9B34FB`

#### GATT Characteristics Layout

| Characteristic Name | UUID | Access / Property | Format / Description |
| :--- | :--- | :--- | :--- |
| **Action Endpoint** | `0x0000CC9F-0000-1000-8000-00805F9B34FB` | `Write` | Sequenced ASCII string actions (`start:true` $\rightarrow$ `key:value` $\rightarrow$ `end:true`). |
| **Player** | `0x0000CCA1-0000-1000-8000-00805F9B34FB` | `Read` | UTF-8 String (e.g., `"user1"`). |
| **Bodypart** | `0x0000CCA2-0000-1000-8000-00805F9B34FB` | `Read` | UTF-8 String (e.g., `"uppersuit"`). |
| **Orientation Abs Value** | `0x0000CCA3-0000-1000-8000-00805F9B34FB` | `Read`, `Notify` | Array of $N \times 4$ quaternions. |
| **Acceleration Rel Value** | `0x0000CCA4-0000-1000-8000-00805F9B34FB` | `Read`, `Notify` | Array of $N \times 3$ acceleration vectors. |
| **Glove Value** | `0x0000CCA5-0000-1000-8000-00805F9B34FB` | `Read`, `Notify` | Array `[a1, a2, a3, a4, a5, d1, d2, d3, d4]`. |
| **Shoe Value** | `0x0000CCA6-0000-1000-8000-00805F9B34FB` | `Read`, `Notify` | Array `[d1]`. |
| **Angular Velocity Rel Value** | `0x0000CCA7-0000-1000-8000-00805F9B34FB` | `Read`, `Notify` | Array of $N \times 3$ gyro vectors. |