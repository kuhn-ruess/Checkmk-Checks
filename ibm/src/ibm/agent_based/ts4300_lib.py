#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    Result,
    State,
    matches,
)

DETECT_TS4300 = matches(".1.3.6.1.4.1.14851.3.1.3.3.0", "IBM")

AVAILABILITY = {
    "1": (State.WARN, "other"),
    "2": (State.UNKNOWN, "unknown"),
    "3": (State.OK, "running full power"),
    "4": (State.WARN, "warning"),
    "5": (State.WARN, "in test"),
    "6": (State.UNKNOWN, "not applicable"),
    "7": (State.WARN, "power off"),
    "8": (State.WARN, "off line"),
    "9": (State.WARN, "off duty"),
    "10": (State.WARN, "degraded"),
    "11": (State.WARN, "not installed"),
    "12": (State.CRIT, "install error"),
    "13": (State.UNKNOWN, "power save unknown"),
    "14": (State.OK, "power save low power mode"),
    "15": (State.OK, "power save standby"),
    "16": (State.WARN, "power cycle"),
    "17": (State.WARN, "power save warning"),
    "18": (State.WARN, "paused"),
    "19": (State.WARN, "not ready"),
    "20": (State.WARN, "not configured"),
    "21": (State.WARN, "quiesced"),
}

OPERATIONAL_STATUS = {
    "0": (State.UNKNOWN, "unknown"),
    "1": (State.WARN, "other"),
    "2": (State.OK, "ok"),
    "3": (State.WARN, "degraded"),
    "4": (State.WARN, "stressed"),
    "5": (State.WARN, "predictive failure"),
    "6": (State.CRIT, "error"),
    "7": (State.CRIT, "non-recoverable error"),
    "8": (State.WARN, "starting"),
    "9": (State.WARN, "stopping"),
    "10": (State.WARN, "stopped"),
    "11": (State.WARN, "in service"),
    "12": (State.UNKNOWN, "no contact"),
    "13": (State.UNKNOWN, "lost communication"),
    "14": (State.CRIT, "aborted"),
    "15": (State.WARN, "dormant"),
    "16": (State.CRIT, "supporting entity in error"),
    "17": (State.WARN, "completed"),
    "18": (State.WARN, "power mode"),
    "19": (State.WARN, "dmtf reserved"),
    "32768": (State.UNKNOWN, "vendor reserved"),
}


def status_result(mapping, value, label):
    """Yield a Result for a CIM style status value."""
    state, text = mapping.get(value, (State.UNKNOWN, f"unknown ({value})"))
    yield Result(state=state, summary=f"{label}: {text}")


def device_name(raw):
    """Normalize the padded device names the library reports."""
    return " ".join(raw.split())
