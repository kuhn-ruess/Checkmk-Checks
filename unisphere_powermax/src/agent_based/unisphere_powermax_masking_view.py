#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#<<unisphere_powermax_port:sep(30)>>>
#SYMMETRIX_SYMMETRIX_000297900498-RZ1_FA-3D:6{u'symmetrixPort': {u'volume_set_addressing': False, u'scsi_support1': True, u'unique_wwn': True, u'portgroup': [u'PG1', u'PG4'], u'sunapee': False, u'scsi_3': True, u'avoid_reset_broadcast': False, u'wwn_node': u'50000975b007c884', u'common_serial_number': True, u'environ_set': False, u'num_of_mapped_vols': 69, u'aclx': True, u'port_status': u'ON', u'type': u'FibreChannel (563)', u'hp_3000_mode': False, u'disable_q_reset_on_ua': False, u'spc2_protocol_version': True, u'num_of_masking_views': 23, u'enable_auto_negotive': True, u'symmetrixPortKey': {u'portId': u'6', u'directorId': u'FA-3D'}, u'max_speed': u'32', u'vnx_attached': False, u'director_status': u'Online', u'maskingview': [u'mv_sapvbp', u'mv_sapkons_sapdbms', u'mv_saptest', u'mv_vmware-mig1', u'mv_d11ovirtnode06_boot', u'mv_ucs-ext1', u'mv_ucs-dev1', u'mv_mssql', u'mv_sapkons', u'mv_ucs-rhel1', u'mv_d11ovirtnode04_boot', u'mv_ucs_sap1', u'mv_s13esx44', u'mv_ucs-prod4', u'mv_s13esx45', u'mv_d11ovirtnode03_boot', u'mv_ucs-prod1', u'mv_ovirt_cluster_dev_02', u'mv_inf1', u'mv_zks1', u'mv_ora1', u'mv_ovirt_cluster_dev_01', u'mv_d11ovirtnode05_boot'], u'siemens': False, u'soft_reset': False, u'num_of_port_groups': 2, u'negotiated_speed': u'32', u'negotiate_reset': False, u'num_of_cores': 8, u'identifier': u'50000975b007c886', u'no_participating': False, u'init_point_to_point': True}}

import json
import functools
import operator
from pprint import pprint

from .agent_based_api.v1 import (
    register,
    Service,
    Result,
    State,
    Metric,
)


def discover_masking_view_port_summary(section):
    items = []
    for port in section:
        sym_prefix = '_'.join(port[0].split('_')[0:-1])
        for mv in json.loads(port[1]).get('maskingview', []):
            items.append(('{}_{}'.format(sym_prefix, mv), sym_prefix, mv))

    for i in set(items):
        yield Service(item=i[0], parameters={'symId': i[1], 'maskingView': i[2]})
        

def check_masking_view_port_summary(item, params, section):
    n_ports = 0
    n_online_ports = 0

    for i in section:
        if not params['symId'] in i[0] :
            continue
        json_data = json.loads(i[1])
        if params['maskingView'] not in  json_data.get('maskingview', []):
            continue

        n_ports += 1
        if json_data.get('director_status', 'unkn') == 'Online':       
            n_online_ports += 1
        #if json_data.get('port_status', 'unkn') == 'ON':       
        #    n_online_ports += 1

    

    state = State.OK
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

def discover_masking_view_volume_summary(section):
    items = []
    for volume in section:
        sym_prefix = '_'.join(volume[0].split('_')[0:-1])
        mv = json.loads(volume[1]).get('maskingView', None)
        if mv is not None:
            items.append(('{}_{}'.format(sym_prefix, mv), sym_prefix, mv))

    for i in set(items):
        yield Service(item=i[0], parameters={'symId': i[1], 'maskingView': i[2]})
        

def check_masking_view_volume_summary(item, params, section):
    n_volumes = 0
    n_ready_volumes = 0

    for i in section:
        if not params['symId'] in i[0] :
            continue
        json_data = json.loads(i[1])
        if json_data.get('maskingView', None) != params['maskingView']:
            continue

        n_volumes += 1
        if json_data.get('status', 'unkn') == 'Ready':       
            n_ready_volumes += 1

    

    state = State.OK
    if n_volumes == 0:
       yield Result(state=State.UNKNOWN, summary="got no data from agent")
       return

    p_online = round(float(n_ready_volumes)/float(n_volumes)*100, 2)
    
    info_text = "volumes online: %s%% %s/%s (warn/crit <%s%%/<%s%%)" % ((p_online, n_ready_volumes, n_volumes) + params['levels'])
    if p_online < params['levels'][1]:
        state = State.CRIT
    elif p_online < params['levels'][0]:
        state = State.WARN
    perfdata = [('percent_volumes_online', "{}%".format(p_online), params['levels'][0], params['levels'][1]),
                ('absolute_volumes_online', "{}%".format(n_ready_volumes), float(params['levels'][0])/100.0*n_volumes, float(params['levels'][1])/100.0*n_volumes)]

    yield Metric(name='percent_volumes_online',
                 value=p_online,
                 levels=(params['levels'][0], params['levels'][1]),
                 boundaries=(0, 100))
    yield Metric(name='absolute_volumes_online',
                 value=n_ready_volumes,
                 levels=(float(params['levels'][0])/100.0*n_volumes, float(params['levels'][1])/100.0*n_volumes))

    yield Result(state=state, summary=info_text)

    

register.check_plugin(
    name = "unisphere_powermax_port_masking_view_port_summary",
    sections = ['unisphere_powermax_port'],
    service_name = 'Masking View Port Summary %s',
    discovery_function = discover_masking_view_port_summary,
    check_function = check_masking_view_port_summary,
    check_ruleset_name="unisphere_powermax_masking_view_port_summary",
    check_default_parameters = {"levels": (100, 50)}
)

register.check_plugin(
    name = "unisphere_powermax_volume_masking_view_volume_summary",
    sections = ['unisphere_powermax_volume'],
    service_name = 'Masking View Volume Summary %s',
    discovery_function = discover_masking_view_volume_summary,
    check_function = check_masking_view_volume_summary,
    check_ruleset_name="unisphere_powermax_masking_view_volume_summary",
    check_default_parameters = {"levels": (100, 100)}
)
