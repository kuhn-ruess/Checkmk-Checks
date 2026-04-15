# Directory Size Monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p13-blue)
<!-- compatibility-badges:end -->

Monitors the on-disk size of arbitrary directories on Linux, Solaris and AIX hosts. One `Size of <path>` service is created per configured directory, with optional upper WARN/CRIT levels on the folder size.

## How it works

A shell agent plugin reads the directory list from `$MK_CONFDIR/dir_size.cfg` and runs `du -s` for each entry. Output is emitted under the `<<<dir_size>>>` agent section, which the check plugin in [`src/dir_size/agent_based/dir_size.py`](src/dir_size/agent_based/dir_size.py) parses into a `{path: size}` mapping. Sizes reported by `du` in KB are converted to bytes before applying levels.

### Example agent output

```text
<<<dir_size>>>
17516   /tmp/
626088  /usr/local/
```

## Package contents

| Path | Purpose |
| --- | --- |
| `src/agents/plugins/dir_size.sh` | Shell agent plugin, reads `dir_size.cfg` and runs `du -s` per path. |
| `src/dir_size/agent_based/dir_size.py` | Section parser and check plugin (`dir_size`). |
| `src/dir_size/agent_based/bakery.py` | Agent Bakery hook: deploys the plugin plus a generated `dir_size.cfg`. |
| `src/dir_size/rulesets/bakery.py` | WATO rule for Bakery deployment (folder list, sync/cached mode). |
| `src/dir_size/rulesets/rules.py` | WATO rule for per-directory size levels. |

## Installation

1. Install the MKP on the Checkmk site.
2. Deploy the agent plugin:
   - **With Bakery:** enable the rule *Agent rules -> Storage -> dir_size: Directory Size Monitoring* and list the folder paths to monitor. Choose synchronous or cached (asynchronous) execution.
   - **Without Bakery:** copy `src/agents/plugins/dir_size.sh` to `/usr/lib/check_mk_agent/plugins/` on the target host, `chmod +x` it, and create `/etc/check_mk/dir_size.cfg` with one absolute path per line.
3. Run service discovery. A `Size of <path>` service is created for each listed directory.

## Configuration

Rule: **Service monitoring rules -> Applications -> dir_size: Directory Parameters**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `levels` | `SimpleLevels` on `DataSize` (upper) | Optional upper WARN/CRIT thresholds on the folder size in bytes. |

If no levels are configured the service reports only the current folder size without thresholds. A migration helper converts the legacy `levels_upper` parameter format.

## Services & metrics

- **Service:** `Size of <path>` — one per configured directory.
- **Metric:** `bytes` — current folder size.
