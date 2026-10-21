# DNF Updates

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0-2f4f4f) ![packaged](https://img.shields.io/badge/packaged-2.4.0p19-blue)
<!-- compatibility-badges:end -->

Monitors pending package updates on RHEL compatible hosts (RHEL, Rocky, Alma,
Oracle Linux 8 and 9) with dnf. One service `DNF updates` per host shows security
and non-security updates, a required reboot and unreachable repositories, and it
respects a veto file and the update schedule of `dnf-automatic`.

## How it works

The agent plug-in `dnf_update` (POSIX shell) reports:

| Data | Source |
| --- | --- |
| Pending updates | `dnf check-update` |
| Pending security updates | `dnf -C --security check-update` |
| Unreachable repositories and their URLs | error output of `dnf check-update`, passwords in URLs are masked on the host |
| Reboot required | `dnf needs-restarting -r` (dnf-plugins-core), otherwise running versus newest installed kernel |
| Veto file | existence of `VETO_FILE` (default `/etc/dnf.veto`) |
| Last and next run of the update timer | `systemctl show` of `dnf-automatic.timer`, `dnf-automatic-install.timer`, `dnf-automatic-download.timer` or `dnf-automatic-notifyonly.timer` |
| Date and ISO calendar week | clock of the monitored host |

The check evaluates in this order, the first case that applies decides:

| Case | Default state |
| --- | --- |
| A repository is not reachable (details: affected URLs) | CRIT |
| `dnf check-update` failed for another reason | UNKNOWN |
| The veto file exists, automatic updates are disabled | CRIT |
| Update week set to even or odd and the current ISO week does not match | OK, not checked |
| The timer ran today | OK, not checked |
| The last run of the timer is longer ago than the configured days (default 3) | OK, not checked |
| Reboot required | CRIT |
| Security updates available | CRIT |
| Non-security updates available | WARN |

The last and next run of the timer are always shown in the details. Without a
timer that ever ran, updates are always evaluated. Metrics: `security_updates`
and `normal_updates` (the same as the built-in apt check).

## Setup

1. Install the MKP on the Checkmk site.
2. Agent bakery: create the rule **DNF updates (Linux)**. Default: asynchronous
   every 2 hours. Set the **Veto path** if it differs from `/etc/dnf.veto`. Bake
   and deploy the agent.

   Without the bakery copy `dnf_update` to `/usr/lib/check_mk_agent/plugins/7200/`
   and, for another veto path, create `/etc/check_mk/dnf_update.cfg`:

   ```
   VETO_FILE=/etc/dnf.veto
   ```

3. Run a service discovery on the host.
4. Optional: rule **DNF updates** for the days after the update timer, the update
   week (every week, even or odd calendar weeks) and all states. Use the
   conditions of the rule to set different update weeks per group of hosts.

The agent has to run as root, otherwise dnf cannot refresh its metadata.

## Test data

`testdata/` holds real output of the plug-in on Rocky Linux 8 and 9 containers
(pending updates, reboot required after a glibc update, an unreachable repository
with user and password in the URL). The timer lines and the kernel versions were
added by hand, because containers have no systemd and no kernel package.

| File | Expected |
| --- | --- |
| `rocky9_updates_reboot.txt` | CRIT: reboot required, 52 security updates, WARN: 56 non-security updates |
| `rocky9_repo_unreachable.txt` | CRIT: repository not reachable, masked URL in the details |
| `rocky9_veto.txt` | CRIT: veto file exists |
| `rocky8_updates.txt` | CRIT: kernel reboot required, security updates; OK with update week "even" (week 43) |
| `rocky8_timer_today.txt` | OK: updates already ran today |
| `rocky8_window_expired.txt` | OK: 3 day window expired |
