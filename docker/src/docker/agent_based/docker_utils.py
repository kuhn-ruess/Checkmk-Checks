#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from typing import NamedTuple

from cmk.agent_based.v2 import GetRateError

class SectionCpuUtilizationOs(NamedTuple):
    num_cpus: int
    time_base: float
    time_cpu: float


def get_docker_container_cpu(value_store, container):
    """
    Get Docker Container CPU
    """
    last_state = value_store.get("usage_counters")
    current_state = {
            "cpu_usage" : float(container["CPU_usage"]),
            "cpu_usage_system" : float(container["CPU_system_usage"]),
    }

    value_store["usage_counters"] = current_state
    if not last_state:
        raise GetRateError("Initialized usage counters")

    usage = current_state["cpu_usage"] - last_state["cpu_usage"]
    system_usage = current_state["cpu_usage_system"] - last_state["cpu_usage_system"]

    if usage < 0 or system_usage < 0:
        raise GetRateError("Value overflow")

    if system_usage == 0:
        raise GetRateError("No time difference")

    cpu_usage_percent = 100 * (usage / system_usage)
    return cpu_usage_percent
