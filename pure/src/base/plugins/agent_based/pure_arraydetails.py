# 2021 created by Sven Rueß, sritd.de
# 2023 reworked by Carlo Kleinloog
# omd/sites/BIS/local/lib/python3/cmk/base/plugins/agent_based

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
    dedup_ratio = (data['data_reduction'])
    perfdata = True
    if item in section.keys():
        yield Result(
            state=State.OK,
            summary=f"Data Reduction: {data['data_reduction']} to 1, Total reduction: {(data['total_reduction'])} to 1, Shared Space: {render.bytes(data['shared_space'])}, Thin Provisioned: {data['thin_provisioning']}, Snapshots: {render.bytes(data['snapshots'])}",
            details=f"Used after deduplication: {render.bytes(data['volumes'])}",
        )

# Metrics
    if perfdata is True:
        yield Metric("dedup_ratio", float(dedup_ratio))


register.check_plugin(
    name="pure_arraydetails",
    service_name="Filesystem %s Details",
    discovery_function=discovery_pure_arraydetails,
    check_function=check_pure_arraydetails,
)
