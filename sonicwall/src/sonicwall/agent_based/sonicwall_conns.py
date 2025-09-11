"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.agent_based.v2 import (
    SimpleSNMPSection,
    CheckPlugin,
    Service,
    SNMPTree,
    State,
    Metric,
    Result,
    check_levels,
    contains,
)

DETECT_SONICWALL = contains('.1.3.6.1.2.1.1.1.0', 'sonicwall')
SONICWALL_CONNS_OIDS = ["1", "2", "3"]

snmp_section_sonicwall_conns = SimpleSNMPSection(
    name="sonicwall_conns",
    detect=DETECT_SONICWALL,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.8741.1.3.1",
        oids=SONICWALL_CONNS_OIDS,
    ),
    parse_function=lambda section: [
        {
            "oid_end": str(entry[0]),
            "con_max": int(entry[1]),
            "con_current": int(entry[2]),
        }
        for entry in section
    ] if section else [],
)

def discover_sonicwall_conns(section):
    for entry in section:
        yield Service(item=entry["oid_end"])

def check_sonicwall_conns(item, params, section):
    data = next((e for e in section if e["oid_end"] == item), None)
    if not data:
        yield Result(state=State.UNKNOWN, summary=f"No connection data for {item}")
        return
    con_max = data["con_max"]
    con_current = data["con_current"]
    percent = int(100 * con_current / con_max)
    yield from check_levels(
        percent,
        levels_upper=params['levels'],
        metric_name="connections",
        label="Connections usage",
        boundaries=(0, 100),
    )

check_plugin_sonicwall_conns = CheckPlugin(
    name="sonicwall_conns",
    service_name="Connections %s",
    discovery_function=discover_sonicwall_conns,
    check_function=check_sonicwall_conns,
    check_default_parameters={"levels": ('fixed', (80, 95))},
    check_ruleset_name="sonicwall_conns",
)
