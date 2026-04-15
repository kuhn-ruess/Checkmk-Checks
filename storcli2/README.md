# Raid controller monitoring via StorCLI2 tool

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p9-blue)
<!-- compatibility-badges:end -->

Monitors LSI / Broadcom RAID controllers on Windows hosts via the `StorCLI2.exe` utility. A PowerShell agent plugin runs `StorCLI2 /call show all`, splits the report into several sub-sections, and the check plugins evaluate tool status, firmware versions, enclosures, physical and virtual drives, chip/board temperature, and a generic key/value status check with a discovery filter.

## How it works

The agent plugin parses the single `StorCLI2 /call show all` output and rewrites section headers on the fly. Lines that look like `Section Name :` become `<<<storcli2_section_name>>>`, so a single tool run feeds multiple Checkmk sections:

| Section | Check | Service name |
| --- | --- | --- |
| `storcli2_tool` | `storcli2_tool` | `StorCli2 Tool` |
| `storcli2_version` | `storcli2_version` | `StorCli2 Version` |
| `storcli2_hwcfg` | `storcli2_temp` | `StorCli2 Temperature Chip` / `Board` |
| `storcli2_enclosure_list` | `storcli2_enclosure_list` | `StorCli2 Enclosure <EID>` |
| `storcli2_pd_list` | `storcli2_pd_list` | `StorCli2 PD <controller:slot>` |
| `storcli2_vd_list` | `storcli2_vd_list` | `StorCli2 VD <id>` |
| `storcli2_status` | `storcli2_status` | `StorCli2 Status` |

Two parsing helpers in `src/storcli2/agent_based/utils/storcli2.py` handle key-value `a = b` blocks (`parse_storcli2_list`) and dashed column tables (`parse_storcli2_table`).

## Package contents

| Path | Purpose |
| --- | --- |
| `src/agents/windows/plugins/storcli2.ps1` | PowerShell agent plugin that calls `StorCLI2.exe` and rewrites its output into Checkmk sections. |
| `src/lib/check_mk/base/cee/plugins/bakery/storcli2.py` | Bakery hook that deploys the plugin and a `storcli2.ps1` config snippet with `$STORCLI2_PATH`. |
| `src/storcli2/rulesets/bakery_storcli2.py` | WATO `AgentConfig` rule for the bakery (activate + path to `storCLI2.exe`). |
| `src/storcli2/rulesets/status.py` | `DiscoveryParameters` rule for filtering status keys (wildcard `*` at end supported). |
| `src/storcli2/agent_based/tool.py` | Tool/CLI status check. |
| `src/storcli2/agent_based/version.py` | Firmware / package / driver version check. |
| `src/storcli2/agent_based/temp.py` | Chip and board temperature check (uses `cmk.plugins.lib.temperature`, default 50/60 C). |
| `src/storcli2/agent_based/enclosure_list.py` | Per-enclosure state, ProdID, alarm count. |
| `src/storcli2/agent_based/pd_list.py` | Physical drive check; CRIT if `State != Conf`, `Status != Online`, or `Sp != U`. |
| `src/storcli2/agent_based/vd_list.py` | Virtual drive check; CRIT if `State != Optl` or `Access != RW`. |
| `src/storcli2/agent_based/status.py` | Generic key/value status check that locks in the values seen at discovery time. |
| `src/storcli2/agent_based/utils/storcli2.py` | Shared parsers. |

## Installation

1. Install the MKP on the Checkmk site.
2. Install `StorCLI2.exe` on the Windows target host.
3. Deploy the agent plugin:
   - **With Bakery:** enable **LSI Raid Controller Status 2 (via StorCLI2)** (topic *Operating System*), set the path to `storCLI2.exe` if it is not in the default location, and bake the agent.
   - **Without Bakery:** copy `storcli2.ps1` into the Windows agent `plugins` directory and create `storcli2.ps1` in the agent config directory setting `$STORCLI2_PATH` to the absolute path of `StorCLI2.exe`.
4. Run service discovery on the host.

## Configuration

| Rule | Form | Purpose |
| --- | --- | --- |
| Agent rules > *LSI Raid Controller Status 2 (via StorCLI2)* | `activate`, `path` | Bakery deployment and path override. |
| Discovery parameters > *StorCli2 Status discovery* | `filters` (list of strings, wildcard `*` suffix) | Keys from the status section to skip at discovery. |
| Service monitoring rules > *Temperature* | standard temperature levels | Used by `storcli2_temp` (default 50/60 C). |

## Services & metrics

- `StorCli2 Tool` reports CLI version, controller and status; UNKNOWN on `ERROR` lines from the agent.
- `StorCli2 Version` reports firmware, package and driver versions.
- `StorCli2 Temperature Chip` / `Board` use the standard temperature check, metric `temp`.
- `StorCli2 Enclosure <EID>` reports state, ProdID and alarm count; CRIT when `Alms > 0`.
- `StorCli2 PD <controller:slot>` — if only one controller is present the item is just the slot.
- `StorCli2 VD <id>` reports all VD attributes; CRIT on non-optimal state or non-RW access.
- `StorCli2 Status` locks the key/value pairs seen at discovery and goes CRIT on any drift.

## Known limitations

- The agent plugin is Windows-only.
- `StorCli2 Status` has no tolerance: any value change versus discovery time becomes CRIT; use the discovery filter to exclude noisy keys.
- Temperature levels are hardcoded defaults (50/60 C) unless overridden via the standard *Temperature* ruleset.
