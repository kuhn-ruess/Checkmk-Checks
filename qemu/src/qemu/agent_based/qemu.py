#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
"""Qemu / KVM check plugin."""
from cmk.agent_based.v2 import AgentSection, CheckPlugin, Metric, Result, Service, State


def parse_qemu(string_table):
    return string_table


def qemu_fix_vmname(name):
    if name.startswith("instance"):
        name.replace("instance", "i")
    return name


def discover_qemu(section):
    for line in section:
        if line[2] == "running":
            yield Service(item=qemu_fix_vmname(line[1]))


def _upper_levels(value):
    """Extract (warn, crit) from a SimpleLevels-shaped param, or None."""
    if not value or value[0] != "fixed":
        return None
    return value[1]


def check_qemu(item, params, section):
    perfdata = []
    for line in section:
        vm = qemu_fix_vmname(line[1])
        if vm != item:
            continue
        status = line[2]
        assigned_mem = line[3]
        infotext = ["Status: %s, id: %s" % (status, line[0])]
        state = State.CRIT
        if status == "running":
            state = State.OK
            current_cpu = int(round(float(line[4])))
            infotext.append("CPU: %s%%" % current_cpu)

            current_mem = int(round(float(line[5])))
            infotext.append("Memory: (assigned: %s MB, used: %s%%)" % (assigned_mem, current_mem))

            perfdata.append(("cpu_util", current_cpu))
            perfdata.append(("memory_usage", current_mem))

            cpu_state = State.OK
            mem_state = State.OK
            cpu_levels = _upper_levels(params.get("cpu"))
            if cpu_levels:
                cpu_warn, cpu_crit = cpu_levels
                if current_cpu >= cpu_crit:
                    cpu_state = State.CRIT
                elif current_cpu >= cpu_warn:
                    cpu_state = State.WARN
            mem_levels = _upper_levels(params.get("mem"))
            if mem_levels:
                mem_warn, mem_crit = mem_levels
                if current_mem >= mem_crit:
                    mem_state = State.CRIT
                elif current_mem >= mem_warn:
                    mem_state = State.WARN
            state = State.worst(mem_state, cpu_state)

        yield Result(state=state, summary=", ".join(infotext))
        for name, value in perfdata:
            yield Metric(name, value)


agent_section_qemu = AgentSection(
    name="qemu",
    parse_function=parse_qemu,
)


check_plugin_qemu = CheckPlugin(
    name="qemu",
    service_name="VM %s",
    discovery_function=discover_qemu,
    check_function=check_qemu,
    check_default_parameters={},
    check_ruleset_name="qemu",
)
