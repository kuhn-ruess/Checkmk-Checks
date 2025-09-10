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
    check_levels,
    get_rate,
    get_value_store,
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

    section = {}
    instance = False
    for line in info:
        if line[0].startswith("[["):
            instance = line[0][2:-2]
            if instance == "":
                instance = "mysql"
            section[instance] = {}
        elif instance:
            varname, value = parse_line(line)
            section[instance][varname] = value

    # Old Agent Plugin, no Instances in output
    if not instance:
        section['mysql'] = {}
        for line in info:
            varname, value = parse_line(line)
            section['mysql'][varname] = value

    return section


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

    levels = params['wsrep_cluster_size']

    yield from check_levels(
        float(section[item]['wsrep_cluster_size']),
        levels_lower=levels,
        metric_name="cluster_size",
        render_func=lambda v: "Size: %s" % v

    )

    cluster_status = section[item]['wsrep_cluster_status']
    cluster_status_state = State.Critical
    if cluster_status == params['wsrep_cluster_status']:
        cluster_status_state = State.OK
    yield Result(state=cluster_status_state, summary=f"Status: {cluster_status}")

    yield Result(state=State.OK, summary=f"ConfID: {section[item]['wsrep_cluster_conf_id']}")
    yield Result(state=State.OK, summary=f"UUID: {section[item]['wsrep_cluster_state_uuid']}")

check_plugin_mysql_galera_cluster_state = CheckPlugin(
    name = "mysql_galera_cluster_cluster_state",
    sections = ["mysql"],
    service_name = "MySQL Galera Cluster State %s",
    discovery_function = discover_mysql_galera,
    check_function = check_galera_cluster_state,
    check_default_parameters = {
        'wsrep_cluster_size': ('fixed', (3, 2)),
        'wsrep_cluster_status': "Primary",
    },
    check_ruleset_name = "galera_cluster_state",
)


def check_galera_node_state(item, params, section):
    """
    Check Galera Node State
    """
    wsrp_ready = section[item]['wsrep_ready']
    wsrp_ready_state = State.Critical
    if wrsp_ready == params['wsrep_ready']:
        wsrp_ready_state = State.OK
    yield Result(state=wsrp_ready_state, summary=f"Ready: {wsrp_ready}")

    wsrep_connected = section[item]['wsrep_connected']
    wsrep_connected_state = State.Critical
    if wsrep_connected == params['wsrep_connected']:
        wsrep_connected_state = State.OK
    yield Result(state=wsrep_connected_state, summary=f"Connected: {wsrep_connected}")

    wsrep_local = section[item]['wsrep_local_state_comment']
    wsrep_local_state = State.OK
    if wsrep_local == params['wsrep_local_state_comment']:
        wsrep_local_state = State.Critical
    yield Result(state=wsrep_local_state, summary=f"State: {wsrep_local}")

check_plugin_mysql_galera_cluster_node_state = CheckPlugin(
    name = "mysql_galera_cluster_node_state",
    sections = ["mysql"],
    service_name = "MySQL Galera Node State %s",
    discovery_function = discover_mysql_galera,
    check_function = check_galera_node_state,
    check_ruleset_name = "galera_node_state",
    check_default_parameters = {
        'wsrep_ready': 'ON',
        'wsrep_connected': 'ON',
        'wsrep_local_state_comment': 'Initialized',
    },
)


def check_galera_repl_health(item, params, section):
    """
    Check Galera Repl Health
    """
    cur_time = time.time()

    # check if agent output is available
    if item not in section:
        yield Result(state=State.Unknown, summary=f"Could not find instance '{item}' in agent output")
        return

    # wsrep_local_recv_queue_avg
    levels = params.get('wsrep_local_recv_queue_avg')
    yield from check_levels(
        float(section[item]['wsrep_local_recv_queue_avg']),
        levels_upper=levels,
        metric_name="recv_queue_avg"
    )
    yield Metric("recv_queue_max", float(section[item]['wsrep_local_recv_queue_max']))
    yield Metric("recv_queue_min", float(section[item]['wsrep_local_recv_queue_min']))
    yield Metric("recv_queue", float(section[item]['wsrep_local_recv_queue']))

    # wsrep_local_send_queue_avg
    levels = params.get('wsrep_local_send_queue_avg')
    yield from check_levels(
        float(section[item]['wsrep_local_send_queue_avg']),
        levels_upper=levels,
        metric_name='send_queue_avg'
    )

    yield Metric("send_queue_max", float(section[item]['wsrep_local_send_queue_max']))
    yield Metric("send_queue_min", float(section[item]['wsrep_local_send_queue_min']))
    yield Metric("send_queue", float(section[item]['wsrep_local_send_queue']))

    # wsrep_flow_control_paused
    levels = params.get('wsrep_flow_control_paused')
    yield from check_levels(
        float(section[item]['wsrep_flow_control_paused']),
        levels_upper=levels,
        metric_name='flow_control_paused'
    )
    flow_control_recv = get_rate(get_value_store(), "flow_control_recv", cur_time, float(section[item]['wsrep_flow_control_recv']))
    flow_control_sent = get_rate(get_value_store(), "flow_control_sent", cur_time, float(section[item]['wsrep_flow_control_sent']))
    yield Metric("flow_control_recv", float(flow_control_recv))
    yield Metric("flow_control_sent", float(flow_control_sent))

    yield Metric("cert_deps_distance", float(section[item]['wsrep_cert_deps_distance']))

check_plugin_mysql_galera_csluter_repl_health = CheckPlugin(
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
