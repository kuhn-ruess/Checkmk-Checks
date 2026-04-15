# Check for Palo Alto Versions

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.0.0p22-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.0.0p22-blue)
<!-- compatibility-badges:end -->

Two SNMP checks for Palo Alto firewalls that surface the currently
installed Threat (ThreatID) and URL-Filtering content versions as Checkmk
services. Both services are informational and always OK — they let you
track the rolled-out content version over time without any thresholds.

## How it works

Both checks use the same detection: sysDescr must start with `Palo Alto`
and the OID `.1.3.6.1.4.1.25461.2.1.2.5.1.*` must exist.

| Check | OID | Service |
| --- | --- | --- |
| `palo_alto_threadid` | `.1.3.6.1.4.1.25461.2.1.2.1.9` | `Palo Alto TheadID Version` |
| `palo_alto_urlfilter` | `.1.3.6.1.4.1.25461.2.1.2.1.10` | `Palo Alto URL-Filtering Version` |

Each check simply reports the string fetched from the OID as the service
summary. State is always OK.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/agent_based/palo_alto_threadid.py` | SNMP section and check plugin for the Threat content version. |
| `src/agent_based/palo_alto_urlfilter.py` | SNMP section and check plugin for the URL-Filtering content version. |

## Installation

1. Install the MKP on the Checkmk site.
2. Add the Palo Alto firewall as an SNMP host and run service discovery.
   Both services appear automatically if the device matches.

## Services & metrics

- `Palo Alto TheadID Version` - always OK, summary shows the Threat
  content version.
- `Palo Alto URL-Filtering Version` - always OK, summary shows the
  URL-Filtering version.

No metrics, no WATO parameters.

## Known limitations

- The service name for the Threat version is misspelled as
  `TheadID Version` (historical typo, kept for compatibility with existing
  service items).
- Uses the legacy `register.*` agent-based API.
