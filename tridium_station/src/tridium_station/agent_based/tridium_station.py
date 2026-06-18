#!/usr/bin/env python3
# Written by Bastian Kuhn (mail@bastian-kuhn.de)
# Tridium Niagara Station SNMP checks (enterprise OID .1.3.6.1.4.1.4131.1)

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Metric,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
    StringTable,
    startswith,
)

# Subtree indices below .1.3.6.1.4.1.4131.1.6 that each get their own
# check variant. Service name "TR<N>".
_TRIDIUM_INDICES = [
    2, 3, 7, 8, 9,
    10, 11, 13, 14, 15,
    16, 17, 19,
    23, 24, 25, 26, 27, 28,
]


def parse_tridium(string_table: StringTable) -> StringTable:
    return string_table


def discover_tridium(section: StringTable) -> DiscoveryResult:
    for line in section:
        yield Service(item=line[0], parameters={"current": line[1]})


def check_tridium(item: str, params: dict, section: StringTable) -> CheckResult:
    for sensor, value in section:
        if sensor != item:
            continue

        try:
            num_value = round(float(value), 2)
            is_float = True
        except ValueError:
            is_float = False

        if is_float:
            state = State.OK
            target = ""
            if params.get("levels"):
                warn, crit = params["levels"]
                if num_value >= crit:
                    state = State.CRIT
                elif num_value >= warn:
                    state = State.WARN
            yield Result(state=state, summary="Current state: %s%s" % (num_value, target))
            yield Metric("value", num_value)
            return

        # String value
        state = State.OK
        target = ""
        if params.get("allowed_strings"):
            if value not in params["allowed_strings"]:
                state = State.CRIT
                target = " and not in: %s" % (", ".join(params["allowed_strings"]))
        if params.get("use_discovery"):
            # Overwrites "allowed strings"
            if value != params.get("current"):
                state = State.CRIT
                target = "(!!) but should be %s" % (params.get("current"))
            else:
                state = State.OK
                target = ""
        if params.get("forced_strings"):
            # Overwrites all
            if value in params["forced_strings"]:
                state = State.CRIT
                target = "(!!)"
        yield Result(state=state, summary="Current state: %s%s" % (value, target))
        return


for _what in _TRIDIUM_INDICES:
    globals()["snmp_section_tridium_%d" % _what] = SimpleSNMPSection(
        name="tridium_%d" % _what,
        parse_function=parse_tridium,
        detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.4131.1"),
        fetch=SNMPTree(
            base=".1.3.6.1.4.1.4131.1.6.%d.2.1" % _what,
            oids=["2", "3"],
        ),
    )

    globals()["check_plugin_tridium_%d" % _what] = CheckPlugin(
        name="tridium_%d" % _what,
        service_name="TR%d %%s" % _what,
        discovery_function=discover_tridium,
        check_function=check_tridium,
        check_default_parameters={},
        check_ruleset_name="tridium",
    )
