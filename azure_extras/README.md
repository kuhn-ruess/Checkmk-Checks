# Additional Azure Monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0p18-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p18-blue)
<!-- compatibility-badges:end -->

Complementary special agent for Azure networking resources. Runs standalone or alongside the built-in Checkmk Azure integration and emits piggyback sections so extra services appear on the same hosts.

Covered resource types:

- Azure Firewalls (main, IP configs, rule collections, policies)
- Virtual Network Gateways (main, IP configs, BGP, VPN clients, remote peerings)
- Virtual Network Gateway Connections
- Virtual Networks (main, subnets, peerings)

## How it works

The special agent [`agent_azure_extra`](src/azure_extra/libexec/agent_azure_extra) authenticates against `login.microsoftonline.com` using a client credentials flow, enumerates resource groups via the Azure Resource Manager REST API, and then iterates over the supported resource types (see `RESOURCE_CONFIGS`). For each discovered resource it emits piggyback output (`<<<<<resource_name>>>>`) containing a JSON blob under section headers such as `<<<azure_extra_azurefirewalls:sep(0)>>>`, `<<<azure_extra_virtualnetworks:sep(0)>>>`, `<<<azure_extra_virtualnetworkgateways:sep(0)>>>` and `<<<azure_extra_connections:sep(0)>>>`.

The agent based plugins parse the JSON and create services based on `provisioningState`, SKU, BGP state, peering state, rule counts, etc. `Succeeded` maps to OK, `Failed` / `Canceled` to CRIT, anything else to WARN.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/azure_extra/libexec/agent_azure_extra` | Special agent script (REST client for Azure ARM). |
| `src/azure_extra/rulesets/agent.py` | WATO special agent rule. |
| `src/azure_extra/server_side_calls/agent.py` | Builds the command line for the special agent. |
| `src/azure_extra/agent_based/azure_extra_azurefirewalls.py` | Services for firewalls, IP configs, rule collections, policies. |
| `src/azure_extra/agent_based/azure_extra_virtualnetworks.py` | Services for virtual networks, subnets, peerings. |
| `src/azure_extra/agent_based/azure_extra_virtualnetworkgateways.py` | Services for VPN gateways, BGP, VPN clients, peerings. |
| `src/azure_extra/agent_based/azure_extra_connections.py` | Services for VPN gateway connections. |

## Installation

1. Install the MKP on the Checkmk site.
2. Create an Azure App Registration with read access on the relevant subscription (Reader role is typically sufficient for ARM metadata).
3. Create a dedicated host for the Azure tenant and attach the rule *KR Azure Extra* under *Setup -> Agents -> Other integrations*.
4. Make sure the Checkmk site can reach `login.microsoftonline.com` and `management.azure.com` (use the proxy option if required).

## Configuration

Rule: **Setup -> Agents -> Other integrations -> KR Azure Extra**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `tenant_id` | String | Azure Active Directory tenant ID. |
| `client_id` | String | App registration client ID. |
| `client_secret` | Password | App registration client secret. |
| `subscription_id` | String | Subscription to enumerate. |
| `proxy_url` | String (optional) | HTTP(S) proxy URL. |

## Services & metrics

Examples of service name patterns created by the check plugins:

- `Azure Firewall %s`, `Azure Firewall IP Config %s`, `Azure Firewall Rule Collection %s`, `Azure Firewall Policy %s`
- `Azure VNet %s`, `Azure VNet Subnet %s`, `Azure VNet Peering %s`
- `Azure VNet Gateway %s`, `Azure VNet Gateway BGP %s`, `Azure VNet Gateway VPN Client %s`, `Azure VNet Gateway Remote Peering %s`
- `Azure Connection %s`

State is derived from `provisioningState` and resource specific fields; these checks currently do not report numeric metrics.

## Known limitations

- Metric collection (`microsoft.insights/metrics`) is defined in the agent but commented out; only ARM property data is shipped.
- Hosts are identified via piggyback using Azure resource names, so they must exist as Checkmk hosts (or be auto-created) for services to appear.
