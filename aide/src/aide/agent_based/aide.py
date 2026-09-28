#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

import re

from cmk.agent_based.v2 import (
    AgentSection,
    check_levels,
    CheckPlugin,
    Metric,
    render,
    Result,
    Service,
    State,
)

AIDE_ERRORS = {
    14: "error writing the database",
    15: "invalid argument",
    16: "unimplemented function",
    17: "invalid configuration line",
    18: "IO error (configuration or database not readable)",
    19: "version mismatch of the database",
    124: "timeout of cmk-aide-run reached",
    126: "aide is not executable",
    127: "aide not found",
}

ENTRY_TYPES = ("added", "removed", "changed")

RE_COUNT = re.compile(r"^\s*(Added|Removed|Changed) entries:\s*(\d+)\s*$")
RE_TOTAL = re.compile(r"^\s*(?:Total number|Number) of entries:\s*(\d+)\s*$")
RE_HEADER = re.compile(r"^(Added|Removed|Changed) entries:\s*$")
RE_ENTRY = re.compile(r"^(\S.*?)\s*: (/.*)$")
IGNORED_LINES = ("Start timestamp", "End timestamp", "AIDE found", "Summary:")


def _parse_output(job, lines):
    """Summary counts, entry lists and detail lines of an 'aide --check' output."""
    job["counts"] = {}
    job["entries"] = {kind: [] for kind in ENTRY_TYPES}
    job["details"] = []
    job["messages"] = []
    block = None
    for line in lines:
        if match := RE_COUNT.match(line):
            job["counts"][match.group(1).lower()] = int(match.group(2))
            continue
        if match := RE_TOTAL.match(line):
            job["total"] = int(match.group(1))
            continue
        if match := RE_HEADER.match(line):
            block = match.group(1).lower()
            continue
        if line.startswith("Detailed information about changes"):
            block = "details"
            continue
        if not line.strip() or set(line.strip()) == {"-"}:
            continue
        if block in ENTRY_TYPES:
            if match := RE_ENTRY.match(line):
                job["entries"][block].append((match.group(1).strip(), match.group(2)))
        elif block == "details":
            job["details"].append(line.rstrip())
        elif block is None and not line.startswith(IGNORED_LINES):
            job["messages"].append(line.strip())


def parse_aide(string_table):
    """Parse the header of the plug-in and one block per AIDE job."""
    section = {"jobs": {}}
    job = None
    output = None
    for (line,) in string_table:
        if line.startswith("[[[") and line.endswith("]]]"):
            job = section["jobs"].setdefault(line[3:-3], {})
            output = None
            continue
        if output is not None:
            output.append(line)
            continue
        if line == "[output]" and job is not None:
            output = job.setdefault("output", [])
            continue
        key, _, value = line.partition("=")
        target = section if job is None else job
        if key in ("now", "started", "finished", "exit", "timeout"):
            try:
                target[key] = int(value)
            except ValueError:
                continue
        else:
            target[key] = value

    now = section.get("now")
    for job in section["jobs"].values():
        job["now"] = now
        _parse_output(job, job.pop("output", []))
    return section


agent_section_aide = AgentSection(
    name="aide",
    parse_function=parse_aide,
)


def discover_aide(section):
    """One service per configured AIDE job."""
    for name in section["jobs"]:
        yield Service(item=name)


def _entry_lines(job, max_entries):
    """Lines for the details: changed paths first, then the AIDE detail block."""
    lines = []
    for kind in ENTRY_TYPES:
        for flags, path in job["entries"][kind]:
            lines.append(f"{kind}: {path} ({flags})")
    if len(lines) > max_entries:
        lines = lines[:max_entries] + [f"... {len(lines) - max_entries} more entries"]
    if job["details"]:
        details = job["details"][:max_entries * 3]
        lines += ["", "Details:"] + details
        if len(job["details"]) > len(details):
            lines.append("... (truncated)")
    return lines


def check_aide(item, params, section):
    """Check one AIDE job."""
    if runner_error := section.get("runner_error"):
        yield Result(state=State(params["state_error"]), summary=f"cmk-aide-run failed: {runner_error}")

    job = section["jobs"].get(item)
    if job is None:
        return

    if missing := job.get("missing"):
        yield Result(
            state=State(params["state_missing"]),
            summary=f"No result yet, {missing} does not exist",
            details=f"AIDE configuration: {job.get('config')}. Has cmk-aide-run run for this job?",
        )
        return

    if error := job.get("error"):
        yield Result(state=State(params["state_error"]), summary=error)
        return

    rc = job.get("exit")
    if rc is None:
        yield Result(state=State(params["state_error"]), summary="Result file is incomplete")
        return

    if rc == 0:
        total = job.get("total")
        yield Result(
            state=State.OK,
            summary="No differences" + (f" ({total} entries checked)" if total is not None else ""),
        )
    elif 1 <= rc <= 7:
        counts = job["counts"]
        if not counts:
            counts = {kind: 1 if rc & bit else 0 for kind, bit in zip(ENTRY_TYPES, (1, 2, 4))}
        text = ", ".join(f"{counts.get(kind, 0)} {kind}" for kind in ENTRY_TYPES)
        lines = _entry_lines(job, params["max_entries"])
        yield Result(
            state=State(params["state_changes"]),
            summary=f"Differences to the AIDE database: {text}",
            details="\n".join([f"Differences to the AIDE database: {text}", ""] + lines),
        )
        for kind in ENTRY_TYPES:
            yield Metric(f"aide_{kind}", counts.get(kind, 0))
    else:
        reason = AIDE_ERRORS.get(rc, "unexpected exit code")
        message = "; ".join(job["messages"][:3])
        yield Result(
            state=State(params["state_error"]),
            summary=f"AIDE check failed: {reason} (exit code {rc})"
            + (f": {message}" if message else ""),
        )

    now, finished = job.get("now"), job.get("finished")
    if now is not None and finished is not None:
        yield from check_levels(
            max(now - finished, 0),
            levels_upper=params["max_age"],
            render_func=render.timespan,
            label="Age of result",
        )
    else:
        yield Result(state=State(params["state_error"]), summary="Time of the last run is unknown")

    started = job.get("started")
    if started is not None and finished is not None:
        yield from check_levels(
            max(finished - started, 0),
            metric_name="aide_runtime",
            render_func=render.timespan,
            label="Runtime",
            notice_only=True,
        )
    if config := job.get("config"):
        yield Result(state=State.OK, notice=f"AIDE configuration: {config}")


check_plugin_aide = CheckPlugin(
    name="aide",
    service_name="AIDE %s",
    discovery_function=discover_aide,
    check_function=check_aide,
    check_ruleset_name="aide",
    check_default_parameters={
        "state_changes": 2,
        "state_error": 2,
        "state_missing": 2,
        "max_age": ("fixed", (10800.0, 21600.0)),
        "max_entries": 20,
    },
)
