#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

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
    get_value_store,
    render,
)



register.snmp_section(
    name="palo_alto_antivirus",
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.25461.2.1.2.1",
        oids=["8"],
    ),
    detect=all_of(
        startswith(".1.3.6.1.2.1.1.1.0", 'Palo Alto'),
        exists(".1.3.6.1.4.1.25461.2.1.2.5.1.*"),
    ),
)


def discover_palo_alto_antivirus(section):
    yield Service()


def check_palo_alto_antivirus(params, section):
    value_store = get_value_store()
    now = time.time()

    # Version
    version = section[0][0]
    last_version = value_store.get('last_version', version)
    if last_version != version:
        value_store['last_update'] = now
    # We need to set it anyway to have it available
    value_store['last_version'] = version

    yield Result(
        state=State.OK,
        summary=f"Current Version: {version}",
    )

    # Age
    age_warn, age_crit = params.get("age")
    last_update = value_store.get('last_update', now)

    if last_update == now:
        value_store['last_update'] = now

    timediff = now - last_update

    if timediff >= age_crit:
        yield Result(
            state=State.CRIT,
            summary = f"No Updates for the last {render.timespan(timediff)}"
        )
    elif timediff >= age_warn:
        yield Result(
            state=State.WARN,
            summary = f"No Updates for the last {render.timespan(timediff)}"
        )


register.check_plugin(
    name="palo_alto_antivirus",
    service_name="Palo Alto AntiVirus Version",
    discovery_function=discover_palo_alto_antivirus,
    check_function=check_palo_alto_antivirus,
    check_ruleset_name="palo_alto_antivirus",
    check_default_parameters={"age": (86400, 104400)},
)
