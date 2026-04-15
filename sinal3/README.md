# SINA device monitoring K+R Updated

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.0.0p1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0-blue)
<!-- compatibility-badges:end -->

SNMP monitoring for secunet SINA L3 boxes. Originally written by Christian Michaelski (CONET Solutions GmbH); this package is the Kuhn & Rueß fork ported to `cmk.agent_based.v2`. A single `sinal3` SNMP section feeds 15 check plugins covering temperatures, fans, voltages, HSB system state, software/config/ACL versions, box type, serial, NTP, IPsec, IKE-SA and policy counters.

## How it works

The `sinal3` section walks 13 SNMP subtrees under the UCD sensors MIB (`.1.3.6.1.4.1.2021.13.16.*`) for environmental data and the secunet enterprise MIB (`.1.3.6.1.4.1.8299.4.3.*`) for SINA-specific state. Detection triggers if either `.1.3.6.1.4.1.2021.4.5.0` or `.1.3.6.1.4.1.8299.4.3.1.1.0` exists.

| Check plugin | Service | What it reports |
| --- | --- | --- |
| `sinal3_system` | `System` | HSB mode / state of this box and its peer. WARN when peer indicates an error. |
| `sinal3_mgmt` | `Software Versions` | Main / fallback slot; WARN on mismatch. SRSU state mapped via `WARN_TBL` (e.g. `NOVUS_UPDATE_ERROR` -> CRIT). |
| `sinal3_fans` | `Fan <name>` | Uses `cmk.plugins.lib.fan.check_fan` with the `hw_fans` ruleset. |
| `sinal3_temp` | `Temperature <name>` | Uses `check_temperature` with the `temperature` ruleset. Raw values in milli-degrees, divided by 1000. |
| `sinal3_volts` | `Voltage <name>` | Millivolts / 1000; configurable upper/lower levels via the `voltage` ruleset. |
| `sinal3_gstat` | `Global status` | WARN if the global status int != 8. |
| `sinal3_config` | `Config versions` | Compares active vs. system-CFS vs. smartcard config. |
| `sinal3_aclvers` | `ACL versions` | WARN when active ACL differs from smartcard ACL. |
| `sinal3_vers` | `Version` | Running software version. |
| `sinal3_serial` | `Serial` | Box serial. |
| `sinal3_box` | `Box type` | Box hardware type. |
| `sinal3_ntp` | `NTP` | State mapped via `NSTATE`; WARN for `START`/`INIT`, CRIT above `SYNC`. |
| `sinal3_policycnt` | `Policy count` | Enabled/configured policy counts as metrics. |
| `sinal3_ipsec` | `IPsec phase one childs` / `phase two childs` / `peer count` / `connection count` | Counters with dedicated metrics (`count_one`, `count_two`, `count_peer`, `count_con`). |
| `sinal3_ike_sa` | `Active IKE-SA` | Number of established IKE security associations. |

## Package contents

| Path | Purpose |
| --- | --- |
| `src/sinal3/agent_based/sinal3.py` | SNMP section and all 15 check plugins. |
| `src/sinal3/checkman/sinal3_*` | Check manual pages for each plugin. |

## Installation

1. Install the MKP on the Checkmk site.
2. Add the SINA L3 device as an SNMP host. Detection is automatic based on the OIDs listed above.
3. Run service discovery. The exact set of services depends on which subtrees the device exposes.

## Configuration

The plugins reuse the following built-in WATO rulesets instead of defining their own:

| Plugin | Ruleset |
| --- | --- |
| `sinal3_fans` | `hw_fans` |
| `sinal3_temp` | `temperature` |
| `sinal3_volts` | `voltage` |

All other checks only expose default parameters.

## Known limitations

- State mappings for `NTP`, `HSB` and `SRSU` are hardcoded; adding new values requires a code change.
- The `Policy count` service displays the enabled count twice in its summary (`enabled: <ev>; configured: <ev>`); the metric for configured policies is still exported correctly.
- The serial and box-type services parse values using `str.strip()` on the raw SNMP response and assume single-line strings.
