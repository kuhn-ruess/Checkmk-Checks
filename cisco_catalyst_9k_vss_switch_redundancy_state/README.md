# Cisco Catalyst 9k VSS switch redundancy state

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.0.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.0.0p20-blue)
<!-- compatibility-badges:end -->

Monitors the StackWise Virtual (VSS) redundancy state on Cisco Catalyst 9000 series switches. One service per member switch reports the current switch role (master / member / standby / not member) and the switch state (ready, waiting, mismatches, etc.).

## How it works

SNMP section `cisco_catalyst_9k_vss_switch_redundancy_state` walks `CISCO-STACKWISE-MIB` under `.1.3.6.1.4.1.9.9.500.1.2.1.1` and collects:

- `cswSwitchNumCurrent` (`.1`) — switch number (used as item)
- `cswSwitchRole` (`.3`) — 1=master, 2=member, 3=not member, 4=standby
- `cswSwitchState` (`.6`) — 1..11, where 4 is `ready`

Detection matches sysObjectID starting with `.1.3.6.1.4.1.9.1.2871`. Any state other than `ready` yields CRIT. A mismatch between the expected and actual switch role also yields CRIT.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/base/plugins/agent_based/cisco_catalyst_9k_vss_switch_redundancy_state.py` | SNMP section, discovery and check plugin. |
| `src/web/plugins/wato/cisco_catalyst_9k_vss_switch_redundancy_state.py` | Legacy WATO rule to pin the expected switch role. |

## Installation

1. Install the MKP on the Checkmk site.
2. Run SNMP service discovery on a Catalyst 9000 switch. One service `State Switch <n>` is created per member.

## Configuration

Rule: **Parameters for discovered services -> Networking -> Cisco Catalyst 9k redundancy State**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `switch_role` | Dropdown (`1`..`4`) | Expected role for this switch number; CRIT if the current role differs. |

## Services & metrics

- **Service:** `State Switch <switch_number>` — one per stack member.
- **State logic:** CRIT on unexpected role or any switch state other than `ready`.
- No metrics.

## Known limitations

- The WATO file uses the legacy pre-2.3 rulespec API (`rulespec_registry.register` / `CheckParameterRulespecWithItem`). References `TextAscii` without importing it, which will fail on sites where that symbol is no longer auto-loaded.
