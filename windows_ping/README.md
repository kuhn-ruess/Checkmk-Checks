# windows_ping

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0-2f4f4f) ![packaged](https://img.shields.io/badge/packaged-2.4.0p13-blue)
<!-- compatibility-badges:end -->

Ping checks for Windows hosts, executed by the Checkmk agent on the host
itself. Useful when targets are only reachable from inside a network segment
the Checkmk server cannot see.

The package contains two independent ways to use it:

1. **Agent bakery plug-in `windows_ping.ps1`** (since 2.0.0): the targets are
   maintained in an agent bakery rule, the plug-in pings all of them
   concurrently and creates one local service per target.
2. **MRPE script `check_ping.ps1`** with its `check_ping.cmd` wrapper: a
   Nagios compatible single target check, deployed via "Deploy custom files
   with the agent" and called from MRPE.

## Agent bakery plug-in (windows_ping.ps1)

Requires a Checkmk edition with the agent bakery.

### Package layout

```text
windows_ping/
  src/
    agents/windows/plugins/windows_ping.ps1
    windows_ping/rulesets/bakery.py
    lib/python3/cmk/base/cee/plugins/bakery/windows_ping.py
```

### Configuration

Setup → Agents → Windows, Linux, Solaris, AIX → Agent rules →
**Windows Ping**

| Parameter | Default | Description |
|-----------|---------|-------------|
| Deployment type | synchronous | Run synchronously, cached (asynchronously, with interval) or do not deploy |
| Targets | (required) | List of targets: IP address or host name, optional display name |
| Echo requests per target | 1 | Number of echo requests per target and agent run |
| Timeout per echo request | 1000 ms | Timeout of a single echo request |
| Levels on average round trip time | 100 / 500 ms | WARN / CRIT on the average round trip time |
| Levels on packet loss | 40 / 80 % | WARN / CRIT on packet loss; no reply at all is always CRIT |

The bakery writes the settings to `windows_ping.cfg.ps1` in the agent config
directory (`C:\ProgramData\checkmk\agent\config`), the plug-in itself goes to
`C:\ProgramData\checkmk\agent\plugins`. Without a config file or without
targets the plug-in prints nothing.

Example of a generated config:

```powershell
$Targets = @(
    @{ Address = '192.0.2.10'; Name = 'Gateway' }
    @{ Address = '192.0.2.11'; Name = '' }
)
$Count = 1
$TimeoutMs = 1000
$WarnRta = 100
$CritRta = 500
$WarnPl = 40
$CritPl = 80
```

### Services

One local service per target, named `Ping <display name>` or
`Ping <address>` when no display name is set. After baking and updating the
agent, run a service discovery on the Windows host.

```text
<<<local:sep(0)>>>
0 "Ping Gateway" rta=0.002;0.1;0.5;0|pl=0;40;80;0;100 192.0.2.10: rta 2 ms, packet loss 0% (1/1)
2 "Ping 192.0.2.11" pl=100;40;80;0;100 192.0.2.11: no reply (TimedOut), packet loss 100%
```

Metrics: `rta` (seconds) and `pl` (percent). All targets are pinged in
parallel, so one agent run takes roughly `count × timeout` at most,
independent of the number of targets.

## MRPE script (check_ping.ps1)

### Package layout

```text
windows_ping/
  src/
    agents/custom/windows_ping/bin/check_ping.ps1
    agents/custom/windows_ping/bin/check_ping.cmd
```

Both files are packaged under `agents/custom/windows_ping/bin/` so that they
can be shipped through the Checkmk Agent Bakery rule **"Deploy custom files
with the agent"**. On the Checkmk server, after installing the MKP, they
live at:

```text
~/local/share/check_mk/agents/custom/windows_ping/bin/check_ping.ps1
~/local/share/check_mk/agents/custom/windows_ping/bin/check_ping.cmd
```

> **Important: the `bin/` subdirectory is required.** The custom-files
> bakelet only deploys files that sit under one of the logical
> subdirectories of the package (`bin`, `lib`, `config`, `var`,
> `lib/plugins`, `lib/local`). Files placed directly under
> `custom/windows_ping/` (as in releases ≤ 1.0.3) match no logical path and
> are silently **not** baked into the agent. `bin` is chosen because, unlike
> `lib/local` or `lib/plugins`, files there are deployed but not executed
> automatically by the agent, which is what an MRPE-invoked script needs.

On a Windows target the `bin` files are deployed to the agent's `bin`
directory:

```text
C:\ProgramData\checkmk\agent\bin\check_ping.ps1
C:\ProgramData\checkmk\agent\bin\check_ping.cmd
```

`check_ping.cmd` is a thin wrapper that resolves `powershell.exe` via
`%SystemRoot%`, invokes `check_ping.ps1` from its own directory and
forwards every argument plus the exit code. Always invoke the wrapper from
MRPE, never the `.ps1` directly (see below).

### Deployment via Agent Bakery

1. Install the MKP on the Checkmk site (Setup → Extension Packages).
2. Create/edit a rule under **Setup → Agents → Windows, Linux, Solaris, AIX →
   Deploy custom files with the agent** and add the `windows_ping` package to
   the files that should be shipped to the selected hosts.
3. Bake and sign the agent, then update the affected hosts.

### Invoking the check via MRPE

Add an MRPE entry to the Windows agent configuration
(`check_mk.user.yml`), pointing at the wrapper:

```yaml
mrpe:
  config:
    - check: 'Ping_router'
      plugin: 'C:\ProgramData\checkmk\agent\bin\check_ping.cmd router.example.com'
```

Classic `mrpe.cfg` format works the same way. After the next agent run,
rediscover services on the host; the check appears as `MRPE Ping_router`.

#### Why the wrapper

MRPE invokes the first whitespace-separated token of the `plugin:` line
via `CreateProcess` and only verifies that this token exists as a file on
disk. Pointing it directly at the `.ps1` is not possible (PowerShell
scripts are not executables), and pointing it at `powershell.exe` with the
`.ps1` as `-File` argument is fragile: an unqualified `powershell.exe`
fails the existence check (`Unable to execute - plugin may be missing`),
and even with the full path the agent's own argument splitter can mangle
the quotes around the script path, which then leaves PowerShell in
interactive mode (output starts with the `Windows PowerShell / Copyright`
banner and Checkmk reports `Invalid plug-in status '4294770688'`). The
`.cmd` wrapper sidesteps all of that.

### Parameters

| Parameter      | Default | Description                              |
|----------------|---------|------------------------------------------|
| `-HostName`    | (none)  | Target hostname or IP (required)         |
| `-Count`       | 4       | Number of echo requests                  |
| `-WarningRta`  | 200     | WARN if average RTA >= value (ms)        |
| `-CriticalRta` | 500     | CRIT if average RTA >= value (ms)        |
| `-WarningPl`   | 40      | WARN if packet loss >= value (%)         |
| `-CriticalPl`  | 80      | CRIT if packet loss >= value (%)         |

### Output / exit codes

Nagios convention: `0=OK`, `1=WARN`, `2=CRIT`, `3=UNKNOWN`. Status line
followed by performance data that Checkmk picks up automatically:

```
PING OK - router.example.com: rta 2.41ms, lost 0% (4/4) | rta=2.41ms;200;500;0; pl=0%;40;80;0;100 rtmin=1.9ms rtmax=3.1ms
```

## Compatibility

- Windows PowerShell 5.1 (uses `ResponseTime`)
- PowerShell 7+ (uses `Latency`)
