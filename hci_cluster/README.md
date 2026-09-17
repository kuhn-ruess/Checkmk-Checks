# HCI Cluster Monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0-2f4f4f) ![packaged](https://img.shields.io/badge/packaged-2.3.0p25-blue)
<!-- compatibility-badges:end -->

Monitoring for Microsoft Storage Spaces Direct / Failover Cluster (HCI) environments. A PowerShell agent plugin on a Windows host queries cluster state via the FailoverClusters cmdlets and produces sections that are evaluated by several check plugins: nodes, cluster resources, S2D storage pools, virtual disks, storage jobs, and volume performance.

## How it works

1. The Bakery deploys `hci_cluster.ps1` to Windows hosts together with a generated `hci_cluster.cfg.ps1` that sets `$domain`, `$FilterTyp` (`None` / `Inclusion` / `Exclusion`), and `$FilterPattern`.
2. The plugin connects to the cluster (the Checkmk agent user needs permissions to query cluster information) and prints several sections.
3. Each section is parsed into a dict keyed by an identifier and evaluated by its own check plugin.

Sections and services produced:

| Section | Service name | State logic |
| --- | --- | --- |
| `hci_cluster_nodes` | `Node <Name>` | OK when `State == Up`, else CRIT |
| `hci_cluster_resources` | `Resource <Name>` | OK when `State == Online`, else CRIT |
| `hci_s2d_storage_pools` | `Storage Pool <DeviceId>` | OK when `OperationalStatus == OK`, else CRIT |
| `hci_virtual_disks` | `Virtual Disk <FriendlyName>` | OK when `OperationalStatus == OK`, else CRIT |
| `hci_storage_jobs` | `Storage Jobs` | OK if no jobs, CRIT while any job is listed (a running job is treated as bad even in state `Completed`) |
| `hci_s2d_volume_performance` / `hci_cluster_performance` | `Storage Pool Performance` | Informational: IOPS, latency, throughput, size; cluster mode also reports CsvCache metrics |

## Package contents

| Path | Purpose |
| --- | --- |
| `src/agents/plugins/hci_cluster.ps1` | PowerShell agent plugin that queries the cluster and emits all sections. |
| `src/cmk_addons_plugins/hci_cluster/agent_based/hci_helper.py` | Shared parsers (`parse_list`, `parse_multi_list`). |
| `src/cmk_addons_plugins/hci_cluster/agent_based/hci_cluster_nodes.py` | Cluster node check. |
| `src/cmk_addons_plugins/hci_cluster/agent_based/hci_cluster_resources.py` | Cluster resource check. |
| `src/cmk_addons_plugins/hci_cluster/agent_based/hci_s2d-storage-pools.py` | S2D storage pool check. |
| `src/cmk_addons_plugins/hci_cluster/agent_based/hci_virtual_disks.py` | Virtual disk check. |
| `src/cmk_addons_plugins/hci_cluster/agent_based/hci_storage_jobs.py` | Storage jobs check. |
| `src/cmk_addons_plugins/hci_cluster/agent_based/hci_s2d_volume_performance.py` | Volume / cluster performance metrics. |
| `src/cmk_addons_plugins/hci_cluster/agent_based/bakery.py` | Bakery hook registering the plugin and config. |
| `src/cmk_addons_plugins/hci_cluster/rulesets/bakery.py` | WATO ruleset for the Bakery config. |

## Installation

1. Install the MKP on the Checkmk site.
2. Deploy the plugin via the Agent Bakery rule *HCI Cluster Monitoring (Windows)* to a Windows host that has permission to query the cluster (domain account with cluster access).
3. Bake and roll out the agent; run service discovery on the host.

## Configuration

Bakery rule: **Agent rules -> HCI Cluster Monitoring (Windows)**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `deployment` | `sync` / `cached` (interval) / `do_not_deploy` | Whether the plugin is deployed and whether it runs synchronously or cached. |
| `domain` | text | AD domain to run the cluster query against. |
| `filter_type` | `no_filter` / `inclusion` / `exclusion` | How `filter_pattern` is applied when enumerating cluster objects. |
| `filter_pattern` | text | Pattern used together with `filter_type` (e.g. `HCI`). Optional. |

## Upgrading to 2.1.0

The Bakery ruleset was ported from the pre-2.3 WATO API to `cmk.rulesets.v1`.
On Checkmk 2.5 the old file could not be imported at all
(`ModuleNotFoundError: No module named 'cmk.gui.cee'`), which made the whole
rule spec loading of the site fail — not just this package.

Existing rules keep working: the bakery plugin still accepts the old value
shape (a plain dict, or `None` for "do not deploy") and the capitalized
`None` / `Inclusion` / `Exclusion` filter values. As soon as a rule is opened
and saved in the GUI it is written in the new shape, which adds the
`deployment` choice and spells the filter types `no_filter` / `inclusion` /
`exclusion` (the PowerShell plugin receives the capitalized value either way).

## Known limitations

- `hci_storage_jobs` intentionally reports CRIT whenever any job is listed, including `Completed`, because the Windows API keeps completed jobs visible.
- `hci_s2d_volume_performance` uses `render.timespan` for IOPS-like metrics — a cosmetic quirk kept from the original implementation.
