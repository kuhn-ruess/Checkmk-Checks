from datetime import datetime

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    check_levels,
    Service,
    render,
)


def parse_password_age(section):
    parsed = {}
    username = False
    for line in info:
        if username:
            if line[1].strip() == 'never':
                parsed[username] = 'never'
            else:
            	parsed[username] = datetime.strptime(line[1].strip(), "%b %d, %Y")
        if line[0].startswith('[[['):
            username = line[0][3:-3]
    return parsed

def discover_password_age(section):
    for user, data in section.items():
        yield Service(itemn=user)

def check_password_age(item, section):
    date = section[item]
    state = State.OK
    if date == 'never':
        yield Result(state=state,
                      summary=f"Never expires")
        return
    timediff = date - datetime.now()
    days = timediff.days
    if days <= 10:
        state = State.CRI

    yield Result(state=state,
                  summary=f"Expires in {days} days")


check_plugin_password_age = CheckPlugin(
    name = "password_age",
    service_name = "Password Age: %s",
    discovery_function = discover_password_age,
    check_function = check_password_age,
)
