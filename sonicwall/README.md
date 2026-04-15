# Sonicwall VPN Monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0p1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p8-blue)
<!-- compatibility-badges:end -->

SNMP-based monitoring of SonicWall firewalls. Covers CPU and memory utilization, current connection usage, and per-VPN security association status with encryption/decryption byte rates.

## How it works

All sections detect SonicWall devices via `sysDescr` containing `sonicwall` and fetch data from the SonicWall enterprise MIB under `.1.3.6.1.4.1.8741.1.3`.

| Section | Base OID | Purpose |
| --- | --- | --- |
| `sonicwall_cpu` | `.1.3.6.1.4.1.8741.1.3.1.3` | Current CPU utilization (%). |
| `sonicwall_mem` | `.1.3.6.1.4.1.8741.1.3.1.4` | Current memory utilization (%). |
| `sonicwall_conns` | `.1.3.6.1.4.1.8741.1.3.1` | Max and current firewall connections (percent used). |
| `sonicwall_vpn` | `.1.3.6.1.4.1.8741.1.3.2.1.1.1` | VPN security associations: name, peer IP, encrypted and decrypted byte counters. |

## Package contents

| Path | Purpose |
| --- | --- |
| `src/sonicwall/agent_based/sonicwall_cpu.py` | CPU section and check plugin. |
| `src/sonicwall/agent_based/sonicwall_mem.py` | Memory section and check plugin. |
| `src/sonicwall/agent_based/sonicwall_conns.py` | Connection usage section and check plugin. |
| `src/sonicwall/agent_based/sonicwall_vpn.py` | VPN SA section and check plugin. |

## Installation

1. Install the MKP on the Checkmk site.
2. Ensure SNMP is configured on the SonicWall and the Checkmk host uses SNMP.
3. Run service discovery; services are created automatically on any host whose `sysDescr` contains `sonicwall`.

## Services & metrics

| Service | Ruleset | Default levels | Metric |
| --- | --- | --- | --- |
| `CPU utilization` | `sonicwall_cpu` | 80 / 95 % | `cpu` |
| `Memory` | `sonicwall_mem` | 80 / 95 % | `memory` |
| `Connections <n>` | `sonicwall_conns` | 80 / 95 % | `connections` |
| `VPN - <name>` | (none) | — | `sa_bytes_encrypted`, `sa_bytes_decrypted` |

The VPN service reports the peer IP in the summary and emits per-second byte rates derived from the encrypted/decrypted counter OIDs.

## Known limitations

- No WATO ruleset files are shipped in the MKP; the CPU, memory and connection checks reference `check_ruleset_name` values (`sonicwall_cpu`, `sonicwall_mem`, `sonicwall_conns`) but the ruleset definitions themselves are not part of this package, so parameters can only be changed through the built-in defaults.
- The VPN check always reports state OK for a discovered SA; there is no tunnel up/down evaluation.
