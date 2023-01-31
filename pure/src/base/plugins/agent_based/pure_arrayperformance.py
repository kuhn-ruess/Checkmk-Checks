# 2021 created by Sven Rueß, sritd.de
# 2023 reworked by Carlo Kleinloog
#/omd/sites/BIS/local/lib/python3/cmk/base/plugins/agent_based

from .agent_based_api.v1 import (
    register,
    Service,
    Result,
    State,
    Metric,
    render,
)

def parse_pure_arrayperformance(string_table):
    section = {}
    for row in string_table:
        (item,
        reads_per_sec,
        writes_per_sec,
        output_per_sec,
        input_per_sec,
        usec_per_read_op,
        usec_per_write_op)  = row

        section[item] = {
            'reads_per_sec': reads_per_sec,
            'writes_per_sec': writes_per_sec,
            'output_per_sec': output_per_sec,
            'input_per_sec': input_per_sec,
            'usec_per_read_op': usec_per_read_op,
            'usec_per_write_op': usec_per_write_op,        
        }
    return section

register.agent_section(
    name="pure_arrayperformance",
    parse_function=parse_pure_arrayperformance,
)

def discovery_pure_arrayperformance(section):
    for item in section.keys():
        yield Service(item=item)

def check_pure_arrayperformance(item, section):
    failed = []

    if item not in section.keys():
        yield Result(
            state=State.UNKNOWN,
            summary=f"Item {item} not found",
        )

    data = section[item]
    disk_read_ios = (data['reads_per_sec'])
    disk_write_ios = (data['writes_per_sec'])
    disk_read_throughput = (data['output_per_sec'])
    disk_write_throughput = (data['input_per_sec'])
    disk_read_responsetime = (data['usec_per_read_op'])
    disk_write_responsetime = (data['usec_per_write_op'])
    perfdata = True

    if item in section.keys():
        yield Result(state=State.OK, notice = f"Read latency: {data['reads_per_sec']}\n \
            Write latency: {data['writes_per_sec']}\n \
            Flash Volume: Yes")

# Metrics
    if perfdata is True:
        yield Metric("disk_read_ios", int(disk_read_ios))
        yield Metric("disk_write_ios", int(disk_write_ios))
        yield Metric("disk_read_throughput", int(disk_read_throughput))
        yield Metric("disk_write_throughput", int(disk_write_throughput))
        yield Metric("read_latency", int(disk_read_responsetime))
        yield Metric("write_latency", int(disk_write_responsetime))
        state = State.OK
        message = f"Read: {render.bytes(data['output_per_sec'])}, Write: {render.bytes(data['input_per_sec'])}, Read operations: {data['reads_per_sec']}/s, Write operations: {data['writes_per_sec']}/s"
        yield Result(state=State(state), summary=message)


register.check_plugin(
    name="pure_arrayperformance",
    service_name="Filesystem %s Performance",
    discovery_function=discovery_pure_arrayperformance,
    check_function=check_pure_arrayperformance,
)
