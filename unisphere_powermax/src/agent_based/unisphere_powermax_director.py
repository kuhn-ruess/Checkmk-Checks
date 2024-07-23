#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#<<<unisphere_powermax_director:sep(30)>>>
#SYMMETRIX_000297900498-RZ1_DF-1C{"num_of_ports": 4, "directorId": "DF-1C", "num_of_cores": 10, "director_slot_number": 1, "availability": "Online", "director_number": 33}
#SYMMETRIX_000297900498-RZ1_DF-2C{"num_of_ports": 4, "directorId": "DF-2C", "num_of_cores": 10, "director_slot_number": 2, "availability": "Online", "director_number": 34}
#SYMMETRIX_000297900498-RZ1_DF-3C{"num_of_ports": 4, "directorId": "DF-3C", "num_of_cores": 11, "director_slot_number": 3, "availability": "Online", "director_number": 35}
#SYMMETRIX_000297900498-RZ1_DF-4C{"num_of_ports": 4, "directorId": "DF-4C", "num_of_cores": 11, "director_slot_number": 4, "availability": "Online", "director_number": 36}
#SYMMETRIX_000297900498-RZ1_ED-1B{"num_of_ports": 0, "directorId": "ED-1B", "num_of_cores": 15, "director_slot_number": 1, "availability": "Online", "director_number": 17}



import json
from pprint import pprint

from .agent_based_api.v1 import (
    register,
    Service,
    Result,
    State,
    Metric,
)

def discover_director_status(section):
    for i in section:
        j = json.loads(i[1])
        if j.get('availability', None) is not None:
            yield Service(item=i[0])

def check_director_status(item, params, section):
    director_info = list(filter(lambda x: x[0] == item, section))
    if len(director_info) != 1:
       yield Result(state=State.UNKNOWN, summary="got no data from agent")
       return

    director = director_info[0][0]
    director_data = json.loads(director_info[0][1])

    state = State.OK
  
    status = director_data.get('availability', None).lower()
    if status is None:
       yield Result(state=State.UNKNOWN, summary="got no data from agent")
       return
    
    info_text = "director status: %s" % (status)
    if status != 'online':
        state = State.CRIT

    yield Result(state=state, summary=info_text)

register.check_plugin(
    name = "unisphere_powermax_director_status",
    sections = ['unisphere_powermax_director'],
    service_name = 'Director Status %s',
    discovery_function = discover_director_status,
    check_function = check_director_status,
    check_default_parameters =  {}
)
