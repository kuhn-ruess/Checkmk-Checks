# Cisco Portsecurity Status

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p18-blue)
<!-- compatibility-badges:end -->

Reports on Cisco switches whether any administratively up port has Port Security disabled. A single service `Port Security Status` is created per device; it goes WARN when at least one non-excluded port has port security turned off.

## How it works

The SNMP section `cisco_portsec` joins two SNMP trees:

- `.1.3.6.1.2.1.2.2.1` / `.1.3.6.1.2.1.31.1.1.1.18` — port name, ifAdminStatus, alias
- `.1.3.6.1.4.1.9.9.315.1.2.1.1` (`CISCO-PORT-SECURITY-MIB::cpsIfConfigTable`) — `cpsIfPortSecurityEnable` (1=yes, 2=no), operational status, violation count, last MAC

Detection requires a sysDescr containing `cisco` and that the port security table exists. Administratively down ports (`ifAdminStatus == 2`) and any interface whose name or alias matches the exception list are skipped.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/cisco_portsec/agent_based/cisco_portsec.py` | SNMP section and check plugin. |
| `src/cisco_portsec/rulesets/agent.py` | Check parameters ruleset (exception list). |

## Installation

1. Install the MKP on the Checkmk site.
2. Run service discovery on a Cisco switch host. The service `Port Security Status` appears on devices where the port security table has entries.

## Configuration

Rule: **Parameters for discovered services -> Networking -> Cisco Portsecurity Status**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `exceptions` | List of strings | Interface names or alias prefixes that must not be checked. Alias matching uses `startswith`. |

## Services & metrics

- **Service:** `Port Security Status` — one per host.
- **State logic:** WARN if any port that is up and not excluded has port security disabled, UNKNOWN if the enable state cannot be parsed, otherwise OK.
