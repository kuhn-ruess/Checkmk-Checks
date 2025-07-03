#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from .utils import parse_section

from cmk.agent_based.v2 import (
    Service,
    Result,
    State,
    Metric,
    CheckPlugin,
    AgentSection,
    check_levels,
)

agent_section_unispere_powermax_port_group = AgentSection(
    name="unisphere_powermax_port_group",
    parse_function=parse_section,
)

def discover_port_group_state(section):
    for item in section:
        yield Service(item=item)

def check_port_group_state(item, params, section):
    ports_data = section[item]


    # @TODO Cleanup these lines
    n_online_ports = len(list(filter(lambda x: x.get('symmetrixPort', {}).get('director_status') == 'Online', ports_data)))
    n_ports = len(list(filter(lambda x: x.get('symmetrixPort'), ports_data)))

    if n_ports == 0:
       yield Result(state=State.UNKNOWN, summary="got no data from agent")
       return

    p_online = round(float(n_online_ports)/float(n_ports)*100, 2)


    yield from check_levels(
       p_online,
       levels_lower=params['levels'],
       metric_name="percent_ports_online",
       label="Ports",
       render_func= lambda v: f"Ports Online: {n_online_ports}/{n_ports} ({v}%)"
    )
    yield Metric(name='absolute_ports_online',
                 value=n_online_ports)


check_plugin_unisphere_powermax_port_group_state = CheckPlugin(
    name = "unisphere_powermax_port_group_state",
    sections = ['unisphere_powermax_port_group'],
    service_name = 'Port Group %s',
    discovery_function = discover_port_group_state,
    check_function = check_port_group_state,
    check_ruleset_name="unisphere_powermax_port_group_state",
    check_default_parameters = {"levels": ('fixed', (80.0, 50.0))}
)

