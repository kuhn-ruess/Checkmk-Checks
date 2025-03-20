from .hci_helper import parse_list
from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Result,
    State,
    Service,
)

def discovery(section):
    """ Discovery """
    for disk_id in section:
        yield Service(item=disk_id)

def check(item, section):
    """ Check """
    if item not in section:
        return

    data = section[item]
    if data['OperationalStatus'] == 'OK':
        state = State.OK
    else:
        state = State.CRIT
    yield Result(
        state = state,
        summary = 'Health State: {HealthStatus}, Operational State: {OperationalStatus}, Type: {MediaType}'.format(**data)
    )

agent_section_hci_storage_pools = AgentSection(
    name="hci_s2d_storage_pools",
    parse_function=lambda string_table: parse_list(string_table, "DeviceId"),
)

check_plugin_hci_storage_pools = CheckPlugin(
    name="hci_s2d_storage_pools",
    service_name="Storage Pool %s",
    discovery_function=discovery,
    check_function=check,
)
