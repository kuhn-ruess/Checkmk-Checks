# Net Backup Checks

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-1.6.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.2.0p16-blue)
<!-- compatibility-badges:end -->

Monitors the status of tape drives / devices managed by Veritas
NetBackup on the media server by parsing `vmoprcmd` output. One service
per NetBackup device is created and goes CRIT if any drive on that
device reports a status other than `SCAN-TLD`, `TLD` or `ACTIVE`.

## How it works

The agent plugin runs `/usr/openv/volmgr/bin/vmoprcmd` on the media
server and prints its output under the `<<<net_backup>>>` section. The
legacy check plugin parses the `Host / DrivePath / Status` table,
groups rows by device, and reports client, path and status for each
drive.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/agents/plugins/net_backup.sh` | Bash agent plugin (runs `vmoprcmd`). |
| `src/agents/bakery/net_backup` | Agent Bakery hook. |
| `src/checks/net_backup` | Legacy check plugin (`check_info["net_backup"]`). |
| `src/web/plugins/wato/net_backup.py` | WATO rule `agent_config:net_backup` for the Bakery. |

## Installation

1. Install the MKP on the Checkmk site.
2. Deploy the agent plugin:
   - **With Bakery:** enable the rule *Netbackup Monitoring (Linux)*
     and bake the agent.
   - **Manually:** copy `src/agents/plugins/net_backup.sh` to
     `/usr/lib/check_mk_agent/plugins/` on the NetBackup media server
     and make it executable. `/usr/openv/volmgr/bin/vmoprcmd` must be
     runnable by the Checkmk agent user.
3. Run service discovery.

## Services & metrics

- **Service:** `Device <device>` (one per NetBackup device).
- **State logic:** CRIT if any drive on the device has a status other
  than `SCAN-TLD`, `TLD` or `ACTIVE`, otherwise OK. No metrics.

## Known limitations

- Uses the legacy `check_info` API and the legacy `register_rule` WATO
  API. Functional on Checkmk 2.x as long as the legacy APIs are
  available.
