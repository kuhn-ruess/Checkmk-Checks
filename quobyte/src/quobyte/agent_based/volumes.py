#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Result,
    Service,
    State,
    Metric,
    render,
)


def parse_quobyte_volumes(string_table):
    """
    Parse lines into dict
    """
    parsed = {}

    for line in string_table:
        if len(line) == 1:
            current_volume = line[0]
            parsed.setdefault(current_volume, {})
        else:
            parsed[current_volume][line[0]] = int(line[1])
    return parsed


def discover_quobyte_volumes(section):
    """
    Discover one Service
    """
    for volume in section:
        yield Service(item=volume)


def check_levels(current, levels):
    """
    Helper
    """
    warn, crit = levels
    if current >= crit:
        return State.CRIT
    elif current >= warn:
        return State.WARN
    return State.OK


def check_quobyte_volumes(item, params, section):
    """
    Check single Volume
    """
    data = section[item]
    state = State.OK

    if 'used_allocated_space_bytes' in data:
        if levels := params.get('used_allocated_space_bytes'):
            state = check_levels(data['used_allocated_space_bytes'], levels)

        yield Result(state=state, summary=f"Disk Used {render.bytes(data['used_allocated_space_bytes'])}")
        yield Metric("disk_used", data['used_allocated_space_bytes'])

    if 'file_count' in data:
        if levels := params.get('file_count'):
            state = check_levels(data['file_count'], levels)
        yield Result(state=state, summary=f"Files Used {data['file_count']}")
        yield Metric("files_total", data['file_count'])

    if 'directory_count' in data:
        if levels := params.get('directory_count'):
            state = check_levels(data['directory_count'], levels)
        yield Result(state=state, summary=f"Directories Used {data['directory_count']}")
        yield Metric("directories_total", data['directory_count'])

    if 'used_logical_space_bytes' in data:
        if levels := params.get('used_logical_space_bytes'):
            state = check_levels(data['used_logical_space_bytes'], levels)
        yield Result(state=state, summary=f"Logical Used {render.bytes(data['used_logical_space_bytes'])}")
        yield Metric("logical_used", data['used_logical_space_bytes'])

    if 'used_disk_space_bytes' in data:
        if levels := params.get('used_disk_space_bytes'):
            state = check_levels(data['used_disk_space_bytes'], levels)
        yield Result(state=state, summary=f"Physical Used {render.bytes(data['used_disk_space_bytes'])}")
        yield Metric("physical_used", data['used_disk_space_bytes'])


agent_section_quobyte_volumes = AgentSection(
    name = "quobyte_volumes",
    parse_function = parse_quobyte_volumes,
)


check_plugin_quobyte_volumes = CheckPlugin(
    name = "quobyte_volumes",
    sections = ["quobyte_volumes"],
    service_name = "Volume %s",
    discovery_function = discover_quobyte_volumes,
    check_function = check_quobyte_volumes,
    check_default_parameters = {},
    check_ruleset_name = "quobyte_volumes",
)
