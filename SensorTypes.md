MIT License

Copyright (c) 2021-2026 Manuel Bottini

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

---

# Sensor Types Development Specification Version 1.0

This document details the supported sensor types and their payload definitions for Bodynodes.

> **Note:** Please open an Issue if this document is ambiguous or missing information.

---

## 1. Supported Sensor Types

### 1.1 Absolute Orientation (`orientation_abs`)
* **Description:** Represents the absolute spatial orientation of a node or body part.
* **Format:** Array of 4 floating-point values representing a Quaternion `[w, x, y, z]`.
* **Dimension ($D$):** 4 values per body part.
* **Example Payload:**
  ```json
  [0.7071, 0.0, 0.7071, 0.0]
  ```

---

### 1.2 Relative Acceleration (`acceleration_rel`)
* **Description:** Linear acceleration relative to the local coordinate system of the sensor module.
* **Format:** Array of 3 floating-point values representing a 3D vector `[x, y, z]`.
* **Dimension ($D$):** 3 values per body part.
* **Example Payload:**
  ```json
  [0.3, -0.1, 9.81]
  ```

---

### 1.3 Relative Angular Velocity (`angularvelocity_rel`)
* **Description:** Rotational velocity (gyroscope data) relative to the local coordinate system of the sensor module.
* **Format:** Array of 3 floating-point values representing a 3D vector `[x, y, z]`.
* **Dimension ($D$):** 3 values per body part.
* **Example Payload:**
  ```json
  [0.02, -0.15, 0.01]
  ```

---

### 1.4 Glove Sensor (`glove`)
* **Description:** Captures finger bend angles and contact touch flags.
* **Applicability:** Single body parts only (`hand_left`, `hand_right`).
* **Format:** Array of 9 numerical values `[a1, a2, a3, a4, a5, d1, d2, d3, d4]`:
  * **Flex Angles (0°–90°):**
    * `a1`: Pinky finger flex angle (`0` = straight, `90` = fully closed)
    * `a2`: Ring finger flex angle
    * `a3`: Middle finger flex angle
    * `a4`: Index finger flex angle
    * `a5`: Thumb flex angle
  * **Digital Contacts (1 or 0):**
    * `d1`: Pinky finger touching thumb (`1` = contact, `0` = open)
    * `d2`: Ring finger touching thumb (`1` = contact, `0` = open)
    * `d3`: Middle finger touching thumb (`1` = contact, `0` = open)
    * `d4`: Index finger touching thumb (`1` = contact, `0` = open)
* **Example Payload:**
  ```json
  [20, 45, 45, 90, 90, 1, 0, 0, 0]
  ```

---

### 1.5 Shoe Sensor (`shoe`)
* **Description:** Captures foot step pressure and contact state on the ground.
* **Applicability:** Single body parts only (`foot_left`, `foot_right`).
* **Format:** Array of 1 integer value `[a1]`:
  * `a1`: Step intensity/ground contact indication (`0` = lifted/no contact, `>0` = stepping on ground).
* **Example Payload:**
  ```json
  [1]
  ```

---

## 2. Composite Suit Constraints & Sizing

### Exclusion Rule
> **Important:** Composite suit body parts (`fullsuit`, `uppersuit`, `lowersuit`) **ONLY** aggregate motion streams (`orientation_abs`, `acceleration_rel`, `angularvelocity_rel`). Composite suits **NEVER** include `glove` or `shoe` sensor types, which remain strictly restricted to single dedicated hand or foot nodes.

### Payload Dimension Formula
When reporting sensor data for a composite suit, payload size equals $N \times D$:
* $N$ = Number of single body parts aggregated in the suit
* $D$ = Dimension of the specific sensor type (4 for `orientation_abs`, 3 for `acceleration_rel` and `angularvelocity_rel`)

---

## 3. Composite Suit Examples

### Example 1: `fullsuit` Absolute Orientation (`orientation_abs`)
* **Composite Bodypart:** `fullsuit` ($N = 11$ parts)
* **Sensor Type:** `orientation_abs` ($D = 4$)
* **Total Payload Size:** $11 \times 4 = 44$ floating-point values
* **Sequence Order:** `head` [0..3], `lowerarm_left` [4..7], `upperarm_left` [8..11], `lowerarm_right` [12..15], `upperarm_right` [16..19], `lowerleg_left` [20..23], `upperleg_left` [24..27], `lowerleg_right` [28..31], `upperleg_right` [32..35], `upperbody` [36..39], `lowerbody` [40..43].

```json
[
  1.0, 0.0, 0.0, 0.0,
  0.707, 0.0, 0.707, 0.0,
  1.0, 0.0, 0.0, 0.0,
  0.707, 0.0, -0.707, 0.0,
  1.0, 0.0, 0.0, 0.0,
  1.0, 0.0, 0.0, 0.0,
  1.0, 0.0, 0.0, 0.0,
  1.0, 0.0, 0.0, 0.0,
  1.0, 0.0, 0.0, 0.0,
  1.0, 0.0, 0.0, 0.0,
  1.0, 0.0, 0.0, 0.0
]
```

---

### Example 2: `lowersuit` Relative Acceleration (`acceleration_rel`)
* **Composite Bodypart:** `lowersuit` ($N = 4$ parts)
* **Sensor Type:** `acceleration_rel` ($D = 3$)
* **Total Payload Size:** $4 \times 3 = 12$ floating-point values
* **Sequence Order:** `lowerleg_left` [0..2], `upperleg_left` [3..5], `lowerleg_right` [6..8], `upperleg_right` [9..11].

```json
[
  0.0, 0.0, 9.81,
  0.1, -0.2, 9.80,
  0.0, 0.0, 9.81,
  -0.1, 0.2, 9.82
]
```