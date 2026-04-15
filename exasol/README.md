# Exasol appliance monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.3.0p30-blue)
<!-- compatibility-badges:end -->

Special agent for monitoring an Exasol appliance via its XML-RPC management API. Replaces the legacy Nagios plugins and collects node states, service health, per-database storage usage and backup expirations in a single pass, with all parameters configurable from WATO.

## How it works

The special agent [`agent_exasol`](src/exasol/libexec/agent_exasol) connects to `https://<user>:<password>@<host>/cluster1` via `xmlrpc.client.ServerProxy` and emits three agent sections:

- `<<<exasol_nodes>>>` — `<node> <status>` per cluster node.
- `<<<exasol_services>>>` — `<module> <state>` per cluster service.
- `<<<exasol_database>>>` — one block per database (`[[[name]]]`) with `usage`, `free`, and `backup_expiration` lines. The agent computes per-node free space by walking the storage volume layout and correcting for redundancy and other volumes; values are cached in `~/tmp/check_mk/exasol_<host>` for one hour to reduce RPC load.

Databases can be excluded with the special agent parameter `ignore_dbs`.

Check plugins:

- [`nodes.py`](src/exasol/agent_based/nodes.py) — `Node <name>` service, CRIT if not `Running`.
- [`services.py`](src/exasol/agent_based/services.py) — single `Services` aggregate, CRIT if any module is not `OK`.
- [`database.py`](src/exasol/agent_based/database.py) — `Database <name> usage`, levels either absolute bytes or percentage via the `exasol_database` ruleset.
- [`database_backup.py`](src/exasol/agent_based/database_backup.py) — `Database <name> backup`, CRIT if no valid backup exists, WARN if a remote base backup expires before its dependency.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/exasol/libexec/agent_exasol` | Special agent script (XML-RPC client). |
| `src/exasol/server_side_calls/exasol.py` | Builds the agent command line from WATO params. |
| `src/exasol/rulesets/special_agent.py` | WATO rule *Exasol via XMLAPI* (username, password, ignore list). |
| `src/exasol/rulesets/database.py` | WATO rule for database size thresholds. |
| `src/exasol/agent_based/nodes.py` | `Node <name>` check. |
| `src/exasol/agent_based/services.py` | `Services` check. |
| `src/exasol/agent_based/database.py` | `Database <name> usage` check. |
| `src/exasol/agent_based/database_backup.py` | `Database <name> backup` check. |
| `src/exasol/agent_based/utils/exasol.py` | Shared section parser. |
| `src/exasol/graphing/database.py` | Metric and graph definitions for database sizes. |

## Installation

1. Install the MKP on the Checkmk site.
2. Create the WATO rule *Setup -> Agents -> Other integrations -> Exasol via XMLAPI* for the appliance host and provide a user with read access to the management API.
3. Run service discovery.

## Configuration

Special agent rule: **Setup -> Agents -> Other integrations -> Exasol via XMLAPI**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `username` | String | Exasol management user (passed URL-encoded). |
| `password` | Password | Password for the user. |
| `ignore_dbs` | List of String | Database names to skip. |

Check parameter rule: **Service monitoring rules -> Databases -> Exasol database levels** (ruleset name `exasol_database`)

| Parameter | Type | Meaning |
| --- | --- | --- |
| `levels` | Cascading `absolute` or `percentage` | Upper levels on database persistent usage, either as bytes or percent. |

## Services & metrics

- `Node <name>` — OK only when node is `Running`.
- `Services` — single aggregate, CRIT on any non-OK module.
- `Database <name> usage` — metric `exasol_db_size` (bytes) or `exasol_db_size_perc` (%).
- `Database <name> backup` — CRIT if no usable backup, WARN if backup dependency ordering is broken.

## Known limitations

- The special agent currently hardcodes `VERIFY = True` while also setting `check_hostname = VERIFY`; TLS verification is not exposed as a WATO option.
- The `--ignore` argument is treated as an iterable by the agent without splitting the comma-joined value passed from `server_side_calls/exasol.py`, so the ignore list may not filter as expected with multiple entries.
- Partition size cache is keyed only by hostname under `~/tmp/check_mk/exasol_<host>` with a fixed 1 h TTL.
