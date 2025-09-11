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
SONICWALL_CPU_OID = ".1.3.6.1.4.1.8741.1.3.1.3.0"

snmp_section_sonicwall_cpu = SimpleSNMPSection(
    name="sonicwall_cpu",
    detect=DETECT_SONICWALL,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.8741.1.3.1.3",
        oids=["0"],
    ),
    parse_function=lambda section: int(section[0][0]) if section and section[0] else None,
)

def discover_sonicwall_cpu(section):
    if section is not None:
        yield Service()

def check_sonicwall_cpu(params, section):
    value = section
    if value is None:
        yield Result(state=State.UNKNOWN, summary="No CPU data")
        return
    yield from check_levels(
        value,
        levels_upper=params['levels'],
        metric_name="cpu",
        label="CPU usage",
        boundaries=(0, 100),
    )

check_plugin_sonicwall_cpu = CheckPlugin(
    name="sonicwall_cpu",
    service_name="CPU utilization",
    discovery_function=discover_sonicwall_cpu,
    check_function=check_sonicwall_cpu,
    check_default_parameters={"levels": ('fixed', (80.0, 95.0))},
    check_ruleset_name="sonicwall_cpu",
)