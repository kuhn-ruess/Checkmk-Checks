# VMware Aria Automation cluster services

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0-2f4f4f) ![packaged](https://img.shields.io/badge/packaged-2.5.0p16-blue)
<!-- compatibility-badges:end -->

Special agent for VMware Aria Automation. It queries `/api/v1/services/cluster` (port 8008)
on a node and monitors the Kubernetes services of the appliance cluster: the service
instances of the queried node on the node host, the cluster wide service state on a
separate cluster host.

## How it works

Every node answers `/api/v1/services/cluster` with the same data: all services of the cluster,
each with its instances on all nodes (`serviceInstances[].nodeName`). The special agent runs on
each node host, queries that node and picks its instances by the node name:

* node name = host name by default, or set in the rule
* compared case insensitive, first the full name, then the first label (a host `node1`
  matches the node `node1.example.com`)

Sections and services:

| Section | Host | Services |
| --- | --- | --- |
| `aria_automation_node` | node host | `Aria node` (which node, instance count), `Aria service <name>` per instance on this node |
| `aria_automation_cluster` | cluster host (piggyback) or node host | `Aria cluster service <name>` per service of the cluster |

| Case | State |
| --- | --- |
| Instance state other than `running` | CRIT |
| Cluster service state other than `started` | CRIT |
| Health `healthy` / `degraded`, `warning` / `unknown` / anything else | OK / WARN / UNKN / CRIT |
| Instance not running or not healthy (on the cluster service) | WARN |
| Service still in the cluster but no instance on this node | WARN (rule `VMware Aria Automation node service`) |
| Node name not found in the cluster data | CRIT on `Aria node`, lists the reported node names |

CPU, memory and disk per instance are stored as metrics as far as Aria reports them.

## Setup

1. Install the MKP.
2. Node hosts: data source `Configured API integrations, no Checkmk agent`.
3. Rule **VMware Aria Automation cluster services** (Applications) for all node hosts:
   protocol and port (default `http`, `8008`), optional address, node name, TLS verification,
   timeout, and **Send cluster wide services to host**.
4. Cluster host (for example the host of the cluster address): data source
   `No API integrations, no Checkmk agent`, piggyback `Always use and expect piggyback data`.
   All nodes deliver the cluster data, so it stays fresh while a node is down.
5. Service discovery on the node hosts first, then on the cluster host.

Without a cluster host the cluster wide services are created on every node host.

## Test data

| File | Content |
| --- | --- |
| `testdata/services_cluster.json` | answer of a healthy three node cluster |
| `testdata/services_cluster_failures.json` | same with a degraded service, a pending instance, a stopped service and a moved single instance |
