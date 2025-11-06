from datetime import datetime

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Service,
    State,
    Result,
)


def parse_password_age(string_table):
    parsed = {}
    username = False
    for line in string_table:
        if line[0].startswith('[[['):
            username = line[0][3:-3]
            continue
        if username:
            if line[1].strip() == 'never':
                parsed[username] = 'never'
            elif "does not" in line[1]:
                parsed[username] = line[1]
            else:
                parsed[username] = datetime.strptime(line[1].strip(), "%b %d, %Y")
    return parsed

def discover_password_age(section):
    for user, _ in section.items():
        yield Service(item=user)

def check_password_age(item, section):
    date = section[item]
    state = State.OK
    if date == 'never':
        yield Result(state=state,
                      summary=f"Never expires")
        return
    if 'does not' in date:
        yield Result(state=State.WARN,
                      summary=str(date))
        return

    timediff = date - datetime.now()
    days = timediff.days
    if days <= 10:
        state = State.CRI

    yield Result(state=state,
                  summary=f"Expires in {days} days")

agent_section_password_age = AgentSection(
    name="password_age",
    parse_function=parse_password_age,
)

check_plugin_password_age = CheckPlugin(
    name = "password_age",
    service_name = "Password Age: %s",
    discovery_function = discover_password_age,
    check_function = check_password_age,
)
