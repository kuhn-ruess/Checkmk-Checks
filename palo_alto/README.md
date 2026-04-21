# Palo Alto enhanced checks

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p4-blue)
<!-- compatibility-badges:end -->

Consolidated SNMP checks for Palo Alto firewalls. This package replaces the
earlier separate `palo_alto_gp_tunnels` and `palo_alto_versions` MKPs (see
their READMEs), and adds the antivirus signature age check. All services
keep their existing identifiers, so migrating from the legacy packages does
not orphan services.

## Provided check plugins

| Check plugin | Service | Purpose |
| --- | --- | --- |
| `palo_alto_antivirus` | `Palo Alto antivirus version` | WARN/CRIT when the antivirus signature database has not been updated for longer than the configured age. |
| `palo_alto_gp_tunnels` | `Palo Alto GlobalProtect Tunnels` | WARN/CRIT when the remaining free GlobalProtect tunnel slots drop below the configured thresholds. |
| `palo_alto_threadid` | `Palo Alto TheadID Version` | Reports the current Threat content version (always OK, informational). |
| `palo_alto_urlfilter` | `Palo Alto URL-Filtering Version` | Reports the current URL-Filtering content version (always OK, informational). |

All four checks share the same detection: `sysDescr` must start with
`Palo Alto` and the Palo Alto sub-tree `.1.3.6.1.4.1.25461.2.1.2.5.1.*` must
exist.

## Rulesets

| Ruleset | Applies to | Default |
| --- | --- | --- |
| `Palo Alto antivirus age` (Applications) | `palo_alto_antivirus` | WARN 24h, CRIT ~29h |
| `Palo Alto GlobalProtect tunnels` (Applications) | `palo_alto_gp_tunnels` | WARN 50 free slots, CRIT 15 free slots |

## Package contents

| Path | Purpose |
| --- | --- |
| `src/palo_alto/agent_based/antivirus.py` | `palo_alto_antivirus` section + check. |
| `src/palo_alto/agent_based/gp_tunnels.py` | `palo_alto_gp_tunnels` section + check. |
| `src/palo_alto/agent_based/threadid.py` | `palo_alto_threadid` section + check. |
| `src/palo_alto/agent_based/urlfilter.py` | `palo_alto_urlfilter` section + check. |
| `src/palo_alto/rulesets/antivirus.py` | WATO ruleset for antivirus age. |
| `src/palo_alto/rulesets/gp_tunnels.py` | WATO ruleset for GlobalProtect tunnel levels. |

## Installation

1. Uninstall any previously installed `palo_alto_gp_tunnels` and
   `palo_alto_versions` MKPs.
2. Install this MKP on the Checkmk site.
3. Add the Palo Alto firewall as an SNMP host and run service discovery.

## Known limitations

- The antivirus "age" is measured from the first time the plugin sees a
  given version string, not from the actual last update on the firewall.
- The service name for the Threat content version is kept as the historical
  typo `TheadID Version` so existing services stay intact.
