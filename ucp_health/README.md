# UCP / MKE Health Monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0-2f4f4f) ![packaged](https://img.shields.io/badge/packaged-2.4.0p19-blue)
<!-- compatibility-badges:end -->

Special agent that queries the Mirantis Kubernetes Engine (MKE / UCP) manager _ping endpoint of one or more nodes and reports the result as Checkmk local checks. Per-node "UCP Healthy" checks can be distributed to the node hosts via piggyback (opt-in), while an optional collection check ("UCP Manager") aggregates the nodes on the configured host and alerts once a configurable number of nodes is unhealthy.
