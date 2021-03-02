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
        summary = 'Health State: {HealthStatus}, Operational State: {OperationalStatus}'.format(**data)
    )

register.agent_section(
    name="hci_virtual_disks",
    parse_function=lambda string_table: parse_list(string_table, "FriendlyName"),
)

register.check_plugin(
    name="hci_virtual_disks",
    service_name="Virtual Disk %s",
    discovery_function=discovery,
    check_function=check,
)
