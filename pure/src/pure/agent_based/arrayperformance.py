#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Metric,
    Result,
    Service,
    State,
)
from cmk.agent_based.v2.render import (
    bytes,
)


def parse_pure_arrayperformance(string_table):
    section = {}

    for row in string_table:
        item, reads_per_sec, writes_per_sec, output_per_sec, input_per_sec, usec_per_read_op, usec_per_write_op  = row

        section[item] = {
            'reads_per_sec': reads_per_sec,
            'writes_per_sec': writes_per_sec,
            'output_per_sec': output_per_sec,
            'input_per_sec': input_per_sec,
            'usec_per_read_op': usec_per_read_op,
            'usec_per_write_op': usec_per_write_op,
        }

    return section


agent_section_pure_arrayperformance = AgentSection(
    name="pure_arrayperformance",
    parse_function=parse_pure_arrayperformance,
)


def discover_pure_arrayperformance(section):
    for item in section.keys():
        yield Service(item=item)

def check_pure_arrayperformance(item, section):
    failed = []

    if item not in section.keys():
        yield Result(
            state=State.UNKNOWN,
            summary=f"Item {item} not found",
        )

    else:
        data=section[item]
        disk_read_ios=data['reads_per_sec']
        disk_write_ios=data['writes_per_sec']
        disk_read_throughput=data['output_per_sec']
        disk_write_throughput=data['input_per_sec']
        disk_read_responsetime=data['usec_per_read_op']
        disk_write_responsetime=data['usec_per_write_op']

        yield Result(state=State.OK, notice=f"Read latency: {data['reads_per_sec']}\n \
            Write latency: {data['writes_per_sec']}\n \
            Flash Volume: Yes")

        yield Result(
            state=State.OK,
            summary=f"Read: {bytes(data['output_per_sec'])}, Write: {bytes(data['input_per_sec'])}, Read operations: {data['reads_per_sec']}/s, Write operations: {data['writes_per_sec']}/s"
        )

        # Metrics
        yield Metric("disk_read_ios", int(disk_read_ios))
        yield Metric("disk_write_ios", int(disk_write_ios))
        yield Metric("disk_read_throughput", int(disk_read_throughput))
        yield Metric("disk_write_throughput", int(disk_write_throughput))
        yield Metric("read_latency", int(disk_read_responsetime))
        yield Metric("write_latency", int(disk_write_responsetime))


check_plugin_pure_arrayperformance = CheckPlugin(
    name="pure_arrayperformance",
    sections=["pure_arrayperformance"],
    service_name="Filesystem %s Performance",
    discovery_function=discover_pure_arrayperformance,
    check_function=check_pure_arrayperformance,
)
