#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

import time

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    State,
    StringTable,
)

JOB_STATES = {
    "A": "Canceled by user",
    "B": "Blocked",
    "C": "Created, but not running",
    "c": "Waiting for client resource",
    "D": "Verify differences",
    "d": "Waiting for maximum jobs",
    "E": "Terminated in error",
    "e": "Non-fatal error",
    "f": "fatal error",
    "F": "Waiting on File Daemon",
    "j": "Waiting for job resource",
    "M": "Waiting for mount",
    "m": "Waiting for new media",
    "p": "Waiting for higher priority jobs to finish",
    "R": "Running",
    "S": "Scan",
    "s": "Waiting for storage resource",
    "T": "Terminated normally",
    "t": "Waiting for start time",
    "W": "Terminated with Warning",
}


def _max_age_levels(value):
    """Normalize the max_age parameter to a (warn, crit) tuple or None.

    Accepts both the legacy bare ``(warn, crit)`` tuple and the
    rulesets.v1 SimpleLevels form ``("fixed", (warn, crit))`` /
    ``("no_levels", None)``.
    """
    if not value:
        return None
    if isinstance(value, tuple) and len(value) == 2 and isinstance(value[0], str):
        mode, levels = value
        if mode == "fixed" and levels:
            return levels
        return None
    return value


def parse_bacula_jobs(string_table: StringTable) -> dict:
    latest_state: dict = {}
    for line in string_table[1:]:
        if len(line) < 4:
            continue
        job_id, name, status, endtime = line[0], line[1], line[2], line[3]
        try:
            end_date = time.strptime(endtime, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
        latest_state.setdefault(name, {"last_backup": end_date, "state": status})
        if end_date > latest_state[name]["last_backup"]:
            latest_state[name] = {
                "last_backup": end_date,
                "state": status,
            }
    return latest_state


agent_section_bacula_jobs = AgentSection(
    name="bacula_jobs",
    parse_function=parse_bacula_jobs,
)


def discovery_bacula_jobs(section: dict) -> DiscoveryResult:
    for job in section:
        yield Service(item=job)


def check_bacula_jobs(item: str, params: dict, section: dict) -> CheckResult:
    if item not in section:
        return
    data = section[item]

    state = State.WARN
    message = "Current State: %s" % JOB_STATES.get(data["state"], data["state"])
    if data["state"] in params["crit_states"]:
        state = State.CRIT
    elif data["state"] in params["ok_states"]:
        state = State.OK
    yield Result(state=state, summary=message)

    state = State.OK
    message = "Last Backup: %s" % time.strftime("%Y-%m-%d %H:%M", data["last_backup"])
    levels = _max_age_levels(params.get("max_age"))
    if levels:
        now = time.time()
        age = now - time.mktime(data["last_backup"])
        warn, crit = levels
        if age >= crit:
            state = State.CRIT
        elif age >= warn:
            state = State.WARN
    yield Result(state=state, summary=message)


check_plugin_bacula_jobs = CheckPlugin(
    name="bacula_jobs",
    service_name="Job %s",
    discovery_function=discovery_bacula_jobs,
    check_function=check_bacula_jobs,
    check_default_parameters={
        "ok_states": ["T", "R"],
        "crit_states": ["E", "f"],
        "max_age": ("fixed", (86400.0 * 5, 86400.0 * 7)),
    },
    check_ruleset_name="bacula_jobs",
)
