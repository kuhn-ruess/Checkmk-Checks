# Monitoring Linux sensors

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p5-blue)
<!-- compatibility-badges:end -->

Agent-side plugin that collects CPU temperatures via `lm-sensors` on Linux hosts and evaluates them through the built-in `temperature` check. One `Temperature CPU <core>` service is created per CPU core. The section supersedes `lnx_thermal`, so enabling this plugin disables the built-in thermal check.

## How it works

1. The bash agent plugin `lnx_sensors` calls `sensors --no-adapter -j` and emits the JSON under `<<<lnx_sensors>>>`.
2. `parse_lnx_sensors` concatenates the lines, parses JSON, and keeps every entry whose name contains `Core` under the `cpu` bucket.
3. The discovery function consumes the `discover_lnx_sensors` ruleset; filters currently only offer `cpu`.
4. `check_lnx_cpus` calls the library function `check_temperature` with the device WARN/CRIT values read from the sensor plus the default software levels `(70.0, 80.0)`.

Example agent output (truncated):

```text
<<<lnx_sensors>>>
{"coretemp-isa-0000": {"Core 0": {"temp1_input": 42.0, "temp1_max": 84.0, "temp1_crit": 100.0, "temp1_crit_alarm": 0.0}}}
```

## Package contents

| Path | Purpose |
| --- | --- |
| `src/agents/plugins/lnx_sensors` | Bash agent plugin shipped to Linux hosts (needs `sensors` / `lm-sensors`). |
| `src/cmk_addons_plugins/lnx_sensors/agent_based/lnx_cpu.py` | Section parser and CPU temperature check. |
| `src/cmk_addons_plugins/lnx_sensors/agent_based/agent_bakery_lnx_sensors.py` | Bakery hook that ships the plugin. |
| `src/cmk_addons_plugins/lnx_sensors/rulesets/agent_bakery_lnx_sensors.py` | AgentConfig rule *Sensors* for the Bakery. |
| `src/cmk_addons_plugins/lnx_sensors/rulesets/lnx_cpu.py` | DiscoveryParameters rule *Sensors discovery*. |

## Installation

1. Install the MKP on the Checkmk site.
2. Install `lm-sensors` on the target Linux hosts (`sensors` command must be on `$PATH`).
3. Deploy the agent plugin:
   - **With Bakery:** enable the rule *Sensors* under *Agent rules -> Operating system* and bake the agent.
   - **Without Bakery:** copy `src/agents/plugins/lnx_sensors` to `/usr/lib/check_mk_agent/plugins/lnx_sensors` and make it executable.
4. Enable the discovery rule *Sensors discovery* and select `CPU`, then run discovery.

## Configuration

| Rule | Parameter | Type | Meaning |
| --- | --- | --- | --- |
| *Sensors* (AgentConfig) | `deploy` | `sync` / `no_deploy` | Deploy and run the plugin synchronously, or skip deployment. |
| *Sensors discovery* (DiscoveryParameters) | `filters` | MultipleChoice | Which sensor groups to discover. Currently only `cpu` is available. |
| *Temperature* (built-in `temperature` ruleset) | — | — | Used for per-service thresholds. Defaults: WARN 70.0 degC, CRIT 80.0 degC, `device_levels_handling=devdefault`. |

## Services & metrics

- **Service:** `Temperature CPU <core>` — one per core entry returned by `sensors`.
- **State logic / metric:** delegated to `cmk.plugins.lib.temperature.check_temperature`, which emits the standard `temp` metric and combines device and software levels.

## Known limitations

- Only `Core *` entries are parsed; other `lm-sensors` channels (fans, package temperatures, chipset) are ignored.
- The section `supersedes = ["lnx_thermal"]`, so installing this plugin disables Checkmk's built-in `lnx_thermal` check as soon as an agent emits `<<<lnx_sensors>>>`.
