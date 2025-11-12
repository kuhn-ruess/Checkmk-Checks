#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from .lib import DETECT_AS400, parse_as400

from cmk.agent_based.v2 import (
    SimpleSNMPSection,
    CheckPlugin,
    Service,
    SNMPTree,
    State,
    Metric,
    Result,
)


snmp_section_as400_jobs = SimpleSNMPSection(
    name="as400_jobs",
    detect=DETECT_AS400,
    fetch=SNMPTree(
        base=".1.3.6.1.2.1.25.1.6",
        oids=["0"],
    ),
    parse_function = parse_as400,
)


def discover_as400_jobs(section):
    """ Discover Function """
    yield Service()

def check_as400_jobs(params, section):
    """ Check Function """
    warn, crit = params["job_levels"][1]
    jobs_num = section

    yield Metric("jobs", jobs_num)

    state = State.OK
    if jobs_num >= crit:
        state = State.CRIT
    elif jobs_num >= warn:
        state = State.WARN

    yield Result(state=state, summary=f"Jobs at {jobs_num}")


check_plugin_as400_jobs = CheckPlugin(
    name="as400_jobs",
    service_name="Jobs",
    discovery_function=discover_as400_jobs,
    check_function=check_as400_jobs,
    check_default_parameters={"job_levels": ("fixed", (9000, 9500))},
    check_ruleset_name="as400_jobs",
)
