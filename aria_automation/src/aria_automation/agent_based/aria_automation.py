#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

import json

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Metric,
    Result,
    Service,
    State,
    StringTable,
    render,
)

HEALTH_STATES = {
    "healthy": State.OK,
    "degraded": State.WARN,
    "warning": State.WARN,
    "unknown": State.UNKNOWN,
}


def parse_json_section(string_table: StringTable):
    """Return the last valid JSON line (piggyback data may come from several nodes)."""
    for line in reversed(string_table):
        try:
            return json.loads(line[0])
        except (ValueError, IndexError):
            continue
    return None


agent_section_aria_automation_node = AgentSection(
    name="aria_automation_node",
    parse_function=parse_json_section,
)

agent_section_aria_automation_cluster = AgentSection(
    name="aria_automation_cluster",
    parse_function=parse_json_section,
)


def _health_result(health, message, prefix="Health"):
    """Map an Aria health value to a Result."""
    state = HEALTH_STATES.get(str(health).lower(), State.CRIT)
    text = f"{prefix}: {health or 'n/a'}"
    if message:
        text += f" ({message})"
    return Result(state=state, summary=text)


def _state_result(value, expected, prefix="State"):
    """OK if the state is the expected one, CRIT otherwise."""
    return Result(state=State.OK if value == expected else State.CRIT, summary=f"{prefix}: {value or 'n/a'}")


def _short(name):
    """First label of a node name."""
    return name.split(".")[0]


def discover_aria_automation_node(section) -> DiscoveryResult:
    """One summary service per node."""
    if section is not None:
        yield Service()


def check_aria_automation_node(section) -> CheckResult:
    """Show which cluster node this host is and how its instances are doing."""
    if section is None:
        return
    matched = section.get("matched")
    nodes = ", ".join(section.get("nodes") or []) or "none"
    if not matched:
        yield Result(
            state=State.CRIT,
            summary=f"Node name {section.get('node')} not found in cluster data",
            details=f"Nodes in cluster data: {nodes}. Set the node name in the special agent rule.",
        )
        return
    services = section.get("services") or {}
    bad = sorted(
        name for name, data in services.items()
        if data.get("state") != "running" or str(data.get("health")).lower() != "healthy"
    )
    yield Result(state=State.OK, summary=f"Node: {matched}")
    yield Result(state=State.OK, summary=f"{len(services)} service instances, {len(bad)} not running or not healthy")
    if bad:
        yield Result(state=State.OK, notice=f"Not running or not healthy: {', '.join(bad)}")
    yield Result(state=State.OK, notice=f"Cluster nodes: {nodes}")
    yield Metric("aria_instances", len(services))


check_plugin_aria_automation_node = CheckPlugin(
    name="aria_automation_node",
    service_name="Aria node",
    sections=["aria_automation_node"],
    discovery_function=discover_aria_automation_node,
    check_function=check_aria_automation_node,
)


def discover_aria_automation_service(section) -> DiscoveryResult:
    """One service per service instance running on this node."""
    if section is None:
        return
    for name in section.get("services") or {}:
        yield Service(item=name)


def check_aria_automation_service(item, params, section) -> CheckResult:
    """Check the instance of one service on this node."""
    if section is None:
        return
    data = (section.get("services") or {}).get(item)
    if data is None:
        if item in (section.get("elsewhere") or {}):
            nodes = ", ".join(_short(n) for n in section["elsewhere"][item]) or "no node"
            yield Result(
                state=State(params["missing_state"]),
                summary=f"No instance on this node, running on: {nodes}",
            )
        return
    yield _state_result(data.get("state"), "running")
    yield _health_result(data.get("health"), data.get("message"))
    yield Result(state=State.OK, summary=f"Category: {data.get('category') or 'n/a'}")
    resources = data.get("resources") or {}
    if "cpuPercents" in resources:
        yield Result(state=State.OK, notice=f"CPU: {render.percent(resources['cpuPercents'])}")
        yield Metric("aria_cpu_percent", resources["cpuPercents"])
    if "memoryBytes" in resources:
        yield Result(state=State.OK, notice=f"Memory: {render.bytes(resources['memoryBytes'])}")
        yield Metric("aria_memory_bytes", resources["memoryBytes"])
    if "diskBytes" in resources:
        yield Result(state=State.OK, notice=f"Disk: {render.bytes(resources['diskBytes'])}")
        yield Metric("aria_disk_bytes", resources["diskBytes"])


check_plugin_aria_automation_service = CheckPlugin(
    name="aria_automation_service",
    service_name="Aria service %s",
    sections=["aria_automation_node"],
    discovery_function=discover_aria_automation_service,
    check_function=check_aria_automation_service,
    check_ruleset_name="aria_automation_service",
    check_default_parameters={"missing_state": 1},
)


def discover_aria_automation_cluster(section) -> DiscoveryResult:
    """One service per cluster wide service."""
    if section is None:
        return
    for svc in section:
        yield Service(item=svc["name"])


def check_aria_automation_cluster(item, section) -> CheckResult:
    """Check the cluster wide state of one service and the state of its instances."""
    if section is None:
        return
    svc = next((s for s in section if s.get("name") == item), None)
    if svc is None:
        return
    yield _state_result(svc.get("state"), "started")
    yield _health_result(svc.get("health"), svc.get("message"))
    instances = svc.get("instances") or []
    nodes = ", ".join(_short(i.get("node", "")) for i in instances) or "none"
    yield Result(state=State.OK, summary=f"Instances: {len(instances)} ({nodes})")
    if not instances:
        yield Result(state=State.CRIT, summary="No service instance")
    for inst in instances:
        problems = []
        if inst.get("state") != "running":
            problems.append(f"state {inst.get('state') or 'n/a'}")
        if str(inst.get("health")).lower() != "healthy":
            problems.append(f"health {inst.get('health') or 'n/a'}")
        if problems:
            text = f"{_short(inst.get('node', ''))}: {', '.join(problems)}"
            if inst.get("message"):
                text += f" ({inst['message']})"
            yield Result(state=State.WARN, summary=text)
    yield Result(state=State.OK, notice=f"Category: {svc.get('category') or 'n/a'}, scope: {svc.get('scope') or 'n/a'}")
    yield Metric("aria_instances", len(instances))


check_plugin_aria_automation_cluster = CheckPlugin(
    name="aria_automation_cluster",
    service_name="Aria cluster service %s",
    sections=["aria_automation_cluster"],
    discovery_function=discover_aria_automation_cluster,
    check_function=check_aria_automation_cluster,
)
