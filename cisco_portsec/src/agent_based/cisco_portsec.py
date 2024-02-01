#!/usr/bin/env python3
"""
Report Ports with missing Porstec config
"""
from .agent_based_api.v1 import (
    all_of,
    exists,
    register,
    Service,
    SNMPTree,
    State,
    Result,
    OIDEnd,
    contains,
)


def _sanitize_mac(string):
    """
    """
    hx_gen = ("%02s" % hex(ord(m))[2:] for m in string)
    return ":".join(hx_gen).replace(" ", "0")


def parse_cisco_portsec(string_table):
    """
    Parse Function
    """
    parsed = []
    # l[1] = Name, l[2] = Portstate
    names = {l[0]: (l[1], l[2], l[3]) for l in string_table[0]}
    for num, is_enabled, status, _violation_count, _lastmac in string_table[1]:
        enabled_txt = {"1": "yes", "2": "no"}.get(is_enabled)
        try:
            status_int = int(status)
        except ValueError:
            status_int = None
        if num in names:
            parsed.append(
                (
                    names[num][0],
                    int(names[num][1]),
                    enabled_txt,
                    status_int,
                    names[num][2],
                )
            )
        else:
            parsed.append((num, 0, enabled_txt, status_int, ""))

    return parsed


def discover_cisco_portsec(section):
    """
    Discovery Function
    """
    if section:
        yield Service()


def check_cisco_portsec(params, section):
    """
    Check Function
    """
    exceptions = params['exceptions']

    at_least_one_problem = False
    for name, adm_state, is_enabled, _status, alias in section:
        message = f"Port {name} ({alias})"

        if is_enabled is not None:
            # If port cant be enabled and is up and has violations -> WARN
            if adm_state == int(2):
                continue
            if name in exceptions or alias in exceptions:
                continue
            if True in [True for x in exceptions if x and alias.startswith(x)]:
                continue
            if is_enabled == "no":
                at_least_one_problem = True
                yield Result(
                    state=State.WARN,
                    summary=f"{message} not enabled"
                )
        else:
            yield Result(
                state=State.UNK,
                summary=f"{message} unknown enabled state"
            )
            at_least_one_problem = True

    if not at_least_one_problem:
        yield Result(
            state=State.OK,
            summary="All Ports Secured"
        )


register.snmp_section(
    name="cisco_portsec",
    detect=all_of(
        contains(".1.3.6.1.2.1.1.1.0", "cisco"), exists(".1.3.6.1.4.1.9.9.315.1.2.1.1.1.*")
    ),
    fetch=[
        SNMPTree(
            base=".1.3.6.1.2.1",
            oids=[OIDEnd(), "2.2.1.2", "2.2.1.7", "31.1.1.1.18"],
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.9.9.315.1.2.1.1",
            oids=[OIDEnd(), "1", "2", "9", "10"],
        ),
    ],
    parse_function=parse_cisco_portsec,

)


register.check_plugin(
    name="cisco_portsec",
    service_name="Port Security Status",
    discovery_function=discover_cisco_portsec,
    check_function=check_cisco_portsec,
    check_default_parameters={
        'exceptions': [],
    },
    check_ruleset_name="cisco_portsec",
)
