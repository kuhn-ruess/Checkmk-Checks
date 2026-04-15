# HP OpenView Agent Version Monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p7-blue)
<!-- compatibility-badges:end -->

Ships an agent-side script that detects whether an HP OpenView /
Operations Agent ("OVO") is installed on Linux, Solaris or AIX hosts
and publishes its version as Checkmk host labels. Useful for
inventorying OVO agent rollouts alongside Checkmk.

## How it works

The agent plugin runs `/opt/OV/bin/ovdeploy -inv` (wrapped in `waitmax
-s 9 2`) and greps for the `Operations-agent` and `HPOvSecCo`
component versions. The result is emitted as a `<<<labels:sep(0)>>>`
section, so the values become host labels in Checkmk:

```text
<<<labels:sep(0)>>>
{"HP_OVO_Vers_Detect": "in_Place"}
{"HP_OVO_OA_Installed": "Yes"}
{"HP_OVO_OA_Vers_gen": "12.12.010"}
{"HP_OVO_OA_Vers_HPOvSecCo": "12.12.010"}
```

If `ovdeploy` is not installed, only `HP_OVO_OA_Installed: No` is
emitted.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/agents/plugins/ovo_agent_linux.sh` | Linux agent plugin. |
| `src/agents/plugins/ovo_agent_solaris.sh` | Solaris agent plugin. |
| `src/agents/plugins/ovo_agent_aix.sh` | AIX agent plugin. |
| `src/ovo_agent/agent_based/bakery.py` | Bakery registration, deploys the matching script for Linux, Solaris and AIX. |
| `src/ovo_agent/rulesets/bakery.py` | `AgentConfig` ruleset `ovo_agent`. |

## Installation

1. Install the MKP on the Checkmk site.
2. Create a rule *Agent rules -> Operating system -> Monitoring the
   Agents of HP Openview* and bake the agent. The Bakery picks the
   matching script per OS automatically.
3. After the next agent run the new host labels appear and can be used
   in rules or dashboards.

## Configuration

| Parameter | Type | Meaning |
| --- | --- | --- |
| `deployment` | `sync` / `cached <TimeSpan>` / `do_not_deploy` | How the Bakery deploys the plugin on the target host. |

## Known limitations

- The plugin is only effective on hosts that have `waitmax` available;
  otherwise it exits silently.
- Reports host labels only — no services or metrics are generated.
