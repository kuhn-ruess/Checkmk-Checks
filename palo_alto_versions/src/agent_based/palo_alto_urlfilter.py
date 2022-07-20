#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .agent_based_api.v1 import (
    all_of,
    startswith,
    exists,
    Metric,
    register,
    Result,
    Service,
    SNMPTree,
    State,
)



register.snmp_section(
    name="palo_alto_urlfilter",
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.25461.2.1.2.1",
        oids=["10"],
    ),
    detect=all_of(
        startswith(".1.3.6.1.2.1.1.1.0", 'Palo Alto'),
        exists(".1.3.6.1.4.1.25461.2.1.2.5.1.*"),
    ),
)


def discover_palo_alto_urlfilter(section):
    yield Service()


def check_palo_alto_urlfilter(section):
    state = State.OK
    version = section[0][0]
    yield Result(
        state=state,
        summary=f"Current Version: {version}",
    )


register.check_plugin(
    name="palo_alto_urlfilter",
    service_name="Palo Alto URL-Filtering Version",
    discovery_function=discover_palo_alto_urlfilter,
    check_function=check_palo_alto_urlfilter,
)
