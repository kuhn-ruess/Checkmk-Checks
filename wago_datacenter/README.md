# WAGO Datacenter Signals

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p24-blue)
<!-- compatibility-badges:end -->

SNMP check for WAGO PFC200 controllers used as datacenter signal gateways. Reads a table of free-form signal strings from the WAGO PLC data write area and produces one Checkmk service per signal, with OK/CRIT driven by the first word of the payload.

## How it works

- Detection: `sysObjectID` starts with `.1.3.6.1.4.1.13576` (WAGO enterprise OID).
- Fetches the table under `.1.3.6.1.4.1.13576.10.1.100.1.1` using `OIDEnd()` as the table index and column `3` (`wioPlcDataWriteArea`) as the value.
- Indices `1`, `2`, `3` are treated as device info (ASP name, device name, company) and skipped from service discovery.
- All remaining indices become services named `DC Signal <index> <description>`. The index is preserved in the item because several entries can share the same description in their OK state (e.g. `.15/.16/.17` all showing `Notstrom`).
- The check splits the value on the first space: the first token is the status word. If it equals `OK` the service is OK, otherwise CRIT. The full payload is shown in the summary, the ASP/device name is added as details.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/wago_datacenter/agent_based/wago_datacenter.py` | SNMP section, parser, discovery and check plugin. |
| `testdata/wago-dc-walk.txt` | Reference SNMP walk used for development. |

## Installation

1. Install the MKP on the Checkmk site.
2. Add the PFC200 controller as an SNMP host; the detection rule fires automatically for devices under the WAGO enterprise OID.
3. Run service discovery; one `DC Signal ...` service is created per non-info table row.

## Services

- **Service:** `DC Signal <index> <description>`
- **State logic:** OK if the first word of the SNMP payload is `OK`, otherwise CRIT.
- **Summary:** full raw payload from the PLC.
- **Details:** ASP name / device name from indices 1-2.
