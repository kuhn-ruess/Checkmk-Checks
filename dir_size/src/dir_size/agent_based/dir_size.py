#!/usr/bin/python
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    check_levels,
    Service,
    render,
    Result,
    State
)

# Example Agent Output
#<<<dir_size>>>
#17516   /tmp/
#626088  /usr/local/

def discover_dir_size(section):
    """
    Discover all directories
    """
    for filesystem in section:
        yield Service(item=filesystem)

def check_dir_size(item, params, section):
    """ Check the size of the directory """

    if item not in section:
        return

    folder_size_bytes = section[item]['size_bytes']

    if not params.get('levels'):
        yield Result(
            state=State.OK,
            summary=f"Folder usage: {render.bytes(folder_size_bytes)}"
        )
    else:
        yield from check_levels(
            folder_size_bytes,
            levels_upper=params['levels'],
            label="Folder usage",
            metric_name='bytes',
            render_func=render.bytes,
        )

def parse_dir_size(string_table):
    """
    Parse Filesystems
    """
    parsed = {}
    for size, folder_name in string_table:
        parsed[folder_name] = {'size_bytes': int(size)*1024}
    return parsed


agent_section_dir_size = AgentSection(
    name="dir_size",
    parse_function=parse_dir_size,
)


check_plugin_dir_size = CheckPlugin(
    name="dir_size",
    service_name="Size of %s",
    discovery_function=discover_dir_size,
    check_function=check_dir_size,
    check_default_parameters={
        'levels': None,
    },
    check_ruleset_name="dir_size",

)
