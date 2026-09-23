# mk_logwatch via sudo

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0b1-2f4f4f) ![packaged](https://img.shields.io/badge/packaged-2.5.0p13-blue)
<!-- compatibility-badges:end -->

Runs the `mk_logwatch` that is installed on the host as another user through `sudo`.
Typical case: the Checkmk agent is deployed as a non-root agent (rule *Customize
agent package (Linux)*) and can no longer read the log files, so mk_logwatch has to
run as `root`. The other direction works as well — an agent running as root that
reads a log file as an unprivileged service user.

**No logwatch is shipped with this package.** The wrapper always calls the original
mk_logwatch of the rule *Text logfiles (Linux, UNIX, Windows)*, wherever the agent
package put it, so the version on the host stays the one of the agent. A customized
mk_logwatch below `local/share/check_mk/agents/plugins/` is therefore used as well —
the standard rule deploys it, the wrapper calls it.

## How it works

The bakery rule **Run mk_logwatch as another user (sudo)** deploys two files:

| File | Purpose |
| --- | --- |
| `<plug-in directory>/mk_logsudo.py` | The wrapper, started by the agent. |
| `<config directory>/mk_logsudo.cfg` | User, maximum runtime and the optional state directory. |

The wrapper calls itself as the configured user:

```
sudo --non-interactive --user <user> <plug-in directory>/mk_logsudo.py --run
```

The child sets `MK_LIBDIR`, `MK_CONFDIR` and `MK_VARDIR` again — sudo drops the
environment — looks for mk_logwatch and executes it. The output is passed through
unchanged, so the normal `LOG ...` services keep working.

**Every path is determined at runtime**, from `MK_LIBDIR`, `MK_CONFDIR` and
`MK_VARDIR` of the agent and, where sudo has dropped them, from the place this file
was installed to. A custom installation directory of *Customize agent package
(Linux)* therefore needs no configuration: for an installation directory of
`/opt/kr/cmkagent` the wrapper finds `/opt/kr/cmkagent/default/package` as library
directory, `.../package/config` as configuration and `/opt/kr/cmkagent/default/runtime`
as state directory. Without a single directory deployment it uses the defaults of
the agent itself, `/etc/check_mk` and `/var/lib/check_mk_agent`. mk_logwatch is searched for as
`mk_logwatch.py` and `mk_logwatch`, in the plug-in directory and in the interval
subdirectories below it, so a *Text logfiles* rule with a cache age is found too.
The key `PLUGIN` in the configuration file overrides the search.

**The logwatch configuration is not touched.** `logwatch.cfg` and `logwatch.d` are
read as usual, the wrapper only changes *who* reads the log files.

## Python on the monitored host

The wrapper is an agent plug-in, so it has to start on the Python the monitored
host brings, not on the one of the Checkmk site. It is written for **Python 3.6**
and parses down to 3.4: no walrus operator, no f-strings, no annotations, nothing
that a newer interpreter introduced. A construct from a newer version is not a
runtime error but a **syntax error**, which kills the plug-in before its first
line runs — the agent then delivers no section at all and nothing says why.

`check_agent_plugins.py` in the repository root keeps it that way:

```
./check_agent_plugins.py mk_logwatch_sudo
./check_agent_plugins.py --floor 3.4 mk_logwatch_sudo
./check_agent_plugins.py --python /usr/bin/python3.6 mk_logwatch_sudo
```

It walks the syntax tree for constructs above the floor and also looks for calls
that only exist in newer versions (`shlex.join`, `str.removeprefix`,
`subprocess.run(capture_output=)` and friends). With `--python` the file is
additionally compiled by that interpreter, which is the real proof.

## What the wrapper changes on the host

The rule *Text logfiles* deploys plug-in and configuration together, the plug-in
alone cannot be switched off there. Without further action the agent would run
mk_logwatch a second time, as the agent user, and every message would be reported
twice. The wrapper therefore takes care of that itself, no manual step is needed:

* On its first run it removes the **execute bit** of the shipped `mk_logwatch.py`
  (`0755` becomes `0644`). Nothing else about the file changes — it is not moved,
  not renamed, not deleted, its content stays untouched, and the wrapper calls it
  through its shebang, so it keeps working.
* This already takes effect on the **first agent call**. The wrapper is named so
  that it sorts before `mk_logwatch.py`, and the agent checks the execute bit of
  each plug-in right before it runs it, so the shipped one is skipped in the same
  run.
* An **agent update** puts the execute bit back, because the package manager
  reinstalls the file. The wrapper checks on every run and removes it again, so the
  next agent call is back to normal by itself.
* Every change is written to `mk_logsudo.log` in the state directory of the agent,
  once per occurrence and not on every run:

  ```
  2026-09-22 12:25:57 took the execute bit from /opt/checkmk/agent/default/package/plugins/mk_logwatch.py (was 0755, undo: chmod 0755 /opt/checkmk/agent/default/package/plugins/mk_logwatch.py)
  ```

* The chmod is done by whoever can: first the agent itself, which is enough when it
  runs as root, and otherwise the **configured user** through sudo, because the file
  normally belongs to root. If that user may not change it, nothing is touched
  and the wrapper reports it as a warning of the log file `mk_logsudo`, with the
  command to run by hand. That is the safety net: logwatch still works, it is only
  reported twice until the warning is dealt with.

### Undoing it

After removing the rule (or the package), deploy the agent once more: the package
manager reinstalls `mk_logwatch.py` with mode `0755` and nothing takes the bit away
again. On a host that is not re-deployed, the exact command is in `mk_logsudo.log`:

```
chmod 0755 /usr/lib/check_mk_agent/plugins/mk_logwatch.py
```

While the bit is missing, `mk_logwatch.py` is not listed in the agent section
`<<<checkmk_agent_plugins_lnx>>>`, and `dpkg -V` / `rpm -V` report the changed mode
of that one file.

## sudo

The agent user needs one sudo rule. sudo only accepts an absolute command and the
bakery does not know the installation directory of the agent, so the section
*Deploy the sudo rule* asks for the agent user **and** the plug-in directory. It
then writes `/etc/sudoers.d/check_mk_mk_logsudo`:

```
cmk-agent ALL=(root) NOPASSWD: /opt/kr/cmkagent/default/package/plugins/mk_logsudo.py --run
```

If that path does not match where the agent really put the plug-in, sudo refuses
the call, the takeover does not happen and logwatch is reported twice. The wrapper
says so in the agent output and names the line that is really needed:

```
C mk_logwatch failed as user root: sudo: a password is required. Needed sudo rule:
  cmk-agent ALL=(root) NOPASSWD: /opt/kr/cmkagent/default/package/plugins/mk_logsudo.py --run
```

An agent that runs as root needs no sudo rule. When mk_logwatch is to run as an
unprivileged user instead, that user additionally needs

* read access to the log files, and write access to the mode of `mk_logwatch.py`
  (otherwise only the warning above),
* read access to `logwatch.cfg` and `mk_logsudo.cfg` — the bakery writes both
  with mode 0640 and the agent user as group,
* a writable state directory. The wrapper creates the directory from *State
  directory for the other user* on the first run if it may; below
  `/var/lib/check_mk_agent` it may not, so create it once by hand:

  ```
  mkdir -p /var/lib/check_mk_agent/logwatch_sudo
  chown logreader /var/lib/check_mk_agent/logwatch_sudo
  chmod 0700 /var/lib/check_mk_agent/logwatch_sudo
  ```

## Configuration

`mk_logsudo.cfg` in the agent configuration directory:

| Key | Meaning |
| --- | --- |
| `USER` | User mk_logwatch is run as, `root` by default. |
| `TIMEOUT` | Maximum runtime of the call, 120 seconds by default. |
| `PLUGIN` | Path of mk_logwatch, when the search does not find it. |
| `STATE_DIR` | State directory of the other user, instead of the agent's variable directory. |

Without the bakery the file can be written by hand, all keys are optional.

## Troubleshooting

Every problem is reported as a message of the pseudo log file `mk_logsudo`, so
it shows up as the service `LOG mk_logsudo`: `W` for a still executable
mk_logwatch, `C` for a failed call, with the last lines of the error.

```
<<<logwatch>>>
[[[mk_logsudo]]]
C Cannot create the state directory /var/lib/check_mk_agent/logwatch_sudo: [Errno 13] Permission denied
```

Called with `--diag` on the host, the wrapper prints everything it found — the
directories, the config it read, the mk_logwatch it would call and its mode, and
whether sudo lets the call through:

```
# /opt/kr/cmkagent/default/package/plugins/mk_logsudo.py --diag
mk_logsudo 1.0.2
running as         : cmk-agent (euid 999)
MK_LIBDIR          : /opt/kr/cmkagent/default/package (derived)
MK_CONFDIR         : /opt/kr/cmkagent/default/package/config (derived)
MK_VARDIR          : /opt/kr/cmkagent/default/runtime (derived)
mk_logwatch        : /opt/kr/cmkagent/default/package/plugins/mk_logwatch.py (mode 0755, the agent runs it too, the execute bit has to go)
needed sudo rule   : cmk-agent ALL=(root) NOPASSWD: /opt/kr/cmkagent/default/package/plugins/mk_logsudo.py --run
sudo allows it     : yes
```

An unexpected error is reported as a logwatch message as well instead of being
dropped with the plug-in output.

The agent reports the version of the wrapper in the section
`<<<checkmk_agent_plugins_lnx>>>` as `mk_logsudo.py:CMK_VERSION = "..."`.

**Known difference to the standard plug-in:** sudo does not pass `REMOTE` on, so
mk_logwatch writes its state as `logwatch.state.remote-unknown` instead of one file
per Checkmk server. With a single server nothing changes; hosts that are polled by
several servers share one state.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/agents/plugins/mk_logsudo.py` | The wrapper. |
| `src/lib/python3/cmk/base/cee/plugins/bakery/mk_logwatch_sudo.py` | Bakery deployment and the sudoers file. |
| `src/mk_logwatch_sudo/rulesets/bakery.py` | The bakery rule. |
| `testdata/agent_output.txt` | Agent output of a run through the wrapper. |
| `testdata/agent_output_error.txt` | Agent output of a refused sudo call and of the safety net. |
| `testdata/diag_output.txt` | Output of `mk_logsudo.py --diag` on a custom installation directory. |
