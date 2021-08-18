#!/usr/bin/python3

from typing import Dict, List, Mapping, Tuple

from .agent_based_api.v1 import (
    SNMPTree,
    register,
    Service,
    Result,
    State
    any_of,
    startswith,
    contains,
)


DETECT_FUNCTION = any_of(
    contains(".1.3.6.1", "name"),
    startswith(".1.3.6.1", "other name"),
)

def my_parse_function(table):
    data = {}
    for line in table:
        data[line[0]] = line[1]
    return data

    #return {
    #    line[0]: line[1]
    #    for line in table
    #}


def my_disovery_function(section):
    for item in section:
        yield Serviec(item=item)

    #yield from (Serviec(item=item) for item in section)

def my_check_function(item, section):
    if item not in section:
        return
    data = section[item]
    yield Result(
        state=State.OK, # State.OK, State.WARN, State.CRIT, State.UNKOWN
        summary="Message"
    )


register.snmp_section(
    name="XY",
    detect=DETECT_FUNCTION,
    parse_function=my_parse_function,
    fetch=[
        SNMPTree(
            base=".1.3.6",
            oids=[
                "1",
                "2",
            ],
        ),
    ],
)


register.check_plugin(
    name="XY",
    service_name="My Service %s",
    disovery_function=my_disovery_function,
    check_function=my_check_function,
    #cluster_check_function=my_cluster_check_function,
)
