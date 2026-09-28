# AIDE File Integrity

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0b1-2f4f4f) ![packaged](https://img.shields.io/badge/packaged-2.5.0p13-blue)
<!-- compatibility-badges:end -->

Monitors file integrity checks of [AIDE](https://aide.github.io/) in Checkmk. One
service `AIDE <job>` per AIDE configuration shows whether files, directories,
permissions, owners, ACLs, SELinux contexts or extended attributes differ from the
AIDE database — and also whether the check itself ran, failed or is outdated.

The package does **not** install AIDE, write AIDE configurations or initialise
databases. What AIDE watches stays entirely in the AIDE configuration on the host.

## How it works

```
systemd timer ──> cmk-aide-run ──> /var/lib/cmk-aide/<job>.result ──> agent plug-in "aide" ──> service "AIDE <job>"
                  (aide --check)                                        (only reads)
```

| File | Purpose |
| --- | --- |
| `/usr/bin/cmk-aide-run` | Runs `aide --config=<file> --check` for every job, with a timeout and a lock, and writes the result file atomically. |
| `/etc/cmk-aide.cfg` | Mode, result directory, timeout, output limit and the jobs (`JOB <name> <aide config>`). |
| `<plug-in directory>/aide` | Agent plug-in, prints the section `<<<aide>>>` from the result files. |
| `/etc/systemd/system/cmk-aide-run.{service,timer}` | Only in the timer mode. Enabled by the package scriptlets. |

A result file holds the job, the AIDE configuration, start and end time, the exit
code of AIDE and its output (without the database checksums at the end, limited to
`MAX_LINES`). The agent adds its own time, so the age of a result is measured with
the clock of the monitored host.

There are two modes, selected in the bakery rule:

* **systemd timer** (default): AIDE runs as root in its own interval, independent
  of the agent. The agent only reads the files. Long AIDE runs never delay or break
  the agent. This is the recommended mode.
* **inline**: the agent plug-in starts `cmk-aide-run` on every call (optionally
  asynchronously with a cache age). Only for small configurations that finish in
  seconds, and the agent has to run as root to read protected directories.

Both modes use the same runner and the same result format, so switching between
them changes nothing in Checkmk.

## Setup

1. Install AIDE on the host, write the AIDE configuration for the directories to
   watch and initialise the database:

   ```
   aide --config=/etc/aide-fhs.conf --init
   mv /var/lib/aide/fhs.db.new.gz /var/lib/aide/fhs.db.gz
   ```

2. Install the MKP on the Checkmk site.
3. Create the bakery rule **AIDE file integrity (Linux)**: choose the mode and add
   one job per AIDE configuration (e.g. name `fhs`, configuration
   `/etc/aide-fhs.conf`). Bake and deploy the agent.
4. Run a service discovery on the host. Until the first run of the timer the
   service shows *No result yet* (CRIT by default); `cmk-aide-run` on the host
   produces a result immediately.

Without the bakery, copy `cmk-aide-run` to `/usr/bin`, the plug-in to the plug-in
directory of the agent, write `/etc/cmk-aide.cfg` by hand and create the timer:

```
MODE=timer
RESULT_DIR=/var/lib/cmk-aide
TIMEOUT=600
MAX_LINES=2000
JOB fhs /etc/aide-fhs.conf
```

If the agent binaries are installed to a directory other than `/usr/bin` (rule
*Installation paths for agent files*), make sure `cmk-aide-run` is in the `PATH` of
systemd and of the agent.

## Status mapping

All states can be changed in the rule **AIDE file integrity**.

| Situation | AIDE exit code | Default state |
| --- | --- | --- |
| No differences | 0 | OK |
| Added, removed or changed entries | 1–7 (bit mask) | CRIT |
| AIDE failed: database or configuration missing/unreadable, invalid config, version mismatch | 14–19 | CRIT |
| Timeout of `cmk-aide-run` | 124 | CRIT |
| `aide` not installed / not executable | 126, 127 | CRIT |
| Job configured, but no result file yet | – | CRIT |
| Result file not readable by the agent user | – | CRIT |
| `cmk-aide-run` itself failed in the inline mode | – | CRIT |
| Result older than the maximum age | – | WARN 3 h / CRIT 6 h |
| Agent plug-in no longer delivers the section | – | service goes stale / UNKNOWN (Checkmk standard) |

The maximum age has to fit the interval of the timer; a reasonable value is two to
three intervals for WARN. The details of a service with differences list the paths
with the AIDE flags and the old and new attributes as AIDE reports them.

Every difference is CRIT on purpose. A finer evaluation (e.g. WARN for stricter
permissions) would need a per-attribute interpretation of the AIDE output, makes the
check more complex and can cause false positives or hide a real change.

## Handling legitimate changes

A difference stays CRIT until the AIDE database matches the file system again —
acknowledging the problem in Checkmk alone does not change that. After review by
an administrator or incident responder, either

* **revert** the change on the host, or
* **accept** it by updating the database:

  ```
  aide --config=/etc/aide-fhs.conf --update
  mv /var/lib/aide/fhs.db.new.gz /var/lib/aide/fhs.db.gz
  cmk-aide-run fhs
  ```

`cmk-aide-run <job>` refreshes the result at once, so the service turns OK with the
next agent call instead of the next timer run. Planned changes (package updates,
deployments) are best followed by the same update as part of the change process.
Checkmk downtimes or acknowledgements can bridge the time until the database is
updated.

## Adding further AIDE checks

Every further AIDE check is a job: write an AIDE configuration with its own
database (`database_in` / `database_out`), initialise it, and add a job in the
bakery rule. Each job gets its own service, its own result file and its own
parameters (rule condition on the item). No change to the plug-in is needed.

## Test cases

`testdata/agent_output.txt` is the real output of AIDE 0.19.2 (Rocky Linux 9) with
three jobs: one with differences (added, removed, owner and permission/ACL change),
one with a missing database (exit 18) and one that never ran. The following cases
were checked with a real AIDE:

| Case | How to reproduce | Expected |
| --- | --- | --- |
| Clean | `aide --init`, move the database, run | OK, number of entries |
| New file | `touch <dir>/new` | CRIT, 1 added |
| Removed file | `rm <dir>/file` | CRIT, 1 removed |
| Permission / ACL | `chmod 600 <file>` | CRIT, 1 changed, `Perm` and `ACL` in the details |
| Owner | `chown nobody <dir>` | CRIT, 1 changed, `Uid` in the details |
| Database missing | remove the database | CRIT, IO error (exit code 18) |
| Timeout | `TIMEOUT=1` and a long run | CRIT, timeout (exit code 124) |
| AIDE missing | uninstall aide | CRIT, aide not found (exit code 127) |
| Never ran | new job, no run yet | CRIT, no result yet |
| Outdated | stop the timer | WARN/CRIT on the age of the result |
| Agent not root (inline) | run the plug-in as a normal user | CRIT, cmk-aide-run cannot write to the result directory |
| Accepted change | `aide --update`, move database, `cmk-aide-run` | OK |

To estimate the false positive rate, run the check in the timer mode for some
weeks and look at the service history: every CRIT that was not caused by a real
change points to a directory that should be excluded or to attributes that should
not be compared in the AIDE configuration.
