# discover_os_labels

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p13-blue)
<!-- compatibility-badges:end -->

Deploys an agent plugin that detects the OS vendor and version on Linux, Solaris and AIX hosts and publishes the result as Checkmk host labels. The labels can then be used as conditions in other rules.

## How it works

The Linux variant reads `/etc/os-release` (falling back to `/etc/redhat-release` or `/etc/SuSE-release`) and emits a `<<<labels:sep(0)>>>` section containing one JSON object per line. Equivalent plugins exist for Solaris and AIX. No dedicated check plugin is needed; Checkmk ingests the labels natively.

### Published labels

- `OS_Vend_Vers_Detect` — always `in_Place` when the plugin ran successfully.
- `OS_Vendor` — e.g. `rhel`, `sles`, `debian`, or `not_found`.
- `OS_Vendor_Major_Version` — major version digit only.
- `OS_Vendor_Maj_Vers` — `<vendor>_<major>` (e.g. `rhel_9`).
- `OS_Vendor_Vers` — `<vendor>_<full version>`.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/agents/plugins/discover_os_labels.linux` | Linux shell plugin. |
| `src/agents/plugins/discover_os_labels.solaris` | Solaris shell plugin. |
| `src/agents/plugins/discover_os_labels.aix` | AIX shell plugin. |
| `src/discover_os_labels/agent_based/bakery.py` | Agent Bakery hook, selects the correct plugin per OS. |
| `src/discover_os_labels/rulesets/bakery.py` | WATO rule for Bakery deployment. |

## Installation

1. Install the MKP on the Checkmk site.
2. Enable the rule *Agent rules -> Operating System -> Discover OS Labels* for the target hosts and bake the agent. The rule allows sync, cached (async) or no deployment.
3. After the next agent run the host will appear with the labels listed above.

## Configuration

Rule: **Agent rules -> Operating System -> Discover OS Labels**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `deployment` | `CascadingSingleChoice` | `sync`, `cached` (with interval), or `do_not_deploy`. Default: `cached`. |
