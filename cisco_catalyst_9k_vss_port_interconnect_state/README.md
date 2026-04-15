# Cisco Catalyst 9K VSS Port Interconnect State

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.0.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.0.0p20-blue)
<!-- compatibility-badges:end -->

SNMP check for the StackWise Virtual Link (SVL) physical ports on Cisco Catalyst 9000 series switches. Creates one service per SVL port and reports its operational status, plus the operational status of the neighbor port.

See the [Cisco StackWise Virtual whitepaper](https://www.cisco.com/c/en/us/products/collateral/switches/catalyst-9000/nb-06-cat-9k-stack-wp-cte-en.html) for background.

## How it works

The plugin [`cisco_catalyst_9k_vss_port_interconnect_state.py`](src/base/plugins/agent_based/cisco_catalyst_9k_vss_port_interconnect_state.py) registers an SNMP section `cisco_distr_stack_port` whose detection requires `sysObjectID` to start with `.1.3.6.1.4.1.9.1.2871`. It walks `.1.3.6.1.4.1.9.9.500.1.2.4.1`:

- `.1` `cswDistrStackPhyPort` — port identifier
- `.2` `cswDistrStackPhyPortOperStatus` — port operational state (`1` up, `2` down)
- `.3` `cswDistrStackPhyPortNbr` — neighbor port identifier

One service is discovered per physical SVL port. The check reports OK on `up` and CRIT on `down`, for both the local port and any rows where the neighbor port matches the item.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/base/plugins/agent_based/cisco_catalyst_9k_vss_port_interconnect_state.py` | SNMP section, discovery and check. |

## Installation

1. Install the MKP on the Checkmk site.
2. Ensure SNMP access to the Catalyst 9K device is configured; run service discovery.

## Services & metrics

- **Service:** `Distributed stack port status %s` — one per SVL port.
- **State logic:** OK when the port (and its neighbor row when present) is up, CRIT when down.
- **Metrics:** none.

## Known limitations

- Uses the legacy `agent_based_api.v1` import style and `register.*` functions.
- Detection is pinned to one exact `sysObjectID` prefix (`.1.3.6.1.4.1.9.1.2871`); other Catalyst models are not matched even if they expose `CISCO-STACKWISE-MIB`.
