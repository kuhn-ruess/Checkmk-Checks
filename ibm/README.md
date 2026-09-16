# IBM Tape Library

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0b1-2f4f4f) ![packaged](https://img.shields.io/badge/packaged-2.5.0p13-blue)
<!-- compatibility-badges:end -->

SNMP monitoring for IBM TS4300 tape libraries. Besides the inventory data of the
library the package monitors the power supplies, the operational status of the
library and its chassis, the tape drives, the media slots and the cleaning
cartridges.

The TS4300 answers neither `sysDescr` nor `sysObjectID`, which is why the tape
library checks shipped with Checkmk never discover on these devices. All checks
of this package therefore detect on the SNIA product vendor OID
`.1.3.6.1.4.1.14851.3.1.3.3.0` — the host needs the rule
**Hosts without system description OID** for that to work.

## Services

| Service | Source | Description |
| --- | --- | --- |
| `Library Info` | SNIA-SML `.1.3.6.1.4.1.14851.3.1.3` | Model, serial, firmware, description. Informational. |
| `Library Status` | SNIA-SML `.10.2.0`, `.4.10.1` | Operational status of the library and of every chassis. |
| `Power Supply <chassis>/<n>` | IBM Automation Query `.1.3.6.1.4.1.2.6.257.1.3.2.1` | Both power supply slots per chassis. `not ok` is CRIT. |
| `Drive <name>` | SNIA-SML `.6.2.1` + IBM AQ `.1.5.2.1` | Availability, status, cleaning request, mount count, operating time, LTO generation, firmware, control path and port link states. |
| `Slots <type>` | SNIA-SML `.13.3.1` | Utilization of the storage slots and of the I/O station. |
| `Cleaning Cartridges` | SNIA-SML `.13.3.1.17` | Number of cleaning cartridges and where they sit. |

## Two MIBs

The SNIA-SML-MIB (`.1.3.6.1.4.1.14851.3.1`) describes the library in CIM terms —
changer, drives, media locations, ports. Everything the library knows about its
own hardware and configuration sits in the IBM Automation Query MIB
(`ibmQueryConfig`, `.1.3.6.1.4.1.2.6.257`) instead; the power supply status is
only available there.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/ibm/agent_based/ts4300.py` | Library information. |
| `src/ibm/agent_based/ts4300_library.py` | Library and chassis status. |
| `src/ibm/agent_based/ts4300_psu.py` | Power supplies. |
| `src/ibm/agent_based/ts4300_drives.py` | Tape drives. |
| `src/ibm/agent_based/ts4300_slots.py` | Media slots and cleaning cartridges. |
| `src/ibm/agent_based/ts4300_lib.py` | Shared detection and CIM status maps. |
| `src/ibm/rulesets/` | Check parameters for drives, slots and cleaning cartridges. |
| `src/ibm/graphing/metrics.py` | Metrics, graph and perfometers. |
| `src/ibm/checkman/` | Check documentation. |
| `testdata/snmp_walk.txt` | Anonymized walk of a TS4300 used for testing. |

## Installation

1. Install the MKP on the Checkmk site.
2. Configure SNMP access to the tape library and add the host to the rule
   **Hosts without system description OID**.
3. Run service discovery.

## Parameters

- **IBM TS4300 tape drives** — state for a pending cleaning request (WARN by
  default) and optional levels on the total operating time.
- **IBM TS4300 media slots** — levels on the slot utilization. Storage slots are
  discovered with 90%/95%, the I/O station without levels, because cartridges
  waiting in the mail slot are normal on many sites.
- **IBM TS4300 cleaning cartridges** — lower levels on the number of cleaning
  cartridges, CRIT when none is left.
