# EC Cleanup Script

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p13-blue)
<!-- compatibility-badges:end -->

Command-line helper for the Checkmk Event Console. When the EC is flooded with Checkmk-sourced events and the Notification Spooler cannot keep up delivering the OK follow-ups, this script finds all open EC events whose corresponding Checkmk host or service is already back to OK and archives them on demand.

## How it works

`sync_ec_events.py` is installed under `bin/` in the site and uses the Checkmk REST API (`/check_mk/api/1.0/`) with the local `automation` user (auto-detected from `~/var/check_mk/web/automation/automation.secret`) unless credentials are passed explicitly.

1. List open EC events filtered by the given `event_rule_id`.
2. For each event, query the matching service (or host, if `application == "HOST"`) state.
3. Print a classification per event (`OK`, `Error`, `NOT FOUND`).
4. Prompt for confirmation; on `yes`, archive the OK events via the EC `delete` action.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/bin/sync_ec_events.py` | Interactive cleanup script, installed into the site `bin/` directory. |

## Installation

1. Install the MKP on the Checkmk site. The script is placed in the site's `bin/` directory.
2. Log in as the site user and run `sync_ec_events.py --rule-filter <rule_id>`.

## Usage

```text
sync_ec_events.py --rule-filter <rule_id> [--user <name>] [--password <secret>] \
                  [--site-url https://host/site] [--no-verify]
```

| Flag | Required | Meaning |
| --- | --- | --- |
| `--rule-filter` | yes | EC rule ID whose open events should be reconciled. |
| `--user` | no | Checkmk user; defaults to `automation`. |
| `--password` | no | Password or automation secret; auto-loaded from the site when omitted. |
| `--site-url` | no | Full site URL; defaults to `http://localhost/<OMD_SITE>`. |
| `--no-verify` | no | Disable TLS certificate verification. |

## Known limitations

- The `__main__` block in the current source calls `cmk.close_event(2, "cmk")` for debugging; `sync_ec_data()` is commented out. Remove the debug call and re-enable `sync_ec_data()` before using in production.
