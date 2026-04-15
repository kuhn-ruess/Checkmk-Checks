# KVM / QEMU Monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.0.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.2.0p3-blue)
<!-- compatibility-badges:end -->

Monitors KVM / QEMU virtual machines on Linux hypervisors via `libvirt`.
One Checkmk service is created per running VM, reporting power state,
assigned memory, live CPU usage and memory usage, with optional WARN/CRIT
thresholds on CPU and memory.

## How it works

1. A shell agent plugin runs on the hypervisor and calls `virsh list` to
   enumerate domains.
2. For each domain it collects state, assigned memory (`virsh dominfo`),
   and live CPU / memory usage of the matching `qemu-*` process via `top`.
3. Output is emitted under the `<<<qemu>>>` agent section.
4. The check plugin [`qemu.py`](src/agent_based/qemu.py) parses the
   section, discovers one `VM <name>` service per **running** domain, and
   evaluates the configured CPU / memory thresholds.

### Example agent output

```text
<<<qemu>>>
4 i-4B9008BE running 2048 4.0 2.7
5 i-44F608B6 running 2048 0.0 0.7
```

## Package contents

| Path | Purpose |
|---|---|
| `src/agents/plugins/qemu` | Bash agent plugin shipped to Linux hypervisors (uses `virsh` + `top`). |
| `src/agents/bakery/qemu` | Agent Bakery hook — deploys the plugin when the Bakery rule is enabled. |
| `src/agent_based/qemu.py` | Section parser + check plugin. |
| `src/web/plugins/wato/qemu.py` | WATO rules: Bakery deployment toggle and per-VM CPU/memory thresholds. |

> **Note:** the WATO file uses the legacy pre-2.3 rulespec API
> (`register_rule` / `register_check_parameters`). Still loads on 2.3/2.4 as
> long as the legacy API is available — if it ever drops, this plugin needs
> porting to `cmk.rulesets.v1`.

## Installation

1. Install the MKP (`qemu-<version>.mkp`) on the Checkmk site.
2. Deploy the agent plugin:
   - **With Bakery:** enable the rule *Agent Plugins → QEMU/KVM Monitoring
     (Linux)* for the hypervisor hosts and bake the agent.
   - **Without Bakery:** copy `src/agents/plugins/qemu` to
     `/usr/lib/check_mk_agent/plugins/qemu` on the hypervisor and
     `chmod +x` it. The hypervisor must have `libvirt-clients` (for
     `virsh`) installed and the Checkmk agent user must be able to run it.
3. Run service discovery on the hypervisor host. A service `VM <name>` is
   created for each VM that is currently running.

## Configuration

Rule: **Parameters for discovered services → Applications, Processes &
Services → Qemu/KVM Check**

| Parameter | Type | Meaning |
|---|---|---|
| `cpu` | `(warn, crit)` in percent | Upper levels on live CPU usage of the VM process. |
| `mem` | `(warn, crit)` in percent | Upper levels on live memory usage of the VM process. |

Both parameters are optional; if unset the service only reports state and
assigned memory without WARN/CRIT thresholds.

## Services & metrics

- **Service:** `VM <vmname>` — one per running VM
- **State logic:** CRIT if the VM is not `running`, otherwise worst of
  CPU / memory level evaluation.
- **Metrics:** `cpu_util` (%), `memory_usage` (%)

## Known limitations

- VMs that are **not** in state `running` at discovery time are not
  created as services.
- CPU / memory are measured via a single `top -n 1` sample per agent
  run, so short spikes may be missed.
- VM name rewriting: names starting with `instance` are shortened to
  `i` — historical quirk kept for compatibility with existing service
  items.
