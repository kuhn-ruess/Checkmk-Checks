#!/usr/bin/env python3
# Written by Bastian Kuhn (mail@bastian-kuhn.de)
# Tridium Niagara Station - cross-probe "special" checks

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Metric,
    Result,
    Service,
    SNMPSection,
    SNMPTree,
    State,
    StringTable,
    startswith,
)


def parse_tridium_special(string_table: list[StringTable]) -> dict:
    data = dict(string_table[0])
    data.update(dict(string_table[1]))
    return data


snmp_section_tridium_special = SNMPSection(
    name="tridium_special",
    parse_function=parse_tridium_special,
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.4131.1"),
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.4131.1.6.21",
            oids=["2.1.2", "2.1.3"],
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.4131.1.6.22",
            oids=["2.1.2", "2.1.3"],
        ),
    ],
)


def discover_tridium_special(section: dict) -> DiscoveryResult:
    for item in section:
        yield Service(item=item)


def check_tridium_special(item: str, params: dict, section: dict) -> CheckResult:
    if item not in section:
        return

    status = section[item]
    is_float = False
    try:
        status = round(float(status), 2)
        is_float = True
    except ValueError:
        pass

    state = State.OK
    message = "Status %s" % status

    if params.get("rule"):
        rule = params["rule"]
        if_field_status = section.get(rule["if_field"])

        if if_field_status == rule["if_field_state"]:
            target_state = rule["if_state"]
        else:
            target_state = rule["else_state"]

        if status != target_state:
            state = State.CRIT
            message = "State is %s but should be %s because %s is %s" % (
                status,
                target_state,
                rule["if_field"],
                if_field_status,
            )
    elif params.get("states"):
        if not is_float and status not in params["states"]:
            state = State.CRIT
            message += ", State not in %s" % str(params["states"])
    else:
        message += " (Always OK)"

    yield Result(state=state, summary=message)
    if is_float:
        yield Metric("value", status)


check_plugin_tridium_special = CheckPlugin(
    name="tridium_special",
    service_name="TRS %s",
    discovery_function=discover_tridium_special,
    check_function=check_tridium_special,
    check_default_parameters={},
    check_ruleset_name="tridium_special",
)
