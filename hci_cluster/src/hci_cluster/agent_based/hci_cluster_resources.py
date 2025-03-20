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

    if data['State'] == 'Online':
        state = State.OK
    else:
        state = State.CRIT

    yield Result(
        state = state,
        summary = 'State: {State}, Owner group: {OwnerGroup}, Resource Type: {ResourceType}'.format(**data)
    )

agent_section_hci_cluster_resources = AgentSection(
    name="hci_cluster_resources",
    parse_function=lambda string_table: parse_list(string_table, "Name"),
)

check_plugin_hci_cluster_resources = CheckPlugin(
    name="hci_cluster_resources",
    service_name="Resource %s",
    discovery_function=discovery,
    check_function=check,
)
