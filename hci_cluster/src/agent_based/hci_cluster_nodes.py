from .agent_based_api.v1 import *
from .hci_helper import parse_list

def discovery(section):
    """ Discovery """
    for item in section:
        yield Service(item=item)

def check(item, section):
    """ Check """
    if item not in section:
        return

    data = section[item]

    if data['State'] == 'Up':
        state = State.OK
    else:
        state = State.CRIT

    yield Result(
        state = state,
        summary = 'State: {State}, Id: {Id}'.format(**data)
    )


register.agent_section(
    name="hci_cluster_nodes",
    parse_function=lambda string_table: parse_list(string_table, "Name"),
)

register.check_plugin(
    name="hci_cluster_nodes",
    service_name="Node %s",
    discovery_function=discovery,
    check_function=check,
)
