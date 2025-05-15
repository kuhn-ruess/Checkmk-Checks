#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Result,
    Service,
    State,
)

from datetime import datetime

# example output lines
#<<<pure_arraycertificates>>>
#management None self-signed 1677118139000 1992478139000 Pure_Storage,_Inc.,Pure_Storage,_Inc.
#vasa-ct0 10.20.12.236 imported 1679495200000 1711117600000 Pure_Storage,Pure_Storage
#vasa-ct1 10.20.12.237 imported 1679495208000 1711117608000 Pure_Storage,Pure_Storage

def parse_pure_certificates(string_table):
    section = {}

    for row in string_table:
        (name, cn, status, valid_from, valid_to, org)  = row

        try:
            tosecs = int(valid_to)/1000
            valid_dt = datetime.fromtimestamp(tosecs) - datetime.now()

        except ValueError:
            valid_dt = 0

        section[name] = {
            'status': status,
            'cn': cn,
            'valid_to': valid_to,
            'valid': valid_dt.days,
            'org': org,
        }

    return section


agent_section_pure_arraycertificates = AgentSection(
    name="pure_arraycertificates",
    parse_function=parse_pure_certificates,
)


def discover_pure_certificates(section):
    for item in section.keys():
        yield Service(item=item)

def check_pure_certificates(item, section):
    failed = []

    if item not in section.keys():
        yield Result(
            state=State.UNKNOWN,
            summary=f"Item {item} not found",
        )

    else:
        data = section[item]
        yield Result(state=State.OK, summary=f"Common Name: {data['cn']}, Org: {data['org'].replace('_',' ')}, Valid until: {datetime.fromtimestamp(int(data['valid_to'])/1000).strftime('%Y-%m-%d %H:%M:%S')}")

        if data['valid'] > 30:
            yield Result(
                state=State.OK,
                summary=f"Days:{data['valid']}",
            )

        elif data['valid'] < 15:
            yield Result(
                state=State.CRIT,
                summary=f"Status: {data['status']}, Days:{data['valid']}",
            )

        else:
            yield Result(
                state=State.WARN,
                summary=f"Days:{data['valid']}",
            )


check_plugin_pure_arraycertificates = CheckPlugin(
    name="pure_arraycertificates",
    sections=["pure_arraycertificates"],
    service_name="SSL Cert %s",
    discovery_function=discover_pure_certificates,
    check_function=check_pure_certificates,
)
