#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#<<<check_mk>>>
#Version: agent_unisphere_powermax-1.0
#<<<unisphere_powermax_health_check:sep(30)>>>
#{u'item_name': u'Vault State Test ', u'result': True}
#SYMMETRIX_000297900497-RZ2_Vault_State_Test{"item_name": "Vault State Test ", "result": true}
#{u'item_name': u'Spare Drives Test ', u'result': True}
#SYMMETRIX_000297900497-RZ2_Spare_Drives_Test{"item_name": "Spare Drives Test ", "result": true}
#{u'item_name': u'Memory Test ', u'result': True}
#SYMMETRIX_000297900497-RZ2_Memory_Test{"item_name": "Memory Test ", "result": true}
#{u'item_name': u'Locks Test ', u'result': True}
#SYMMETRIX_000297900497-RZ2_Locks_Test{"item_name": "Locks Test ", "result": true}
#{u'item_name': u'Emulations Test ', u'result': True}
#SYMMETRIX_000297900497-RZ2_Emulations_Test{"item_name": "Emulations Test ", "result": true}
#{u'item_name': u'Environmentals Test ', u'result': True}
#SYMMETRIX_000297900497-RZ2_Environmentals_Test{"item_name": "Environmentals Test ", "result": true}
#{u'item_name': u'Battery Test ', u'result': True}
#SYMMETRIX_000297900497-RZ2_Battery_Test{"item_name": "Battery Test ", "result": true}
#{u'item_name': u'General Test ', u'result': True}
#SYMMETRIX_000297900497-RZ2_General_Test{"item_name": "General Test ", "result": true}
#{u'item_name': u'DARE Test ', u'result': True}
#SYMMETRIX_000297900497-RZ2_DARE_Test{"item_name": "DARE Test ", "result": true}
#{u'item_name': u'Compression And Dedup Test ', u'result': True}
#SYMMETRIX_000297900497-RZ2_Compression_And_Dedup_Test{"item_name": "Compression And Dedup Test ", "result": true}

from .utils import parse_section
import time

from cmk.agent_based.v2 import (
    Service,
    Result,
    State,
    Metric,
    CheckPlugin,
    AgentSection,
)

agent_section_unispere_powermax_health_check = AgentSection(
    name="unisphere_powermax_health_check",
    parse_function=parse_section,
)

def discover_health(section):
    for item in section:
        yield Service(item=item)

def check_health(item, params, section):

    # @TODO untestet, no data
    health_data = section[item]

    state = State.OK
    info_text = ""
    
    info_text = "result: %s" % (health_data.get('result'))
    l = params.get('criticality', 'crit') 

    if health_data.get('result') != True:
        if l == 'warn':
           state = State.WARN
        else:
           state = State.CRIT

    
    
    check_age_h = (time.time() - health_data.get('date', 0)/1000.0)/60/60
    if check_age_h >= params.get('max_age', 168):
        state = State.UNKNOWN
        info_text = "health check is too old! age: %s >= %s hours" % (check_age_h, params.get('max_age', 168))

    perfdata = [('health_check_age', "{}h".format(check_age_h), health_data.get('result'))]
    yield Metric(name='health_check_age',
                 value=check_age_h)

    yield Result(state=state, summaary=info_text)
    
check_plugin_unisphere_powermax_health_check = CheckPlugin(
    name = "unisphere_powermax_health_check",
    service_name = 'Health Check %s',
    discovery_function = discover_health,
    check_function = check_health,
    check_ruleset_name='unisphere_powermax_health_check',
    check_default_parameters = {"max_age": 168}
)
