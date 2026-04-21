# Cisco stack extras

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p4-blue)
<!-- compatibility-badges:end -->

Consolidated add-on checks for Cisco StackWise / Catalyst stacks. Everything
here covers scenarios that the Checkmk core does **not** ship a plugin for.
Checks previously covered by the standalone packages
`catalyst_switch_state`, `cisco_distr_stack_port` and the now obsolete
`cisco_ip_sla` custom plugin are covered here, except for `cisco_ip_sla`
which Checkmk 2.4 ships natively — install no custom package for that one.

> **Not included / removed:** `cisco_redundancy` and `cisco_stackwise` were
> removed from this MKP because Checkmk 2.4 ships `cisco_redundancy` and
> `cisco_stack` with equivalent functionality. If you had services from the
> old `cisco 2.0.0` package, rediscover after migrating to 2.4 — the
> built-in checks take over automatically.

## Provided check plugins

| Check plugin | Service | Purpose |
| --- | --- | --- |
| `cisco_stackring` | `Stackring` | CRIT when a StackWise ring is not redundant (>= 2 members). |
| `catalyst_switch_state` | `State Switch <n>` | Per-switch role + state for Catalyst 9500X-class stacks (sysObjectID `.1.3.6.1.4.1.9.1.2871`) that the built-in `cisco_stack` does not detect. |
| `cisco_distr_stack_port` | `Distributed stack port status <port>` | Operational status of distributed stack ports including the neighbor side. |

## Rulesets

| Ruleset | Applies to | Purpose |
| --- | --- | --- |
| `Catalyst Switch State` (Networking) | `catalyst_switch_state` | Pin the expected switch role (`master`, `member`, `not_member`, `standby`). |

## Package contents

| Path | Purpose |
| --- | --- |
| `src/cisco/agent_based/stackring.py` | `cisco_stackring` section + check. |
| `src/cisco/agent_based/catalyst_switch_state.py` | `catalyst_switch_state` section + check. |
| `src/cisco/agent_based/distr_stack_port.py` | `cisco_distr_stack_port` section + check. |
| `src/cisco/rulesets/catalyst_switch_state.py` | WATO ruleset for the expected switch role. |
| `src/checkman/cisco_stackring` | Check manpage. |

## Installation

1. If a previous `cisco_ip_sla` / `catalyst_switch_state` /
   `cisco_distr_stack_port` MKP is installed, uninstall it.
2. Install this MKP on the Checkmk site (>= 2.4).
3. Run service discovery on the Cisco SNMP hosts.
