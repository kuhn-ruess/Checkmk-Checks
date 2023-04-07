#!/usr/bin/env python
import time
from .agent_based_api.v1 import *

def discover_frafos_callagents(section):
    for line in section:
        yield Service(item=line[0])

def check_frafos_callagents(item, params, section):
    for line in section:
        if line[0] == item:
            realm = line[1]
            yield Result(state=State.OK, summary=f"Realm: {realm}")

            starts_to, starts_from = map(int, line[2:4])
            current_to, current_from = map(int, line[4:6])

            value_store = get_value_store()

            to_per_sec = get_rate(value_store, "starts_to", time.time(), starts_to, raise_overflow=False)
            from_per_sec = get_rate(value_store, "starts_from", time.time(), starts_from, raise_overflow=False)

            to_per_min = int(round(to_per_sec * 60, 2))
            from_per_min = int(round(from_per_sec * 60, 2))

            yield Metric("to_per_minute", to_per_min)
            yield Metric("from_per_minute", from_per_min)
            yield Metric("current_to", current_to)
            yield Metric("current_from", current_from)

            yield Result(state=State.OK, summary=f"Currently to: {current_to} calls")
            yield Result(state=State.OK, summary=f"Started to: {to_per_min} per minute")

            yield Result(state=State.OK, summary=f"Currently from: {current_from} calls")
            yield Result(state=State.OK, summary=f"Started from: {from_per_min} per minute")

            bits_to, bits_from = map(int, line[6:8])

            bits_to_per_sec = get_rate(value_store, "bits_to", time.time(), bits_to, raise_overflow=False)
            bits_from_per_sec = get_rate(value_store, "bits_from", time.time(), bits_from, raise_overflow=False)

            yield Result(state=State.OK, summary=f"Traffic In/Out: {render.bytes(bits_to_per_sec)}/ {render.bytes(bits_from_per_sec)} per second")
            yield Metric("current_bytes_to", bits_to_per_sec)
            yield Metric("current_bytes_from", bits_from_per_sec)

            return

register.check_plugin(
    name = "frafos_callagents",
    service_name = "Call Agent %s",
    discovery_function = discover_frafos_callagents,
    check_function = check_frafos_callagents,
    check_default_parameters={},
)

register.snmp_section(
    name = "frafos_callagents",
    detect = contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.8072"),
    fetch = SNMPTree(
        base = '.1.3.6.1.4.1.39695.2.2.1',
        oids = [
            '3', # fSBCCAName
            '4', # fSBCCARealmName
            '5', # fSBCCACallStartsTo
            '6', # fSBCCACallStartsFrom
            '7', # fSBCCACallsTo
            '8', # fSBCCACallsFrom
            '9', # fSBCCABitsTo
            '10', # fSBCCABitsFrom
        ],
    ),
)
