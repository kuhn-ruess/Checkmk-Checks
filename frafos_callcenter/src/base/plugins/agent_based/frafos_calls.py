#!/usr/bin/env python
import time
from .agent_based_api.v1 import *

def discover_frafos_calls(section):
    if section:
        yield Service(item=None)

def check_frafos_calls(params, section):
    total_calls, current_calls = map(int, section[0])
    yield Result(state=State.OK, summary=f"Currently: {current_calls} Calls")

    yield Metric("calls_current", current_calls)


    value_store = get_value_store()
    calls_per_sec = get_rate(value_store, "calls", time.time(), total_calls, raise_overflow=False)

    calls_per_min = int(round(calls_per_sec * 60, 2))

    yield Metric("calls_minute", calls_per_min)
    yield Result(state=State.OK, summary=f"Started {calls_per_min} per minute")

register.check_plugin(
    name = "frafos_calls",
    service_name = "Call Statistics",
    discovery_function = discover_frafos_calls,
    check_function = check_frafos_calls,
    check_default_parameters={},
)

register.snmp_section(
    name = "frafos_calls",
    detect = contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.8072"),
    fetch = SNMPTree(
        base = '.1.3.6.1.4.1.39695.2',
        oids = [
            '3.0', # fSBCCallStarts
            '4.0', # fSBCCalls
        ],
    ),
)
