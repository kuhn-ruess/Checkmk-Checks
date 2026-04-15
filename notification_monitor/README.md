# Monitor Failed Notifications

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p8-blue)
<!-- compatibility-badges:end -->

A special agent that queries the Checkmk notification log via the
built-in "failed_notifications" view and raises a Checkmk service if
any notification command matching a configurable regex has failed in
the last 15 minutes. Useful for catching broken ticket-creation or
SMS-gateway notification scripts where the original failure would
otherwise go unnoticed.

## How it works

1. `agent_notification_monitor` reads the local automation secret from
   `$OMD_ROOT/var/check_mk/web/automation/automation.secret` and calls
   `check_mk/view.py?view_name=failed_notifications` on the configured
   Checkmk site URL, filtering on `log_type=.*NOTIFICATION RESULT$`,
   `logclass3=on` (failed) and `log_command_name_regex=<regex>`.
2. The number of matching failures is printed as a `<<<local>>>`
   section: OK when zero, CRIT when one or more.

```text
<<<local>>>
0 "Failed Notifications" count=0 0 failed
```

## Package contents

| Path | Purpose |
| --- | --- |
| `src/notification_monitor/libexec/agent_notification_monitor` | Special agent script (Python, uses `requests`). |
| `src/notification_monitor/server_side_calls/special_agent.py` | `SpecialAgentConfig` — passes `timeout`, `path`, `command_regex` as positional args. |
| `src/notification_monitor/rulesets/sepcial_agent.py` | `SpecialAgent` ruleset `notification_monitor`. |

## Installation

1. Install the MKP on the Checkmk site.
2. Create a host to run the check on (typically the Checkmk server
   itself) and configure a rule *Setup -> Agents -> Other integrations
   -> Notification Monitor*.
3. The resulting local service is named `Failed Notifications`.

## Configuration

Ruleset: `notification_monitor`

| Parameter | Type | Meaning |
| --- | --- | --- |
| `path` | String | Base URL of the central Checkmk site, e.g. `https://server/site/`. Required so the plugin can run on a remote site. |
| `command_regex` | String | Regex matched against the notification command name (as shown in the Checkmk notification setup). |
| `timeout` | TimeSpan | HTTP request timeout (default 2.5 s). |

## Known limitations

- The special agent reads the `automation` user's secret from disk; it
  must run on a site that has an `automation` user configured.
- Look-back window is hardcoded to 15 minutes (`from_hour=1`,
  `logtime_from_range = from_hour * 900`).
