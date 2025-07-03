#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#<<<unisphere_powermax_director:sep(30)>>>
#SYMMETRIX_000297900498-RZ1_DF-1C{"num_of_ports": 4, "directorId": "DF-1C", "num_of_cores": 10, "director_slot_number": 1, "availability": "Online", "director_number": 33}
#SYMMETRIX_000297900498-RZ1_DF-2C{"num_of_ports": 4, "directorId": "DF-2C", "num_of_cores": 10, "director_slot_number": 2, "availability": "Online", "director_number": 34}
#SYMMETRIX_000297900498-RZ1_DF-3C{"num_of_ports": 4, "directorId": "DF-3C", "num_of_cores": 11, "director_slot_number": 3, "availability": "Online", "director_number": 35}
#SYMMETRIX_000297900498-RZ1_DF-4C{"num_of_ports": 4, "directorId": "DF-4C", "num_of_cores": 11, "director_slot_number": 4, "availability": "Online", "director_number": 36}
#SYMMETRIX_000297900498-RZ1_ED-1B{"num_of_ports": 0, "directorId": "ED-1B", "num_of_cores": 15, "director_slot_number": 1, "availability": "Online", "director_number": 17}

import json


from .utils import parse_section

from cmk.agent_based.v2 import (
    Service,
    Result,
    State,
    Metric,
    CheckPlugin,
    AgentSection,
)

agent_section_unispere_powermax_director = AgentSection(
    name="unisphere_powermax_director",
    parse_function=parse_section,
)

def discover_director_status(section):
    for item, data in section.items():
        if data.get('availability'):
            yield Service(item=item)

def check_director_status(item, params, section):

    director_info = section[item]
    status = director_info.get('availability')
    if not status:
       yield Result(state=State.UNKNOWN, summary="got no data from agent")
       return

    state = State.OK
    info_text = "director status: %s" % (status)
    if status.lower() != 'online':
        state = State.CRIT
    yield Result(state=state, summary=info_text)

check_plugin_unisphere_powermax_director_status = CheckPlugin(
    name = "unisphere_powermax_director_status",
    sections = ['unisphere_powermax_director'],
    service_name = 'Director Status %s',
    discovery_function = discover_director_status,
    check_function = check_director_status,
    check_default_parameters =  {}
)
