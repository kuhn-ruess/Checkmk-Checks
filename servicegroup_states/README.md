# Checkmk Service Group States

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0-2f4f4f) ![packaged](https://img.shields.io/badge/packaged-2.5.0p13-blue)
<!-- compatibility-badges:end -->

Watches Checkmk service groups. Every service group whose name matches one of the configured patterns becomes its own service. That service alarms when either a single member, a configurable amount of members or *all* members of the group are in a problem state and/or stale.

## How it works

The special agent [`agent_servicegroup_states`](src/servicegroup_states/libexec/agent_servicegroup_states) runs on the Checkmk server and talks to the Livestatus socket of the site. It needs exactly **two queries per site**, independent of the number of monitored service groups:

1. `GET servicegroups` with `Filter: name ~ <pattern>` — name, alias and the state distribution (`num_services*`) of every matching group. Livestatus aggregates those counters itself, so nothing has to be counted on our side.
2. `GET services` with `Filter: state != 0` / `staleness >= <factor>` / `has_been_checked = 0` combined with `Filter: groups ~ <pattern>` — only the members which are actually not OK, stale or pending. Healthy members never travel over the socket.

Both filters are the *patterns*, not the resolved group names, so the query size depends on the number of patterns and not on the number of service groups. The results are emitted as one JSON line per service group in the `<<<servicegroup_states:sep(0)>>>` section.

The check plugin [`servicegroup_states.py`](src/servicegroup_states/agent_based/servicegroup_states.py) discovers one service `Service Group <name>` per group and evaluates two independent triggers on the member list.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/servicegroup_states/libexec/agent_servicegroup_states` | Special agent, minimal Livestatus client without Checkmk imports. |
| `src/servicegroup_states/server_side_calls/agent.py` | Builds the agent command line from the WATO parameters. |
| `src/servicegroup_states/rulesets/agent.py` | WATO rule *Checkmk service group states* (special agent). |
| `src/servicegroup_states/rulesets/check_parameters.py` | WATO rule *Checkmk service group states* (check parameters). |
| `src/servicegroup_states/agent_based/servicegroup_states.py` | Section parser, discovery and check. |
| `src/servicegroup_states/graphing/servicegroup_states.py` | Metrics, graph and perf-o-meter. |

## Installation

1. Install the MKP on the Checkmk site.
2. Create a host which represents the Checkmk site (the special agent runs on the Checkmk server, so the host only needs the tag *API integrations* / "No Checkmk agent, all configured special agents").
3. Create the rule *Setup -> Agents -> Other integrations -> Checkmk service group states* for that host and add at least one pattern.
4. Run service discovery.

## Configuration

### Special agent

Rule: **Setup -> Agents -> Other integrations -> Checkmk service group states**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `patterns` | List of regular expressions | Infix match against the service group names. `.*` monitors every service group. Required. |
| `staleness` | Float | Staleness factor from which on a member counts as stale. Same meaning as the global setting *Staleness value to force assume stale* (default `1.5`). |
| `sockets` | List of strings | One Livestatus socket per site, either a path or `tcp:<host>:<port>`. Empty means `$OMD_ROOT/tmp/run/live`. Results of all sites are merged per service group. |
| `timeout` | Integer seconds | Livestatus socket timeout (default `30`). |

### Check parameters

Rule: **Setup -> Service monitoring rules -> Checkmk service group states**

| Parameter | Meaning |
| --- | --- |
| `problem` | Trigger on members in a problem state. Contains `states` (any of WARN / CRIT / UNKNOWN, default CRIT + UNKNOWN), `mode` and the `result` state (default CRIT). Remove the whole section to switch the trigger off. |
| `stale` | Trigger on stale members. Contains `mode` and the `result` state (default WARN). Remove the whole section to switch the trigger off. |
| `only_hard_states` | Ignore members which are still in a soft state (default on). Applies to the problem trigger only. |
| `ignore_acknowledged` | Do not count members with an acknowledged problem (default off). |
| `ignore_downtime` | Do not count members in a scheduled downtime (default on). |
| `empty_group` | State when the group reports no members at all (default WARN). |

Both triggers use the same `mode` choices:

- **One member is enough** — alarm as soon as a single member is affected.
- **All members have to be affected** — alarm only when every member of the group is affected.
- **At least this many members** — absolute number.
- **At least this share of the members** — percentage of the group size.

The two triggers are evaluated independently and the worst resulting state wins, so a group can go WARN because of stale members and CRIT because of failed members at the same time.

## Services & metrics

**`Service Group <name>`**

- Summary: group size plus, per triggered rule, how many of the members are affected.
- Details: the state distribution of the group and the affected members with host, service, state, flags (stale, pending, acknowledged, downtime, soft) and the member's plug-in output (truncated, without the Checkmk state markers). At most 25 members are listed.
- Metrics: `servicegroup_services` (group size), `servicegroup_services_problem`, `servicegroup_services_stale`.

## Notes

- Service groups without members do not exist in Livestatus. If a monitored group loses all of its members, its service reports *item not found* (UNKNOWN) instead of hitting the `empty_group` state.
- A member which belongs to several monitored groups is evaluated in each of them.
