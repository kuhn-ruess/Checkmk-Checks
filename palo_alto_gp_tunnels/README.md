# PaloAlto Globalprotect Tunnels

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.0.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.0.0p20-blue)
<!-- compatibility-badges:end -->

SNMP check for Palo Alto GlobalProtect gateways. Reports how many
GlobalProtect VPN tunnels are currently active compared to the configured
maximum on the device.

## How it works

SNMP section `palo_alto_gp_tunnels` fetches from
`.1.3.6.1.4.1.25461.2.1.2.5.1`:

- `.3` - active tunnels
- `.2` - maximum tunnels

Detection requires sysDescr to start with `Palo Alto` and the sub-tree
`.1.3.6.1.4.1.25461.2.1.2.5.1.*` to exist. The check emits the metric
`active_gp_tunnels` (with upper boundary = max tunnels) and applies
hardcoded thresholds:

- CRIT when `active >= max - 15`
- WARN when `active >= max - 50`
- OK otherwise

## Package contents

| Path | Purpose |
| --- | --- |
| `src/base/plugins/agent_based/palo_alto_gp_tunnels.py` | SNMP section and check plugin `palo_alto_gp_tunnels`. |

## Installation

1. Install the MKP on the Checkmk site.
2. Add the Palo Alto GlobalProtect gateway as an SNMP host and run service
   discovery to create the service `Palo Alto GlobalProtect Tunnels`.

## Services & metrics

- **Service:** `Palo Alto GlobalProtect Tunnels`
- **Metric:** `active_gp_tunnels` with boundary `(0, max_tunnels)`.
- **State logic:** hardcoded proximity thresholds relative to the
  device-reported maximum (WARN 50 below, CRIT 15 below the maximum).

## Known limitations

- The WARN/CRIT thresholds are hardcoded and cannot be configured via
  WATO.
- Uses the legacy `register.*` agent-based API and therefore the
  `min_required` is still 2.0.0 — verify on newer Checkmk releases.
