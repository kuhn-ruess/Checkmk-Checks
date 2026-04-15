# Open-iSCSI session and iSOE host checks

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-1.6.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-1.6.0-blue)
<!-- compatibility-badges:end -->

Monitors Open-iSCSI sessions and iSOE (iSCSI offload engine) hosts on
Linux initiators. Built on the work of Frank Fegert
(<https://github.com/frank-fegert/check_mk/>), refactored and extended
with Agent Bakery support.

Three check plugins are provided:

- **Session status** — tracks the state of each iSCSI session vs. the
  state discovered at inventory time.
- **Session statistics** — per-session counters for software and
  dependent-hardware initiators (e.g. `bnx2i`).
- **Host statistics** — aggregated host counters for QLogic `qla4xxx`
  iSOE initiators, which do not expose per-session statistics.

## How it works

The agent plugin `open-iscsi` runs `iscsiadm -m session -P 1` to
enumerate active sessions and `iscsiadm -m session -r <sid> -s` to
collect per-session statistics. For QLogic `qla4xxx` hosts it also
runs `iscsiadm -m host -H <hst> -C stats`. Output is emitted under
three sections:

```text
<<<open-iscsi_sessions>>>
qla4xxx 10.0.0.4:3260,1 iqn.2001-05.com.equallogic:0-fe83b6-... ... LOGGED_IN ...

<<<open-iscsi_session_stats>>>
[session stats d0:43:1e:51:98:c8 iqn.2001-05.com.equallogic:0-fe83b6-...]
txdata_octets: 337207169024
...

<<<open-iscsi_host_stats>>>
[host stats 84:8f:69:35:fc:70 iqn.2000-04.com.qlogic:...]
mactx_frames: 2920663232
...
```

## Package contents

| Path | Purpose |
| --- | --- |
| `src/agents/plugins/open-iscsi` | Bash agent plugin (`iscsiadm` wrapper). |
| `src/agents/bakery/open-iscsi` | Agent Bakery hook. |
| `src/checks/open-iscsi_sessions` | Session status check. |
| `src/checks/open-iscsi_session_stats` | Per-session PDU and byte counters. |
| `src/checks/open-iscsi_host_stats` | QLogic `qla4xxx` host counters (MAC/IP/TCP/iSCSI). |
| `src/web/plugins/wato/open-iscsi.py` | Bakery deployment rule. |
| `src/web/plugins/wato/open-iscsi_session_stats.py` | Threshold ruleset. |
| `src/web/plugins/wato/open-iscsi_host_stats.py` | Threshold ruleset. |
| `src/web/plugins/perfometer/*.py` | Perfometer definitions. |
| `src/checkman/*` | Check manual pages. |

## Installation

1. Install the MKP on the Checkmk site.
2. Deploy the agent plugin via the Bakery (rule *Open-iSCSI*) or by
   copying `src/agents/plugins/open-iscsi` to
   `/usr/lib/check_mk_agent/plugins/` on each initiator and making it
   executable. `iscsiadm`, `egrep`, `sed` and `tr` must be available.
3. Run service discovery.

## Services & metrics

- `iSCSI Session Status <iface> / <target>` — OK when
  session/connection/internal state is `LOGGED_IN/LOGGED_IN/NO_CHANGE`
  (or just `LOGGED_IN` for hardware initiators that do not expose
  connection state).
- `iSCSI Session Stats <mac> <target>` — 21 per-session PDU and byte
  counters as metrics, rx/tx octets shown as human-readable rate in
  the summary line.
- `iSCSI Host Stats <mac> <iqn>` — full MAC/IP/IPv6/TCP/iSCSI counter
  set for QLogic `qla4xxx` hosts.

## Known limitations

- Uses the legacy `check_info` / `factory_settings` API and the legacy
  WATO `register_check_parameters` API — no port to the v2 APIs yet.
- Per-session statistics are only available for software initiators
  and dependent-hardware initiators (e.g. `bnx2i`); QLogic `qla4xxx`
  ("flashnode") sessions only produce host-level statistics.
- Default thresholds in both stats checks are `(0, 0)` for every
  counter, i.e. disabled — levels must be set explicitly via WATO to
  alert on anything.
