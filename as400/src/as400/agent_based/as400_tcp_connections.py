#!/usr/bin/python
"""
AS 400 Checks
Bastian Kuhn, bastian.kuhn@kuhn-ruess.de
https://kuhn-ruess.de Checkmk Consulting and Development

"""
from .lib import DETECT_AS400, parse_as400

from cmk.agent_based.v2 import (
        SimpleSNMPSection,
        CheckPlugin,
        Service,
        SNMPTree,
        State,
        Metric,
        Result,
)

snmp_section_as400_tcp_connections = SimpleSNMPSection(
    name="as400_tcp_connections",
    detect=DETECT_AS400,
    fetch=SNMPTree(
        base=".1.3.6.1.2.1.6",
        oids=["9"],
    ),
    parse_function = parse_as400,
)

def discover_as400_tcp_connections(section):
    """ Discover Function """
    yield Service()

def check_as400_tcp_connections(params, section):
    """ Check Function """
    warn,crit = params["tcp_connections_levels"]
    conenctions_num = section

    yield Metric("tcp_connections", conenctions_num)

    state = State.OK
    if conenctions_num >= crit:
        state = State.CRIT
    elif conenctions_num >= warn:
        state = State.WARN

    yield Result(state=state, summary=f"Current TCP Connections at {conenctions_num}")

check_plugin_as400_jobs = CheckPlugin(
    name="as400_tcp_connections",
    service_name="Connections",
    discovery_function=discover_as400_tcp_connections,
    check_function=check_as400_tcp_connections,
    check_default_parameters={"tcp_connections_levels": (900000,950000)},
    check_ruleset_name="as400_jobs",
)
