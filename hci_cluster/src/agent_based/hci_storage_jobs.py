from .agent_based_api.v1 import *
from .hci_helper import parse_list

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

register.agent_section(
    name="hci_storage_jobs",
    parse_function=lambda string_table: parse_list(string_table, "Name"),
)

register.check_plugin(
    name="hci_storage_jobs",
    service_name="Storage Jobs",
    discovery_function=discovery,
    check_function=check,
)
