# IBM Tape Library

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p5-blue)
<!-- compatibility-badges:end -->

SNMP monitoring for IBM TS4300 tape libraries. A single `Library Info` service per host reports the library model, serial number, firmware version, and description.

## How it works

The section is fetched via SNMP from `.1.3.6.1.4.1.14851.3.1.3`:

- `.1.0` — model (e.g. `3573-TL`)
- `.2.0` — serial number
- `.3.0` — vendor (used for detection)
- `.4.0` — firmware version
- `.5.0` — description

Detection matches when `.1.3.6.1.4.1.14851.3.1.3.3.0` matches `IBM`. The check always reports OK with a summary line containing all four fields.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/cmk_addons_plugins/ibm/agent_based/ts4300.py` | SNMP section parser and check plugin. |

## Installation

1. Install the MKP on the Checkmk site.
2. Configure SNMP access to the tape library.
3. Run service discovery — a single `Library Info` service is created.

## Services & metrics

- **Service:** `Library Info`
- **Summary:** `Model: <m>, Serial: <s>, Version: <v>, Description: <d>`
- **State:** always OK (informational).
