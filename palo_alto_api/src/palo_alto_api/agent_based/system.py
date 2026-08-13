#!/usr/bin/env python3
"""
Palo Alto XML API - System info check

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
import json

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Result,
    Service,
    State,
    render,
)


def parse_palo_alto_api_system(string_table):
    for line in string_table:
        try:
            data = json.loads(line[0])
        except (json.JSONDecodeError, IndexError):
            continue
        if "error" in data:
            return {"_error": data["error"]}
        if "item" in data:
            return {data["item"]: data}
    return {}


agent_section_palo_alto_api_system = AgentSection(
    name="palo_alto_api_system",
    parse_function=parse_palo_alto_api_system,
)


def discover_palo_alto_api_system(section):
    if section.get("System"):
        yield Service()


def check_palo_alto_api_system(section):
    if "_error" in section:
        yield Result(state=State.CRIT, summary=f"Agent error: {section['_error']}")
        return
    data = section.get("System")
    if not data:
        return

    model = data.get("model") or data.get("family")
    version = data.get("sw_version")
    summary = f"Model: {model}, PAN-OS: {version}"
    yield Result(state=State.OK, summary=summary)

    if data.get("serial"):
        yield Result(state=State.OK, summary=f"Serial: {data['serial']}")

    details = []
    for label, key in (
        ("Hostname", "hostname"),
        ("App-ID version", "app_version"),
        ("App-ID release date", "app_release_date"),
        ("Threat version", "threat_version"),
        ("Antivirus version", "av_version"),
        ("URL filtering version", "url_filtering_version"),
        ("GlobalProtect client", "gp_client_version"),
    ):
        value = data.get(key)
        if value:
            details.append(f"{label}: {value}")
    if details:
        yield Result(state=State.OK, notice="\n".join(details))

    uptime = data.get("uptime_seconds")
    if uptime is not None:
        yield Result(state=State.OK, summary=f"Uptime: {render.timespan(uptime)}")


check_plugin_palo_alto_api_system = CheckPlugin(
    name="palo_alto_api_system",
    service_name="Palo Alto System",
    discovery_function=discover_palo_alto_api_system,
    check_function=check_palo_alto_api_system,
)
