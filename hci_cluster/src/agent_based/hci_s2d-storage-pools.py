from .agent_based_api.v1 import *
from .hci_helper import parse_list

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

register.agent_section(
    name="hci_s2d_storage_pools",
    parse_function=lambda string_table: parse_list(string_table, "DeviceId"),
)

register.check_plugin(
    name="hci_s2d_storage_pools",
    service_name="Storage Pool %s",
    discovery_function=discovery,
    check_function=check,
)
