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


def parse_pure_arraydetails(string_table):
    section = {}

    for row in string_table:
        (item, data_reduction, total_reduction, shared_space, thin_provisioning, snapshots, volumes, size)  = row

        try:
            data_reduction=data_reduction
        except ValueError:
            data_reduction=0
        try:
            total_reduction=total_reduction
        except ValueError:
            total_reduction=0
        try:
            shared_space=int(shared_space)
        except ValueError:
            shared_space=0
        try:
            thin_provisioning=thin_provisioning
        except ValueError:
            thin_provisioning=0
        try:
            snapshots=int(snapshots)
        except ValueError:
            snapshots = 0
        try:
            volumes=int(volumes)
        except ValueError:
            volumes=0
        try:
            size=int(size)
        except ValueError:
            size=0

        section[item] = {
            'data_reduction': data_reduction,
            'total_reduction': total_reduction,
            'shared_space': shared_space,
            'thin_provisioning': thin_provisioning,
            'snapshots': snapshots,
            'volumes': volumes,
            'size': size,
        }

    return section


agent_section_pure_arraydetails = AgentSection(
    name="pure_arraydetails",
    parse_function=parse_pure_arraydetails,
)


def discover_pure_arraydetails(section):
    for item in section.keys():
        yield Service(item=item)

def check_pure_arraydetails(item, section):
    failed = []

    if item not in section.keys():
        yield Result(
            state=State.UNKNOWN,
            summary=f"Item {item} not found",
        )

    else:
        data = section[item]
        fs_snapshots:int=data['snapshots']
        fs_provisioning:int=data['volumes']
        fs_thin_provisioning=data['thin_provisioning']
        fs_size:int=data['size']

        yield Result(
            state=State.OK,
            summary=f"Provisioned Size: {bytes(fs_size)}, Used after deduplication: {bytes(fs_provisioning)}",
            details = f"Data Reduction: {data['data_reduction']} to 1 \n \
            Total reduction: {data['total_reduction']} to 1 \n \
            Thin Provisioned: {fs_thin_provisioning} \n \
            Snapshots: {bytes(fs_snapshots)}",
        )

        # Metrics
        yield Metric("pure_1_datareduction", float(data['data_reduction']))
        yield Metric("pure_2_totalreduction", float(data['total_reduction']))
        yield Metric("pure_3_thinprovisioned", float(fs_thin_provisioning))
        yield Metric("pure_4_snaphots", int(fs_snapshots))


check_plugin_pure_arraydetails = CheckPlugin(
    name="pure_arraydetails",
    sections=["pure_arraydetails"],
    service_name="Filesystem %s Details",
    discovery_function=discover_pure_arraydetails,
    check_function=check_pure_arraydetails,
)
