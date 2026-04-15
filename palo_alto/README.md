# Palo Alto enhanced checks

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p4-blue)
<!-- compatibility-badges:end -->

Additional SNMP checks for Palo Alto firewalls. Currently ships one check
that monitors the age of the antivirus signature database and warns when
the signatures have not been updated for a configurable amount of time.

## How it works

SNMP section `palo_alto_antivirus` fetches the current antivirus version
string from OID `.1.3.6.1.4.1.25461.2.1.2.1.8`. Detection requires the
sysDescr to start with `Palo Alto` and the Palo Alto sub-tree
`.1.3.6.1.4.1.25461.2.1.2.5.1.*` to exist.

The check compares the current version string against the last one seen
(persisted in the value store). Whenever the string changes, the
`last_update` timestamp is refreshed. The service goes WARN/CRIT if the
time since the last observed change exceeds the configured levels.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/palo_alto/agent_based/antivirus.py` | SNMP section and check plugin `palo_alto_antivirus`. |
| `src/palo_alto/rulesets/antivirus.py` | WATO ruleset `palo_alto_antivirus` for the maximum update age. |

## Installation

1. Install the MKP on the Checkmk site.
2. Add the Palo Alto firewall as an SNMP host. The section is auto-detected
   from the Palo Alto sysDescr; run service discovery to pick up the
   service `Palo Alto antivirus version`.

## Configuration

Rule: **Service monitoring rules -> Applications -> Palo Alto antivirus age**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `age` | Upper `SimpleLevels` on time span (days/hours) | WARN/CRIT when the antivirus signature version has not changed for longer than this. Default: 86400 s / 104400 s. |

## Services & metrics

- **Service:** `Palo Alto antivirus version`
- **Summary:** current antivirus version string, plus WARN/CRIT text
  `No Updates for the last <timespan>` when the configured age is exceeded.
- **State logic:** OK while within levels, WARN above warn level, CRIT
  above crit level.

## Known limitations

- The "age" is measured from the moment the plugin first sees a given
  version, not from the actual last update on the firewall. Freshly added
  hosts will therefore not produce a meaningful WARN/CRIT until a full
  age window has passed.
