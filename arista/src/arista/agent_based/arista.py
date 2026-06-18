#!/usr/bin/env python3

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    get_value_store,
    Metric,
    OIDEnd,
    Result,
    Service,
    SNMPSection,
    SNMPTree,
    State,
    StringTable,
    startswith,
)
from cmk.plugins.lib.fan import check_fan
from cmk.plugins.lib.temperature import check_temperature, TempParamDict


def parse_arista(string_table: list[StringTable]) -> dict:
    entity_names = {int(k): v for k, v in string_table[0]}
    value = {int(k): v for k, v in string_table[1]}
    status = {int(k): v for k, v in string_table[2]}
    unit = {int(k): v for k, v in string_table[3]}
    data = {}

    def name_cleanup(what: str) -> str:
        if what.startswith("Fan"):
            return what[4:].strip()
        return what

    for entry in string_table[1]:
        entry_nr = int(entry[0])
        data[name_cleanup(entity_names[entry_nr])] = {
            "value": value.get(entry_nr),
            "status": status.get(entry_nr),
            "unit": unit.get(entry_nr),
        }
    return data


_ARISTA_SNMP_TREE = [
    SNMPTree(base=".1.3.6.1.2.1.47.1.1.1.1", oids=[OIDEnd(), "2"]),  # Entity descriptions
    SNMPTree(base=".1.3.6.1.2.1.99.1.1.1", oids=[OIDEnd(), "4"]),  # Value
    SNMPTree(base=".1.3.6.1.2.1.99.1.1.1", oids=[OIDEnd(), "5"]),  # Status
    SNMPTree(base=".1.3.6.1.2.1.99.1.1.1", oids=[OIDEnd(), "6"]),  # Unit
]

_ARISTA_DETECT = startswith(".1.3.6.1.2.1.1.1.0", "Arista Networks")

arista_state_maps = {
    "1": (State.OK, "OK"),
    "2": (State.WARN, "warning"),
}


snmp_section_arista = SNMPSection(
    name="arista",
    parse_function=parse_arista,
    detect=_ARISTA_DETECT,
    fetch=_ARISTA_SNMP_TREE,
)


def discover_arista_temp(section: dict) -> DiscoveryResult:
    for key, value in section.items():
        if value["unit"] != "Celsius":
            continue
        if key.startswith("PhyAlaska"):
            continue
        if value.get("value"):
            yield Service(item=key)


def check_arista_temp(item: str, params: TempParamDict, section: dict) -> CheckResult:
    if item not in section:
        return
    state, state_readable = arista_state_maps[section[item]["status"]]
    temperature = float(section[item]["value"]) / 10

    yield Result(state=state, summary="Status: %s" % state_readable)
    yield from check_temperature(
        temperature,
        params,
        unique_name="arista_temp_%s" % item,
        value_store=get_value_store(),
    )


check_plugin_arista = CheckPlugin(
    name="arista",
    service_name="Temperature %s",
    discovery_function=discover_arista_temp,
    check_function=check_arista_temp,
    check_default_parameters={},
    check_ruleset_name="temperature",
)


def discover_arista_fan(section: dict) -> DiscoveryResult:
    for key, value in section.items():
        if value["unit"] == "RPM":
            yield Service(item=key)


def check_arista_fan(item: str, params, section: dict) -> CheckResult:
    if item not in section:
        return
    state, state_readable = arista_state_maps[section[item]["status"]]
    try:
        rpm = int(section[item]["value"])
    except (TypeError, ValueError):
        rpm = 0

    yield Result(state=state, summary="Status: %s" % state_readable)
    yield from check_fan(rpm, params)


check_plugin_arista_fan = CheckPlugin(
    name="arista_fan",
    service_name="Fan %s",
    sections=["arista"],
    discovery_function=discover_arista_fan,
    check_function=check_arista_fan,
    check_default_parameters={
        "lower": (2000, 1000),
        "upper": (9000, 9500),
    },
    check_ruleset_name="hw_fans",
)


def discover_arista_voltage(section: dict) -> DiscoveryResult:
    for key, value in section.items():
        if value["unit"] == "Volts":
            yield Service(item=key)


def check_arista_voltage(item: str, params, section: dict) -> CheckResult:
    if item not in section:
        return
    state, state_readable = arista_state_maps[section[item]["status"]]
    try:
        power = int(section[item]["value"])
    except (TypeError, ValueError):
        power = 0

    levels = params.get("levels_lower")
    if levels and levels[0] == "fixed":
        warn, crit = levels[1]
        infotext = "voltage: %dV (warn/crit at %dV/%dV)" % (power, warn, crit)
        yield Metric("voltage", power, levels=(warn, crit), boundaries=(200, 240))
        if power <= crit:
            yield Result(state=State.CRIT, summary=infotext)
        elif power <= warn:
            yield Result(state=State.WARN, summary=infotext)
    else:
        yield Metric("voltage", power, boundaries=(200, 240))

    yield Result(state=state, summary="Status: %s" % state_readable)


check_plugin_arista_voltage = CheckPlugin(
    name="arista_voltage",
    service_name="Voltage %s",
    sections=["arista"],
    discovery_function=discover_arista_voltage,
    check_function=check_arista_voltage,
    check_default_parameters={"levels_lower": ("fixed", (50, 50))},
    check_ruleset_name="arista_voltage",
)
