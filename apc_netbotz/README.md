# APC Netbotz sensors

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p24-blue)
<!-- compatibility-badges:end -->

Additional SNMP checks for APC Netbotz environmental appliances, covering sensor types that are not monitored by the built-in Netbotz checks. Tested on APC Netbotz 750. Adds services for beacon, leak and vibration sensors.

## How it works

All three sections detect the device via `sysObjectID` starting with `.1.3.6.1.4.1.52674.500` and read three OIDs (sensor id, value, label) per sensor from the NetBotz50-MIB:

| Check | SNMP base | Sensor type |
| --- | --- | --- |
| `netbotz_beacon` | `.1.3.6.1.4.1.52674.500.4.2.14.1` | Beacon (`0` off = OK, `1` on = CRIT) |
| `netbotz_leak` | `.1.3.6.1.4.1.52674.500.4.2.13.1` | Leak (`0` noLeak = OK, `1` leakDetected = CRIT) |
| `netbotz_vibration` | `.1.3.6.1.4.1.52674.500.4.2.11.1` | Vibration (`0` noVibration = OK, `1` vibrationDetected = CRIT) |

Each sensor yields one service with the sensor id as item and the label shown in brackets in the summary.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/apc_netbotz/agent_based/beacon.py` | Beacon sensor section and check (service `Beacon <id>`). |
| `src/apc_netbotz/agent_based/leak.py` | Leak sensor section and check (service `Leak <id>`). |
| `src/apc_netbotz/agent_based/vibration.py` | Vibration sensor section and check (service `Vibration <id>`). |

## Installation

1. Install the MKP on the Checkmk site.
2. Add the APC Netbotz device as an SNMP host and run service discovery.
