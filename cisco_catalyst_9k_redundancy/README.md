# Cisco Catalyst 9K Redundancy check

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.0.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.0.0p20-blue)
<!-- compatibility-badges:end -->

SNMP check that verifies whether a Cisco Catalyst 9000 StackWise stack forms a redundant ring. A single service `Stack Ring Redundancy` is created on matching devices.

## How it works

The plugin [`cisco_catalyst_9k_redundancy.py`](src/base/plugins/agent_based/cisco_catalyst_9k_redundancy.py) registers an SNMP section whose detection requires `sysObjectID` to start with `.1.3.6.1.4.1.9.1.2871`. It fetches `CISCO-STACKWISE-MIB::cswRingRedundant` (`.1.3.6.1.4.1.9.9.500.1.1.3`), a TruthValue where:

- `1` (true): OK, "Stackports form a redundant ring"
- `2` (false): CRIT, "Stackports do not form a redundant ring"

## Package contents

| Path | Purpose |
| --- | --- |
| `src/base/plugins/agent_based/cisco_catalyst_9k_redundancy.py` | SNMP section and check plugin. |

## Installation

1. Install the MKP on the Checkmk site.
2. Ensure SNMP access to the Catalyst 9K device is configured; run service discovery.

## Services & metrics

- **Service:** `Stack Ring Redundancy` (single)
- **State logic:** OK when the ring is redundant, CRIT otherwise.
- **Metrics:** none.

## Known limitations

- Uses the legacy `agent_based_api.v1` import style and `register.*` functions; still supported on 2.3 / 2.4 but would need porting to `cmk.agent_based.v2` if that API is dropped.
- Detection is pinned to one exact `sysObjectID` prefix (`cat9300` / `cat9500` family); other Catalyst models with StackWise are not matched.
