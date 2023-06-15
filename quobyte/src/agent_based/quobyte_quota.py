#!/usr/bin/env python3


from .agent_based_api.v1 import (
    register,
    Result,
    Service,
    State,
    render,
    Metric,
)

def parse_quobyte_quotas(string_table):
    """
    Parse Quota Data to Dict
    """
    parsed = {}
    item = None
    for line in string_table:
        if line[0].startswith('[[['):
            item = " ".join(line)[3:-3].lower()
            parsed[item] = {}
        else:
            parsed[item][line[0]] = line[1]
    return parsed



def discover_quobyte_quotas(section):
    """
    Discover one Service per Device
    """
    for quota in section:
        yield Service(item=quota)

def check_quobyte_quotas(item, params, section):
    """
    Check single Service
    """
    state = State.OK
    quota = section[item]
    limit = int(quota['limit'])
    used = int(quota['usage'])
    limit_type = quota['limit_type']
    percentage = int(round((used/limit) * 100,0))
    yield Result(state=state, summary=f"Quota usage: {render.bytes(used)} of {render.bytes(limit)} ({percentage} %)")
    yield Metric("quota_used_bytes", used)
    yield Metric("quota_limit_bytes", limit)

register.agent_section(
    name="quobyte_quotas",
    parse_function=parse_quobyte_quotas,
)

register.check_plugin(
    name="quobyte_quotas",
    sections=["quobyte_quotas"],
    service_name="Quota %s",
    discovery_function=discover_quobyte_quotas,
    check_function=check_quobyte_quotas,
    check_default_parameters={}
)
