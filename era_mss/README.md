# ERA MSS Target Processor Monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0p15-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p15-blue)
<!-- compatibility-badges:end -->

SNMP monitoring for the ERA MSS (Multi-Sensor Surveillance) target processor system from [era.aero](https://www.era.aero/). One check plugin per subsystem produces services for the receiver, transmitter, target processor virtual server, remoter, BVIM, MUSR and NTP status, mapping the vendor status values (`OKA`, `WAR`, `n/a`) to Checkmk OK / WARN / UNKNOWN.

## How it works

All sections are detected via the ERA private enterprise prefix:

```text
sysObjectID startswith .1.3.6.1.4.1.11588.1.5.111   (bvim base)
sysObjectID contains   .1.3.6.1.4.1.311.1.1.3.1.2   (Windows host running the TP)
```

OID base is `.1.3.6.1.4.1.11588.1.5` (ERA MIB). Each subsystem walks its own sub-tree; the shared helper [`utils.py`](src/era_mss/agent_based/utils.py) normalises status values and emits `Result` objects, flagging only the fields that are actually considered "monitored" (the per-field `mon` flag in each parser). Fields like raw CPU / memory / drive usage numbers are reported as info only.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/era_mss/agent_based/utils.py` | Shared detect, discovery and check helpers; status map `OKA/WAR/n/a -> OK/WARN/UNKNOWN`. |
| `src/era_mss/agent_based/bvim.py` | `ERA BVIM` single service (power / DIN status on tp1 and tp2). |
| `src/era_mss/agent_based/vserver.py` | `ERA vServer <idx>` per target processor virtual server (sw, processes, time sync, CPU, memory, drives, LANs). |
| `src/era_mss/agent_based/rx.py` | `ERA <site>` receivers (status, power, FO A/B, mode counters). |
| `src/era_mss/agent_based/tx.py` | `ERA <item>` transmitters. |
| `src/era_mss/agent_based/rmtr.py` | `ERA <item>` remoters. |
| `src/era_mss/agent_based/musr.py` | `ERA MUSR` single service. |
| `src/era_mss/agent_based/ntp.py` | `ERA NTP` single service. |

## Installation

1. Install the MKP on the Checkmk site.
2. Add the ERA MSS device as an SNMP host. Ensure the community / v3 credentials allow reading `.1.3.6.1.4.1.11588.1.5`.
3. Run service discovery.

## Services

- `ERA BVIM`
- `ERA vServer <index>`
- `ERA <site>` — one per RX receiver, TX transmitter and RMTR remoter
- `ERA MUSR`
- `ERA NTP`

## Known limitations

- The `info` file declares destination paths under `era_surveillance_systems/...` while the source on disk lives under `era_mss/...`. The MKP will be packed from whatever the `info` file lists, so double-check the destination namespace before shipping.
- Packaged version is a dev build (`1.0.0-dev3`).
