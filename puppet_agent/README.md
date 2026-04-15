# Puppet Agent Monitor

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-1.6.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.2.0p16-blue)
<!-- compatibility-badges:end -->

Monitors the state of a local Puppet agent by reading its
`last_run_summary.yaml` and reporting how long ago Puppet last ran as well
as the counters for failed, changed, restarted and out-of-sync resources.
Ships Linux and Windows agent plugins plus a Bakery hook.

## How it works

1. Agent plugin reads Puppet's `last_run_summary.yaml` (requires Puppet
   7+). The Linux shell plugin searches
   `/var/lib/puppet/public/last_run_summary.yaml` and
   `/opt/puppetlabs/puppet/public/last_run_summary.yaml`; the Windows
   PowerShell plugin does the Windows equivalent.
2. The agent emits a flat `key: value` list under `<<<puppet_agent>>>`
   containing `last_run`, `resources_*` and `events_*` counters.
3. A single service `Puppet Agent` is created. The check reports the
   last-run timestamp and applies upper levels on all counters.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/agents/plugins/puppet_agent.sh` | Linux agent plug-in: parses `last_run_summary.yaml` and prints counters. |
| `src/agents/plugins/puppet_agent.ps1` | Windows agent plug-in (PowerShell) with the same output format. |
| `src/agents/bakery/puppet_agent` | Legacy Bakery hook for Linux/Windows deployment. |
| `src/checks/puppet_agent` | Legacy check plugin `puppet_agent`. |
| `src/web/plugins/wato/puppet_agent.py` | Legacy WATO rules: agent plug-in deployment toggle and per-counter levels. |

## Installation

1. Install the MKP on the Checkmk site.
2. Deploy the agent plugin:
   - **With Bakery:** enable the rule *Agent Plugins -> Deploy puppet
     agent Monitoring (Linux, Windows)*.
   - **Without Bakery:** copy `puppet_agent.sh` (Linux) or
     `puppet_agent.ps1` (Windows) into the agent plugins directory on the
     target host.
3. Run service discovery. A single `Puppet Agent` service is created per
   host.

## Configuration

Rule: **Parameters for discovered services -> Applications -> Puppet
Agent**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `last_run` | `(warn, crit)` in seconds | Maximum age of the last Puppet run. Default: 1600 / 3200. |
| `events_failure` | `(warn, crit)` | Upper levels on failed events. Default: 10 / 15. |
| `resources_changed` | `(warn, crit)` | Upper levels on changed resources. Default: 10 / 15. |
| `resources_failed` | `(warn, crit)` | Upper levels on failed resources. Default: 10 / 15. |
| `resources_failed_to_restart` | `(warn, crit)` | Upper levels. Default: 10 / 15. |
| `resources_out_of_sync` | `(warn, crit)` | Upper levels. Default: 10 / 15. |
| `resources_restarted` | `(warn, crit)` | Upper levels. Default: 10 / 15. |
| `resources_scheduled` | `(warn, crit)` | Upper levels. Default: 10 / 15. |

## Services & metrics

- **Service:** `Puppet Agent` (one per host)
- **Metrics:** `events_failure`, `resources_changed`, `resources_failed`,
  `resources_failed_to_restart`, `resources_out_of_sync`,
  `resources_restarted`, `resources_scheduled`.

## Known limitations

- Uses the legacy `check_info` / `register_rule` /
  `register_check_parameters` APIs, hence `min_required` 1.6.0.
- Requires Puppet 7+ (older summary format is not parsed).
