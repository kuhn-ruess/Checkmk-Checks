# Agent Based Docker Monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0p1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.3.0p25-blue)
<!-- compatibility-badges:end -->

Monitors Docker via an agent plugin that talks directly to the local Docker socket and reports one service per container, one per image, plus a daemon info service. Useful when a host runs a fixed set of containers and you want per-container state, CPU, memory and size metrics without relying on Checkmk's built-in Docker integration.

## How it works

The agent plugin [`check_docker.py`](src/agents/plugins/check_docker.py) connects to `unix://var/run/docker.sock` using the `docker` Python API, calls `info()`, `containers(all=True, size=True)` and `images(all=True)`, and emits three agent sections:

- `<<<docker_info:sep(59)>>>` — daemon status, version, image count, goroutines, fds, event listeners.
- `<<<docker_containers:sep(35)>>>` — one line per container with name, state, status, image, sizes, CPU/memory stats.
- `<<<docker_images:sep(35)>>>` — one line per image with image id and disk space.

If the container carries a `com.docker.swarm.service.name` label and piggyback mode is enabled, output for that container is wrapped in a piggyback block so services end up on a per-swarm-service host. Container labels can be whitelisted (with optional rewrite) so they become Checkmk service labels.

Check plugins:

- [`docker_info.py`](src/docker/agent_based/docker_info.py) — `Docker Info` service.
- [`docker_containers.py`](src/docker/agent_based/docker_containers.py) — `Docker Container <name>` service, CRIT if `State != running`, with CPU% and memory metrics.
- [`docker_images.py`](src/docker/agent_based/docker_images.py) — `Docker Image <tag>` service, aggregating CPU and memory of all running containers using that image.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/agents/plugins/check_docker.py` | Agent plugin shipped to Docker hosts. Requires `docker` Python package. |
| `src/docker/agent_based/docker_info.py` | Parser and check for `docker_info`. |
| `src/docker/agent_based/docker_containers.py` | Parser and check for `docker_containers` (CPU via `get_rate`, memory, size). |
| `src/docker/agent_based/docker_images.py` | Parser and check for `docker_images`. |
| `src/docker/agent_based/docker_utils.py` | Shared CPU helper (`get_docker_container_cpu`). |
| `src/docker/rulesets/rulesets.py` | Legacy WATO ruleset for the Bakery (interval, timeout, label filters, piggyback). |
| `src/docker/graphing/docker.py` | Metric and graph definitions. |
| `src/lib/python3/cmk/base/cee/plugins/bakery/docker.py` | Agent Bakery hook. |

## Installation

1. Install the MKP on the Checkmk site.
2. On each Docker host install the required Python package: `pip install docker` (version >= 6.1.0).
3. Deploy the plugin via the Bakery rule *Docker Agent Based (Linux)* (under Agent Plugins), or copy `check_docker.py` to `/usr/lib/check_mk_agent/plugins/` manually and create `/etc/check_mk/check_docker.cfg` if you need non-default timeout, whitelist, replacements or piggyback mode.
4. Run service discovery on the host.

## Configuration

Bakery rule: **Agent rules -> Docker Agent Based (Linux)**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `activated` | choice | Deploy the plugin or not. |
| `interval` | Age | Check / cache interval (default 120 s). |
| `timeout` | Age | Connection timeout to the Docker socket (default 30 s). |
| `label_whitelist` | list of strings | Labels to keep. Trailing `*` acts as a prefix match. |
| `label_replacements` | list of `(original, rewrite)` tuples | Rename labels before publishing as service labels. |
| `piggyback` | choice | Use `com.docker.swarm.service.name` as piggyback host. |

If you raise the polling interval, adjust *Normal check interval for service checks* accordingly so Checkmk does not outrun the cached agent output.

## Services & metrics

- **`Docker Info`** — state, version, images, goroutines, file descriptors, events listeners.
- **`Docker Container <name>`** — CRIT if not `running`; metrics `CPU_pct`, `Memory_used`, `Memory_limit`, `SizeRootFs`, `SizeRw`; CPU utilization is derived through `get_rate` on cumulative container and system CPU ticks.
- **`Docker Image <repo:tag>`** — `Running_containers`, `Diskspace_used`, aggregated `CPU_pct` and `Memory_used`.

## Known limitations

- The Bakery ruleset uses the legacy pre-2.3 WATO API (`rulespec_registry`, `HostRulespec`); it will need porting if that API is removed.
- The agent plugin requires the `docker` PyPI package installed on every monitored host.
