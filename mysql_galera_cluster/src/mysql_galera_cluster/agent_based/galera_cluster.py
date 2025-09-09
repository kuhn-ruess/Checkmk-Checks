#!/usr/bin/env python3
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
import time

from cmk.agent_based.v2 import (
    CheckPlugin,
    Metric,
    Result,
    Service,
    State,
)


def parse_mysql_galera(string_table):
    def parse_line(line):
       if len(line) == 2:
           varname, value = line
           try:
               value = int(value)
           except:
                pass
       else:
           varname = line[0]
           value = None
       return varname, value

    parsed = {}
    instance = False
    for line in info:
        if line[0].startswith("[["):
            instance = line[0][2:-2]
            if instance == "":
                instance = "mysql"
            parsed[instance] = {}
        elif instance:
            varname, value = parse_line(line)
            parsed[instance][varname] = value

    # Old Agent Plugin, no Instances in output
    if not instance:
        parsed['mysql'] = {}
        for line in info:
            varname, value = parse_line(line)
            parsed['mysql'][varname] = value

    return parsed


def discover_mysql_galera(section):
    """
    Discover Mysql Galera
    """
    for instance, values in section.items():
        if 'wsrep_provider_name' in values and values['wsrep_provider_name']:
            if 'galera' in values['wsrep_provider_name'].lower():
                yield Service(item=instance)


# set ok_code checks if the ok_code is higher
def set_ok_code(current_ok_code=int(), new_ok_code=int()):
    ok_code = current_ok_code
    if new_ok_code > ok_code:
        ok_code = new_ok_code

    return ok_code


def check_galera_cluster_state(item, params, section):
    """
    Check Galera Cluster
    """

    # check if agent output is available
    if item not in parsed:
        yield Result(state=State.Unknown, summary=f"Could not find instance {item}")
        return

    expected, warn, crit = params.get('wsrep_cluster_size')
    if 'wsrep_cluster_size' not in parsed[item]:
        yield Result(state=State.Unknown, summary="Could not find 'wsrep_cluster_size' in agent output")
    elif int(parsed[item]['wsrep_cluster_size']) <= int(crit):
        yield Result(state=State.Critical, summary=f"Size: {parsed[item]['wsrep_cluster_size']} expected {expected} crit at {crit} (!!)")
    elif int(parsed[item]['wsrep_cluster_size']) <= int(warn):
        yield Result(state=State.Warn, summary=f"Size: {parsed[item]['wsrep_cluster_size']} expected {expected} warn at {warn} (!)")
    else:
        yield Result(state=State.OK, summary=f"Size: {parsed[item]['wsrep_cluster_size']} expected {expected}")

    if 'wsrep_cluster_status' not in parsed[item]:
        yield Result(state=State.Unknown, summary="Could not find 'wsrep_cluster_status' in agent output")
    elif str(parsed[item]['wsrep_cluster_status']) == str(params.get('wsrep_cluster_status')):
        yield Result(state=State.OK, summary=f"Status: {parsed[item]['wsrep_cluster_status']}")
    else:
        yield Result(state=State.Critical, summary=f"Status: {parsed[item]['wsrep_cluster_status']} (!!)")

    if 'wsrep_cluster_conf_id' not in parsed[item]:
        yield Result(state=State.Critical, summary="Could not find 'wsrep_cluster_conf_id' in agent output")
    else:
        yield Result(state=State.OK, summary=f"ConfID: {parsed[item]['wsrep_cluster_conf_id']}")

    if 'wsrep_cluster_state_uuid' not in parsed[item]:
        yield Result(state=State.Critical, summary="Could not find 'wsrep_cluster_state_uuid' in agent output")
    else:
        yield Result(state=State.OK, summary=f"UUID: {parsed[item]['wsrep_cluster_state_uuid']}")

