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


agent_section_hcicluster = AgentSection(
    name="hci_cluster_nodes",
    parse_function=lambda string_table: parse_list(string_table, "Name"),
)

check_plugin_hci_cluster_nodes = CheckPlugin(
    name="hci_cluster_nodes",
    service_name="Node %s",
    discovery_function=discovery,
    check_function=check,
)
