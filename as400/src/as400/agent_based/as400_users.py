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

snmp_section_as400_users = SimpleSNMPSection(
    name="as400_users",
    detect=DETECT_AS400,
    fetch=SNMPTree(
        base=".1.3.6.1.2.1.25.1.5",
        oids=["0"],
    ),
    parse_function = parse_as400,
)

def discover_as400_users(section):
    """ Discover Function """
    yield Service()

def check_as400_users(params, section):
    """ Check Function """
    warn,crit = params["users_levels"]
    users_num = section

    yield Metric("users", users_num)

    state = State.OK
    if users_num >= crit:
        state = State.CRIT
    elif users_num >= warn:
        state = State.WARN

    yield Result(state=state, summary=f"{users_num} logged in users")

check_plugin_as400_users = CheckPlugin(
    name="as400_users",
    service_name="Users",
    discovery_function=discover_as400_users,
    check_function=check_as400_users,
    check_default_parameters={"users_levels": (9000,9500)},
    check_ruleset_name="as400_users",
)