check_plugin_mysql_status = CheckPlugin(
    name = "mysql_galera_cluster_cluster_state",
    sections = ["mysql"],
    service_name = "MySQL Galera Cluster State %s",
    discovery_function = discover_mysql_galera,
    check_function = check_galera_cluster_state,
    check_default_parameters = {
        'wsrep_cluster_size': (3, 2, 2),
        'wsrep_cluster_status': "Primary",
    },
    check_ruleset_name = "galera_cluster_state",
)


def check_galera_node_state(item, params, section):
    """
    Check Galera Node State
    """
    # check if agent output is available
    if item not in parsed:
        yield Result(state=State.Unknown, summary=f"Could not find instance '{item}' in agent output")
        return

    if 'wsrep_ready' not in parsed[item]:
        yield Result(state=State.Unknown, summary="Could not find 'wsrep_ready' in agent output")
    elif str(parsed[item]['wsrep_ready']) == str(params.get('wsrep_ready')):
        yield Result(state=State.OK, summary=f"Ready: {parsed[item]['wsrep_ready']}")
    else:
        yield Result(state=State.Critical, summary=f"Ready: {parsed[item]['wsrep_ready']} (!!)")

    if 'wsrep_connected' not in parsed[item]:
        yield Result(state=State.Unknown, summary="Could not find 'wsrep_connected' in agent output")
    elif str(parsed[item]['wsrep_connected']) == str(params.get('wsrep_connected')):
        yield Result(state=State.OK, summary=f"Connected: {parsed[item]['wsrep_connected']}")
    else:
        yield Result(state=State.Critical, summary=f"Connected: {parsed[item]['wsrep_connected']} (!!)")

    if 'wsrep_local_state_comment' not in parsed[item]:
        yield Result(state=State.Unknown, summary="Could not find 'wsrep_local_state_comment' in agent output")
    elif str(parsed[item]['wsrep_local_state_comment']) == str(params.get('wsrep_local_state_comment')):
        yield Result(state=State.Critical, summary=f"State: {parsed[item]['wsrep_local_state_comment']} (!!)")
    else:
        yield Result(state=State.OK, summary=f"State: {parsed[item]['wsrep_local_state_comment']}")

check_plugin_mysql_status = CheckPlugin(
    name = "mysql_galera_cluster_node_state",
    sections = ["mysql"],
    service_name = "MySQL Galera Node State %s",
    discovery_function = discover_mysql_galera,
    check_function = check_galera_node_state,
    check_default_parameters = {
        'wsrep_ready': 'ON',
        'wsrep_connected': 'ON',
        'wsrep_local_state_comment': 'Initialized',
    },
    check_ruleset_name = "galera_node_state",
)


