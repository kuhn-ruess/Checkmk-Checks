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
    yield Service()

def check(section):
    """ Check """
    if not section:
        yield Result(
            state = State.OK,
            summary = "No Storage Jobs Running"
        )
        return
    for job, data in section.items():
        # Wired Windows, even in state completed, they are not finish
        # So Critical as long there is a Job showing.
        yield Result(
            state = State.CRIT,
            summary = f"Job {job} has State: {data['JobState']}"
        )

agent_section_hci_storage_jobs = AgentSection(
    name="hci_storage_jobs",
    parse_function=lambda string_table: parse_list(string_table, "Name"),
)

check_plugin_hci_storage_jobs = CheckPlugin(
    name="hci_storage_jobs",
    service_name="Storage Jobs",
    discovery_function=discovery,
    check_function=check,
)
