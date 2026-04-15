# Clean spool files of Checkmk Notification Spooler

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.3.0p9-blue)
<!-- compatibility-badges:end -->

Helper script that cleans out stale notifications from the Checkmk notification spooler. When a notification outburst hits the spooler, recovery or downtime-end notifications can queue up behind problem or downtime-start notifications that will never be useful any more. This script scans the spool directory and deletes matching problem/recovery and downtime-start/downtime-end pairs so the spooler drains faster.

## How it works

The script reads every file in `$OMD_ROOT/var/check_mk/notify/spool`, orders them by mtime, and walks through them:

- For hosts: a `DOWNTIMESTART` paired with a later `DOWNTIMEEND` causes both files to be deleted; likewise a `PROBLEM` paired with a later `RECOVERY`.
- For services: the same logic keyed on `HOSTNAME###SERVICEDESC`.
- At the end it prints a small ASCII summary of how many host/service state and downtime entries were removed and the total number of files inspected.

The script uses `eval()` to parse the spool files (which are Python literal dicts written by Checkmk). It must be run as the site user so that `OMD_ROOT` is set correctly.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/bin/clean_spoolfiles` | Python script installed as `bin/clean_spoolfiles` in the site. |

## Installation

1. Install the MKP on the Checkmk site.
2. Run `clean_spoolfiles` as the site user when the notification spooler is backed up. There is no scheduled trigger — you run it manually (or wire it into a cron of your choice).

## Known limitations

- Destructive: matching spool files are unlinked, not quarantined.
- Uses `eval()` on spool file content. This assumes the files were written by the Checkmk notification spooler itself.
- No locking against a concurrently running notification spooler.