def check_galera_repl_health(item, params, section):
    """
    Check Galera Repl Health
    """
    cur_time = time.time()

    # check if agent output is available
    if item not in parsed:
        yield Result(state=State.Unknown, summary=f"Could not find instance '{item}' in agent output")
        return

    # wsrep_local_recv_queue_avg
    warn, crit = params.get('wsrep_local_recv_queue_avg')
    if 'wsrep_local_recv_queue_avg' not in parsed[item]:
        yield Result(state=State.Unknown, summary="Could not find 'wsrep_local_recv_queue_avg' in agent output")
    elif float(parsed[item]['wsrep_local_recv_queue_avg']) >= float(crit):
        yield Result(state=State.Critical, summary=f"RecvQ avg: {round(float(parsed[item]['wsrep_local_recv_queue_avg']), 2)} crit at: {crit} (!!)")
    elif float(parsed[item]['wsrep_local_recv_queue_avg']) >= float(warn):
        yield Result(state=State.Warn, summary=f"RecvQ avg: {round(float(parsed[item]['wsrep_local_recv_queue_avg']), 2)} warn at: {warn} (!)")
    else:
        yield Result(state=State.OK, summary=f"RecvQ avg: {round(float(parsed[item]['wsrep_local_recv_queue_avg']), 2)}")
    yield Metric("recv_queue_avg", float(parsed[item]['wsrep_local_recv_queue_avg']), levels=(warn, crit))
    yield Metric("recv_queue_max", float(parsed[item]['wsrep_local_recv_queue_max']))
    yield Metric("recv_queue_min", float(parsed[item]['wsrep_local_recv_queue_min']))
    yield Metric("recv_queue", float(parsed[item]['wsrep_local_recv_queue']))

    # wsrep_local_send_queue_avg
    warn, crit = params.get('wsrep_local_send_queue_avg')
    if 'wsrep_local_send_queue_avg' not in parsed[item]:
        yield Result(state=State.Unknown, summary="Could not find 'wsrep_local_send_queue_avg' in agent output")
    elif float(parsed[item]['wsrep_local_send_queue_avg']) >= float(crit):
        yield Result(state=State.Critical, summary=f"SendQ avg: {round(float(parsed[item]['wsrep_local_send_queue_avg']), 2)} crit at: {crit} (!!)")
    elif float(parsed[item]['wsrep_local_send_queue_avg']) >= float(warn):
        yield Result(state=State.Warn, summary=f"SendQ avg: {round(float(parsed[item]['wsrep_local_send_queue_avg']), 2)} warn at: {warn} (!)")
    else:
        yield Result(state=State.OK, summary=f"SendQ avg: {round(float(parsed[item]['wsrep_local_send_queue_avg']), 2)}")
    yield Metric("send_queue_avg", float(parsed[item]['wsrep_local_send_queue_avg']), levels=(warn, crit))
    yield Metric("send_queue_max", float(parsed[item]['wsrep_local_send_queue_max']))
    yield Metric("send_queue_min", float(parsed[item]['wsrep_local_send_queue_min']))
    yield Metric("send_queue", float(parsed[item]['wsrep_local_send_queue']))

    # wsrep_flow_control_paused
    warn, crit = params.get('wsrep_flow_control_paused')
    if 'wsrep_flow_control_paused' not in parsed[item]:
        yield Result(state=State.Unknown, summary="Could not find 'wsrep_flow_control_paused' in agent output")
    elif float(parsed[item]['wsrep_flow_control_paused']) >= float(crit):
        yield Result(state=State.Critical, summary=f"FlowCtrlPaused: {round(float(parsed[item]['wsrep_flow_control_paused']), 3)} crit at: {crit} (!!)")
    elif float(parsed[item]['wsrep_flow_control_paused']) >= float(warn):
        yield Result(state=State.Warn, summary=f"FlowCtrlPaused: {round(float(parsed[item]['wsrep_flow_control_paused']), 3)} warn at: {warn} (!)")
    else:
        yield Result(state=State.OK, summary=f"FlowCtrlPaused: {round(float(parsed[item]['wsrep_flow_control_paused']), 3)}")
    yield Metric("flow_control_paused", float(parsed[item]['wsrep_flow_control_paused']), levels=(warn, crit))

    flow_control_recv = get_rate("flow_control_recv", cur_time, float(parsed[item]['wsrep_flow_control_recv']))
    flow_control_sent = get_rate("flow_control_sent", cur_time, float(parsed[item]['wsrep_flow_control_sent']))
    yield Metric("flow_control_recv", float(flow_control_recv))
    yield Metric("flow_control_sent", float(flow_control_sent))

    yield Metric("cert_deps_distance", float(parsed[item]['wsrep_cert_deps_distance']))

check_plugin_mysql_status = CheckPlugin(
    name = "mysql_galera_cluster_repl_health",
    sections = ["mysql"],
    service_name = "MySQL Galera Replication Health %s",
    discovery_function = discover_mysql_galera,
    check_function = check_galera_repl_health,
    check_default_parameters = {
        'wsrep_local_recv_queue_avg':('fixed', (0.1, 0.2)),
        'wsrep_local_send_queue_avg':('fixed', (0.1, 0.2)),
        'wsrep_flow_control_paused': ('fixed',(0.5, 0.7)),
    },
    check_ruleset_name = "galera_repl_health",
)
