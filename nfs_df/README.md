# NFS Filesystem Monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p7-blue)
<!-- compatibility-badges:end -->

Adds NFS mount points to Checkmk filesystem monitoring on Linux hosts.
The stock Linux agent ignores NFS mounts for `df`; this plugin ships a
tiny agent-side script that enumerates NFS mounts with `df -PTk` and
re-emits them as a `df` section so they are picked up by the regular
filesystem check.

## How it works

1. The agent plugin `nfs_df` runs `df -PTk` (wrapped in `waitmax -s 9
   2` to avoid hangs on stuck NFS mounts), filters for the `nfs` fs
   type, and prints the result under `<<<df>>>` with the type rewritten
   to `NFS` so that the standard Checkmk filesystem check picks it up.
2. Deployment is driven by a Bakery rule with three modes: sync,
   cached (async with a configurable interval), or not at all.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/agents/plugins/nfs_df` | Bash agent plugin shipped to Linux hosts. |
| `src/nfs_df/agent_based/bakery.py` | Bakery registration (`register.bakery_plugin`). |
| `src/nfs_df/rulesets/backery.py` | `AgentConfig` ruleset `nfs_df`. |

## Installation

1. Install the MKP on the Checkmk site.
2. Create a rule *Agent rules -> Operating system -> Filesystemmonitoring
   of NFS Mounts via Plugin (Linux)* and bake the agent, or copy
   `src/agents/plugins/nfs_df` to `/usr/lib/check_mk_agent/plugins/`
   manually.
3. Discovered mount points show up as regular Filesystem services.

## Configuration

| Parameter | Type | Meaning |
| --- | --- | --- |
| `deployment` | `sync` / `cached <TimeSpan>` / `do_not_deploy` | How the Bakery deploys the plugin on the target host. |

## Known limitations

- The plugin only emits output if `waitmax` is available on the target
  host.
