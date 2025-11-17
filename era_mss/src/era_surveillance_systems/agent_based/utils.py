"""
Helper Functions
"""
from cmk.agent_based.v2 import (
    contains,
    Service,
    Result,
    State,
)


state_map_era = {
    'OKA' : State.OK,
    'WAR': State.WARN,
}

detect_era = contains('.1.3.6.1.2.1.1.2.0', ".1.3.6.1.4.1.311.1.1.3.1.2")

def discover_era(section):
    for entry in section:
        yield Service(item=entry)

def discover_era_simple(section):
    yield Service()


def check_era(item, section):
    for key, mon_data in section[item].items():
        value = mon_data['value']
        state = State.OK
        if mon_data['mon']:
            state = state_map_era[value]
        yield Result(state=state, summary=f"{key}: {value}")

def check_era_simple(section):
    for key, mon_data in section.items():
        value = mon_data['value']
        state = State.OK
        if mon_data['mon']:
            state = state_map_era[value]
        yield Result(state=state, summary=f"{key}: {value}")

