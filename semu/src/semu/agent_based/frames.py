#!/usr/bin/env python3

'''
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de


<<<semu_frames>>>
mac_address D8:80:39:D3:DE:77
frames_processed 8354128
illumination SUFFICIENT
measured_sensor_direction [0.00884352, -0.00114911, -0.99996]
measured_alpha_deg -0.0658392
measured_beta_deg -0.506703
'''
import time

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Service,
    check_levels,
    Result,
    State,
    get_value_store,
    get_rate,
    check_levels,
)


def parse_function(string_table):
    '''
    Parse Device Data to Dict
    '''
    parsed = {}
    for line in string_table:
        parsed[line[0]] = line[1]
    return parsed


def discover_service(section):
    '''
    Discover
    '''
    yield Service()


def check_service(params,section):
    '''
    Check single Service
    '''
    current_frames = int(section['frames_processed'])
    now = time.time()
    rate = get_rate(get_value_store(), 'frames', now, current_frames)
    yield from check_levels(
            rate,
            levels_lower=params['levels'],
            metric_name='frames',
            label='Framerate',
            render_func=lambda v: f'{round(v, 2)} per sec',


        )

    yield Result(state=State.OK, summary=f'Illumniation: {section['illumination']}')


agent_section_cmdb_syncer_service = AgentSection(
    name = 'semu_frames',
    parse_function = parse_function,
)


check_plugin_cmdb_syncer_service = CheckPlugin(
    name = 'semu_frames',
    sections = ['semu_frames'],
    service_name = 'Framerate',
    discovery_function = discover_service,
    check_function = check_service,
    check_ruleset_name='semu_frames',
    check_default_parameters={
        'levels': ('fixed', (10, 5)),
    }
)
