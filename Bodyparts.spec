# Bodyparts Development Specification Version 1.0

This document details the body parts and composite suit identifiers supported by Bodynodes, along with their applicable sensor types.

> **Note:** Please open an Issue if this document is ambiguous or missing information.

---

## 1. Body Parts & Compatible Sensor Types

Bodynodes classifies nodes based on their physical placement or functional grouping. Below is the full mapping of supported body parts and their compatible sensor data types.

| Body Part Identifier | Type Category | Supported Sensor Types | Description / Notes |
| :--- | :--- | :--- | :--- |
| `"none"` | Reserve | *None* | Unassigned or uninitialized node state. |
| `"head"` | Standard Inertial | `orientation_abs`, `acceleration_rel`, `angularvelocity_rel` | Head sensor placement. |
| `"upperbody"` | Standard Inertial | `orientation_abs`, `acceleration_rel`, `angularvelocity_rel` | Chest / upper torso placement. |
| `"lowerbody"` | Standard Inertial | `orientation_abs`, `acceleration_rel`, `angularvelocity_rel` | Waist / pelvis / lower torso placement. |
| `"body"` | Standard Inertial | `orientation_abs`, `acceleration_rel`, `angularvelocity_rel` | Single torso sensor (legacy/general). |
| `"upperarm_left"` | Standard Inertial | `orientation_abs`, `acceleration_rel`, `angularvelocity_rel` | Left upper arm placement. |
| `"lowerarm_left"` | Standard Inertial | `orientation_abs`, `acceleration_rel`, `angularvelocity_rel` | Left forearm placement. |
| `"hand_left"` | Hand / Glove | `glove`, `orientation_abs`, `acceleration_rel`, `angularvelocity_rel` | Left hand. Exclusively supports `glove` payload. |
| `"upperarm_right"` | Standard Inertial | `orientation_abs`, `acceleration_rel`, `angularvelocity_rel` | Right upper arm placement. |
| `"lowerarm_right"` | Standard Inertial | `orientation_abs`, `acceleration_rel`, `angularvelocity_rel` | Right forearm placement. |
| `"hand_right"` | Hand / Glove | `glove`, `orientation_abs`, `acceleration_rel`, `angularvelocity_rel` | Right hand. Exclusively supports `glove` payload. |
| `"upperleg_left"` | Standard Inertial | `orientation_abs`, `acceleration_rel`, `angularvelocity_rel` | Left thigh placement. |
| `"lowerleg_left"` | Standard Inertial | `orientation_abs`, `acceleration_rel`, `angularvelocity_rel` | Left shin/calf placement. |
| `"foot_left"` | Foot / Shoe | `shoe`, `orientation_abs`, `acceleration_rel`, `angularvelocity_rel` | Left foot. Exclusively supports `shoe` payload. |
| `"upperleg_right"` | Standard Inertial | `orientation_abs`, `acceleration_rel`, `angularvelocity_rel` | Right thigh placement. |
| `"lowerleg_right"` | Standard Inertial | `orientation_abs`, `acceleration_rel`, `angularvelocity_rel` | Right shin/calf placement. |
| `"foot_right"` | Foot / Shoe | `shoe`, `orientation_abs`, `acceleration_rel`, `angularvelocity_rel` | Right foot. Exclusively supports `shoe` payload. |
| `"katana"` | Accessory / Prop | `orientation_abs`, `acceleration_rel`, `angularvelocity_rel` | Handheld sword or motion controller prop. |
| `"untagged"` | Utility | Any single type | Default tag (`untagged` or `untagged_<number>`). Rename recommended. |
| `"all"` | Wildcard / Broadcast | *Special* | Wildcard target used for broadcast actions/commands. |

---

## 2. Composite Suit Identifiers

Composite body parts represent aggregated suits that combine multiple inertial sensors into a single unified telemetry vector ($N \times D$).

> **Important Constraint:** Composite suits **only aggregate inertial sensor streams** (`orientation_abs`, `acceleration_rel`, `angularvelocity_rel`). They **never include** `glove` or `shoe` sensor types.

| Suit Identifier | Contained Single Body Parts ($N$) | Contained Sub-Parts (Ordered Sequence) |
| :--- | :--- | :--- |
| **`fullsuit`** | 11 parts | `head`, `lowerarm_left`, `upperarm_left`, `lowerarm_right`, `upperarm_right`, `lowerleg_left`, `upperleg_left`, `lowerleg_right`, `upperleg_right`, `upperbody`, `lowerbody` |
| **`uppersuit`** | 7 parts | `head`, `lowerarm_left`, `upperarm_left`, `lowerarm_right`, `upperarm_right`, `upperbody`, `lowerbody` |
| **`lowersuit`** | 4 parts | `lowerleg_left`, `upperleg_left`, `lowerleg_right`, `upperleg_right` |

---

## 3. Sensor Type Rules Summary

1. **Inertial Sensors (`orientation_abs`, `acceleration_rel`, `angularvelocity_rel`):**
   * Compatible with all standard body parts, props (`katana`), untagged nodes, and composite suits (`fullsuit`, `uppersuit`, `lowersuit`).
2. **Glove Sensor (`glove`):**
   * Restricted strictly to `hand_left` and `hand_right`. Never included in composite suits.
3. **Shoe Sensor (`shoe`):**
   * Restricted strictly to `foot_left` and `foot_right`. Never included in composite suits.