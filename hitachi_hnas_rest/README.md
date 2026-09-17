# Hitachi HNAS via REST API

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0-2f4f4f) ![packaged](https://img.shields.io/badge/packaged-2.4.0p18-blue)
<!-- compatibility-badges:end -->

Special agent based monitoring of Hitachi NAS (HNAS) systems using the
NAS File Storage REST API (v8, TCP port 8444).

Replaces a legacy Nagios plugin (`nagiosplugin` based) with a native
Checkmk plugin.

## Monitored components

| Service | Source | Description |
|---|---|---|
| HNAS Filesystem | `/v8/storage/filesystems` | Space usage (levels, default 80%/90%), thin provisioning state, mount status |
| HNAS Snapshots | `/v8/storage/filesystems/{id}/snapshots` | Snapshot count, age of oldest snapshot, time since last snapshot |
| HNAS Storage Pool | `/v8/storage/storage-pools` | Space usage (levels, default 80%/90%), health state |
| HNAS EVS | `/v8/storage/virtual-servers` | Virtual server status (ONLINE/DISABLED/OFFLINE/NOT_CONFIGURED) |
| HNAS Node | `/v8/storage/nodes` | Cluster node status, model, firmware, uptime |
| HNAS System Drive | `/v8/storage/system-drives` | System drive status, degraded state |

## Setup

1. Install the MKP.
2. Create an API key on the HNAS (`apikey-create`, recommended) or use
   an API user with password.
3. Configure the rule *Hitachi HNAS via REST API* under
   *Setup > Agents > Other integrations*.

Authentication is done either via the `X-Api-Key` header (recommended
by Hitachi) or via `X-Subsystem-User`/`X-Subsystem-Password` headers
for backward compatibility.
