from collections.abc import Mapping
from typing import Any

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    SNMPTree,
    State,
    StringTable,
    startswith,
    SimpleSNMPSection,
)



def parse_fsc_sc2_ilo_disks(string_table: StringTable) -> Mapping[str, Any]:
    """Parse SNMP data for FSC sc2 iLO disks"""
    parsed = {}
    for line in string_table:
        if len(line) >= 2:
            disk_name, disk_status = line[1], line[0]
            parsed[disk_name] = {
                "status": disk_status,
            }
    
    return parsed

def discover_fsc_sc2_ilo_disks(section: Mapping[str, Any]) -> DiscoveryResult:
    """Discover FSC sc2 iLO disks"""
    for disk_name, disk_data in section.items():
        if disk_data['status'] in ['4', '2']:
            continue 
        yield Service(item=disk_name)

def check_fsc_sc2_ilo_disks(item: str, section: Mapping[str, Any]) -> CheckResult:
    """Check FSC sc2 iLO disk status"""
    if item not in section:
        yield Result(state=State.UNKNOWN, summary=f"Disk {item} not found")
        return
    
    disk_info = section[item]
    status = disk_info["status"]
    
    # Map status values to check states 56             "1": (3, "unknown"),
    status_map = {
        "2": (State.CRIT, "not-present"),
        "3": (State.OK, "ok"),
        "4": (State.OK, "disabled"),
        "5": (State.CRIT, "error"),
        "6": (State.CRIT, "failed"),
        "7": (State.WARN, "prefailure-predicted"),
        "11": (State.OK, "hidden"),
    }
    
    state, status_text = status_map.get(status, (State.UNKNOWN, f"Unknown status: {status}"))
    
    yield Result(
        state=state,
        summary=f"Status: {status_text}",
    )

snmp_section_fsc_sc2_ilo_disks = SimpleSNMPSection(
    name="fsc_sc2_ilo_disks",
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.231"),  # Fujitsu enterprise OID
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.231.2.49.1.5.2.1",
        oids=[
            "15",  # health status
            "24" # Name
        ],
    ),
    parse_function = parse_fsc_sc2_ilo_disks,
)

check_plugin_fsc_sc2_ilo_disks = CheckPlugin(
    name="fsc_sc2_ilo_disks",
    service_name="Disk %s",
    discovery_function=discover_fsc_sc2_ilo_disks,
    check_function=check_fsc_sc2_ilo_disks,
)