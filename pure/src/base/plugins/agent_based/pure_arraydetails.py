
#2023 created by Carlo Kleinloog
#/omd/sites/BIS/local/lib/python3/cmk/base/plugins/agent_based
from cmk.base.check_api import get_bytes_human_readable, get_percent_human_readable

from .agent_based_api.v1 import (
    register,
    Service,
    Result,
    State,
    Metric,
    render,
)

def parse_pure_arraydetails(string_table):


    section = {}
    for row in string_table:
        (item,
        data_reduction,
        total_reduction,
        shared_space,
        thin_provisioning,
        snapshots,
        volumes) = row
    try:
        data_reduction = (data_reduction)
    except ValueError:
        data_reduction: Literal[0] = 0
    try:
        total_reduction = (total_reduction)
    except ValueError:
        total_reduction: Literal[0] = 0	 
    try:
        shared_space = int(shared_space)
    except ValueError:
        shared_space: Literal[0] = 0
    try:
        thin_provisioning = (thin_provisioning)
    except ValueError:
        thin_provisioning: Literal[0] = 0
    try:
        snapshots: int = int(snapshots)
    except ValueError:
        snapshots = 0
    try:
            volumes = int(volumes)
    except ValueError:
            volumes: Literal[0] = 0 

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

register.agent_section(
    name="pure_arraydetails",
    parse_function=parse_pure_arraydetails,
)

def discovery_pure_arraydetails(section):
    for item in section.keys():
        yield Service(item=item)

def check_pure_arraydetails(item, section):
    failed = []

    if item not in section.keys():
        yield Result(
            state=State.UNKNOWN,
            summary=f"Item {item} not found",
        )

    data = section[item]
    fs_snapshots:int=data['snapshots']
    fs_provisioning:int=data['volumes']
    fs_thin_provisioning=data['thin_provisioning']
    fs_size:int=data['size']

    if item in section.keys():
        yield Result(
            state=State.OK,
            summary=f"Provisioned Size: {get_bytes_human_readable(fs_size)}, Used after deduplication: {render.bytes(fs_provisioning)}",
            details = f"Data Reduction: {data['data_reduction']} to 1 \n \
            Total reduction: {data['total_reduction']} to 1 \n \
            Thin Provisioned: {fs_thin_provisioning} \n \
            Snapshots: {render.bytes(fs_snapshots)}",
            )
# Metrics
        yield Metric("pure_1_datareduction", float(data['data_reduction']))
        yield Metric("pure_2_totalreduction", float(data['total_reduction']))
        yield Metric("pure_3_thinprovisioned", float(fs_thin_provisioning))
        yield Metric("pure_4_snaphots", int(fs_snapshots))
    else:
        yield Result(
            state=State.CRIT,
            summary=f"Provisioned Size: {get_bytes_human_readable(fs_size)}, Used after deduplication: {render.bytes(fs_provisioning)}",
            details = f"Data Reduction: {data['data_reduction']} to 1 \n \
            Total reduction: {data['total_reduction']} to 1 \n \
            Thin Provisioned: {fs_thin_provisioning} \n \
            Snapshots: {render.bytes(fs_snapshots)}",
            )

# Metrics
        yield Metric("pure_1_datareduction", float(data['data_reduction']))
        yield Metric("pure_2_totalreduction", float(data['total_reduction']))
        yield Metric("pure_3_thinprovisioned", float(fs_thin_provisioning))
        yield Metric("pure_4_snaphots", int(fs_snapshots))

register.check_plugin(
    name="pure_arraydetails",
    service_name="Filesystem %s Details",
    discovery_function=discovery_pure_arraydetails,
    check_function=check_pure_arraydetails,
)
