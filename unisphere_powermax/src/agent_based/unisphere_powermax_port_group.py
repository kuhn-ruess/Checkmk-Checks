#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

import json
from pprint import pprint

from .agent_based_api.v1 import (
    register,
    Service,
    Result,
    State,
    Metric,
)

def discover_port_group_state(section):
    for i in section:
        j = json.loads(i[1])
        if len(j) != 0:
            yield Service(item=i[0])

def check_port_group_state(item, params, section):
    ports_info = list(filter(lambda x: x[0] == item, section))
    if len(ports_info) != 1:
        return

    ports_data = json.loads(ports_info[0][1])

    #n_online_ports = len(filter(lambda x: x.get('symmetrixPort', {}).get('port_status', None) == 'ON', ports_data))
    n_online_ports = len(list(filter(lambda x: x.get('symmetrixPort', {}).get('director_status', None) == 'Online', ports_data)))
    n_ports = len(list(filter(lambda x: x.get('symmetrixPort', None) is not None, ports_data)))


    state = State.OK
    info_text = ""

    if n_ports == 0:
       yield Result(state=State.UNKNOWN, summary="got no data from agent")
       return

    p_online = round(float(n_online_ports)/float(n_ports)*100, 2)
    
    info_text = "ports online: %s%% %s/%s (warn/crit <%s%%/<%s%%)" % ((p_online, n_online_ports, n_ports) + params['levels'])
    if p_online < params['levels'][1]:
        state = State.CRIT
    elif p_online < params['levels'][0]:
        state = State.WARN
    yield Metric(name='percent_ports_online',
                 value=p_online,
                 levels=(params['levels'][0], params['levels'][1]),
                 boundaries=(0, 100))
    yield Metric(name='absolute_ports_online',
                 value=n_online_ports,
                 levels=(float(params['levels'][0])/100.0*n_ports, float(params['levels'][1])/100.0*n_ports))

    yield Result(state=state, summary=info_text)

register.check_plugin(
    name = "unisphere_powermax_port_group_state",
    sections = ['unisphere_powermax_port_group'],
    service_name = 'Port Group %s',
    discovery_function = discover_port_group_state,
    check_function = check_port_group_state,
    check_ruleset_name="unisphere_powermax_port_group_state",
    check_default_parameters = {"levels": (80.0, 50.0)}
)

