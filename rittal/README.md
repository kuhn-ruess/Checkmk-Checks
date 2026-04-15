# Rittal LCP Monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-1.1.10-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-1.1.10-blue)
<!-- compatibility-badges:end -->

SNMP-based monitoring of Rittal LCP (Liquid Cooling Package) rack cooling units via the Rittal CMC-TC enterprise MIB. One Checkmk service is created per supported sensor (blowers, server in/out temperatures, water in/out temperatures, water flow, blower grade, regulator).

## How it works

The check walks the Rittal CMC-TC sensor table under `.1.3.6.1.4.1.2606.4.2` and collects index, sensor type, status, value and description. Only sensor types that appear in an internal template table are discovered, which covers:

- Blowers 1-6 (RPM)
- LCP Server in/out 1-3 (temperature)
- LCP Overview Server in/out (temperature)
- LCP Overview Water in/out (temperature)
- LCP Overview Water flow (l/min)
- LCP Overview Blower Grade
- LCP Overview Regulator (percent)

Sensor state `4` is mapped to OK, `7` to WARN, everything else to CRIT; unknown sensors return UNKNOWN. Detection triggers when the system description (`.1.3.6.1.2.1.1.1.0`) contains `CMC-TC`.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/checks/rittal_lcp` | Legacy check script: SNMP section, inventory, check function and perf-data mapping. |
| `src/checkman/rittal_lcp` | Check manual page. |
| `src/web/plugins/perfometer/rittal_lcp.py` | Perf-o-meter definition. |

## Installation

1. Install the MKP on the Checkmk site.
2. Add the Rittal LCP as an SNMP host. The check self-detects via the `CMC-TC` string in `sysDescr`.
3. Run service discovery.

## Known limitations

- Uses the legacy pre-2.0 check API (`check_info`, `snmp_info`, `snmp_scan_functions`) and will need porting to `cmk.agent_based.v2` on newer Checkmk versions where that API is removed.
- No WATO parameters: thresholds come from the device itself via the sensor status field.
- Service items embed the raw SNMP OID suffix (`<sensor> - <oid>`), which is kept for compatibility with existing installations.
