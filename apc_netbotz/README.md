# APC Netbotz sensors

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0b1-2f4f4f) ![packaged](https://img.shields.io/badge/packaged-2.5.0p18-blue)
<!-- compatibility-badges:end -->

Additional SNMP checks for APC Netbotz environmental appliances, covering sensor types that are not monitored by the built-in Netbotz checks. Tested on APC Netbotz 750. Adds services for beacon, leak, vibration, smoke and motion sensors, cameras and enclosures. Smoke, motion, camera and enclosure checks were contributed by Kamil Jablonski.

## How it works

All sections detect the device via `sysObjectID` starting with `.1.3.6.1.4.1.52674.500` and read the sensor tables of the NetBotz50-MIB:

| Check | SNMP base | Sensor type |
| --- | --- | --- |
| `netbotz_beacon` | `.1.3.6.1.4.1.52674.500.4.2.14.1` | Beacon (`0` off = OK, `1` on = CRIT) |
| `netbotz_leak` | `.1.3.6.1.4.1.52674.500.4.2.13.1` | Leak (`0` noLeak = OK, `1` leakDetected = CRIT) |
| `netbotz_vibration` | `.1.3.6.1.4.1.52674.500.4.2.11.1` | Vibration (`0` noVibration = OK, `1` vibrationDetected = CRIT) |
| `netbotz_smoke` | `.1.3.6.1.4.1.52674.500.4.2.12.1` | Smoke (`0` noSmoke = OK, `1` smokeDetected = CRIT) |
| `netbotz_motion` | `.1.3.6.1.4.1.52674.500.4.2.3.1` | Motion (`0` noMotion = OK, `1` motionDetected = OK by default, configurable with the rule "APC NetBotz motion sensors") |
| `netbotz_camera` | `.1.3.6.1.4.1.52674.500.6.1.1` | Camera (connected = OK, disconnected = CRIT), with model and IP address |
| `netbotz_enclosure` | `.1.3.6.1.4.1.52674.500.2.1.1` | Enclosure: appliance, pods, probes, wireless coordinator (normal = OK, disconnected or error = CRIT), with serial, model and firmware in the details |

Each sensor yields one service with the sensor id as item and the label shown in brackets in the summary. Smoke, motion, camera and enclosure checks also evaluate the error status of the entry (warning = WARN, error, critical, failure = CRIT).

## Package contents

| Path | Purpose |
| --- | --- |
| `src/apc_netbotz/agent_based/beacon.py` | Beacon sensor section and check (service `Beacon <id>`). |
| `src/apc_netbotz/agent_based/leak.py` | Leak sensor section and check (service `Leak <id>`). |
| `src/apc_netbotz/agent_based/vibration.py` | Vibration sensor section and check (service `Vibration <id>`). |
| `src/apc_netbotz/agent_based/smoke.py` | Smoke sensor section and check (service `Smoke <id>`). |
| `src/apc_netbotz/agent_based/motion.py` | Motion sensor section and check (service `Motion <id>`). |
| `src/apc_netbotz/agent_based/camera.py` | Camera section and check (service `Camera <id>`). |
| `src/apc_netbotz/agent_based/enclosure.py` | Enclosure section and check (service `Enclosure <id>`). |
| `src/apc_netbotz/rulesets/netbotz_motion.py` | Rule "APC NetBotz motion sensors": state for detected motion. |
| `src/apc_netbotz/checkman/` | Check manual pages. |

## Installation

1. Install the MKP on the Checkmk site.
2. Add the APC Netbotz device as an SNMP host and run service discovery.
