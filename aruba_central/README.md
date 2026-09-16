# Aruba Central Access Points

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0b1-2f4f4f) ![packaged](https://img.shields.io/badge/packaged-2.5.0p13-blue)
<!-- compatibility-badges:end -->

Monitoring of Aruba Central access points. An agent plug-in calls the Aruba
Central CLI (`cencli show aps -v --json`) on a host that has cencli installed
and turns the result into one piggyback host per access point, so every AP gets
its own services in Checkmk.

## How it works

`cencli` mixes two status lines into its output, for example

```
Counts: ap: 393 (386:7), clients: 242
API Rate Limit: 11964 of 11970 remaining.
```

The plug-in separates the JSON document from those lines regardless of which
stream they arrive on, reports the counts and the rate limit as the service
`Aruba Central` on the collector host, and emits one piggyback section per
access point.

**Host names:** the key of the JSON document is the AP name. When that name is
just the MAC address of the access point, the serial number is used as the host
name instead, otherwise the name is used as it is.

The plug-in needs about 30 seconds, so deploy it asynchronously — the bakery
rule defaults to a 15 minute cache.

## Services

| Service | Host | Description |
| --- | --- | --- |
| `Aruba Central` | collector | AP counts, clients and the remaining API calls. |
| `AP Status` | access point | Up/Down, model, firmware, serial, MAC, IP, group, site, mode, SSIDs. |
| `AP Clients` | access point | Connected wireless clients. |
| `AP CPU utilization` | access point | CPU in percent, 80%/90% by default. |
| `AP Memory` | access point | Used memory in percent and bytes, 80%/90% by default. |
| `AP Uptime` | access point | Uptime in seconds, informational. |
| `AP Radio <name>` | access point | Radio status, channel utilization, TX power, channel and type. |

The access points also get the host labels `aruba/group`, `aruba/site` and
`aruba/model`, and an inventory entry with model, serial, firmware and the
radios.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/agents/plugins/aruba_central.py` | Agent plug-in for Linux. |
| `src/agents/plugins/aruba_central.ps1` | Agent plug-in for Windows, same output. |
| `src/aruba_central/agent_based/aruba_ap.py` | Section, host labels and the AP checks. |
| `src/aruba_central/agent_based/aruba_ap_radio.py` | Radio check. |
| `src/aruba_central/agent_based/aruba_central.py` | Collector status check. |
| `src/aruba_central/agent_based/aruba_ap_inventory.py` | Hardware and software inventory. |
| `src/aruba_central/agent_based/bakery.py` | Agent bakery deployment. |
| `src/aruba_central/rulesets/` | Check parameters and the deployment rule. |
| `src/aruba_central/graphing/metrics.py` | Metrics, graph and perfometers. |
| `src/aruba_central/checkman/` | Check documentation. |
| `testdata/agent_output.txt` | Anonymized agent output used for testing. |

## Installation

1. Install the MKP on the Checkmk site.
2. Install and configure `cencli` on the collector host for the user the Checkmk
   agent runs as.
3. Deploy the plug-in with the rule **Aruba Central access points (cencli)**, or
   copy it into the agent plug-in directory by hand. Without the bakery, put it
   into `plugins/900/` on Linux so it runs asynchronously.
4. Run service discovery on the collector host, then let the piggyback hosts be
   created (DCD or CMDB Syncer) and discover them as well.

## Environment

The Linux plug-in honours two environment variables: `ARUBA_CENCLI` for a
different cencli path or wrapper command, and `ARUBA_CENCLI_TIMEOUT` for the
subprocess timeout (300 seconds by default). The Windows plug-in honours
`ARUBA_CENCLI`.
