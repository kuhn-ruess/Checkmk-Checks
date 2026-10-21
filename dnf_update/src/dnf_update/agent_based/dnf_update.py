#!/usr/bin/env python3
"""
DNF updates

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

import re
from dataclasses import dataclass, field

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Metric,
    Result,
    Service,
    State,
    StringTable,
    render,
)

RE_PACKAGE = re.compile(r"^(\S+)\.(\S+)\s+(\S+)\s+(\S+)$")
RE_FAILED_REPO = re.compile(r"Failed to download metadata for repo '([^']+)'")
RE_IGNORED_REPOS = re.compile(r"^Ignoring repositories:\s*(.+)$")
RE_URL = re.compile(r"https?://[^\s\]\)]+")


@dataclass
class Command:
    """Exit code and output of one command of the agent plug-in."""

    exit_code: int | None = None
    lines: list[str] = field(default_factory=list)


@dataclass
class Section:
    """Parsed agent output of dnf_update."""

    info: dict[str, str] = field(default_factory=dict)
    commands: dict[str, Command] = field(default_factory=dict)

    def command(self, name: str) -> Command | None:
        """The output of one command, None if the agent did not run it."""
        return self.commands.get(name)


def parse_dnf_update(string_table: StringTable) -> Section:
    """Split the agent output into the info block and the command outputs."""
    section = Section()
    current = None
    for (line,) in string_table:
        if line.startswith("[[[") and line.endswith("]]]"):
            current = line[3:-3]
            if current != "info":
                section.commands[current] = Command()
            continue
        if current == "info":
            key, _, value = line.partition("=")
            section.info[key] = value
        elif current is not None:
            command = section.commands[current]
            if command.exit_code is None and line.startswith("exit="):
                try:
                    command.exit_code = int(line[5:])
                except ValueError:
                    pass
                continue
            command.lines.append(line)
    return section


agent_section_dnf_update = AgentSection(
    name="dnf_update",
    parse_function=parse_dnf_update,
)


def packages(command: Command | None) -> set[str]:
    """Names of the packages listed by dnf check-update."""
    if command is None:
        return set()
    names = set()
    for line in command.lines:
        if line.startswith("Obsoleting Packages"):
            break
        if line[:1].isspace():
            continue
        if match := RE_PACKAGE.match(line.strip()):
            names.add(f"{match.group(1)}.{match.group(2)}")
    return names


def failed_repos(command: Command | None) -> tuple[list[str], list[str]]:
    """Repositories dnf could not reach, and the URLs it tried."""
    if command is None:
        return [], []
    repos: list[str] = []
    urls: list[str] = []
    for line in command.lines:
        for repo in RE_FAILED_REPO.findall(line):
            if repo not in repos:
                repos.append(repo)
        if match := RE_IGNORED_REPOS.match(line.strip()):
            for repo in match.group(1).split(","):
                if (repo := repo.strip()) and repo not in repos:
                    repos.append(repo)
        for url in RE_URL.findall(line):
            url = url.removesuffix("/repodata/repomd.xml")
            if url not in urls:
                urls.append(url)
    return repos, urls


def timer_details(info: dict[str, str]) -> str:
    """Last and next run of the dnf-automatic timer for the details."""
    if "timer" not in info:
        return "No dnf-automatic timer found"
    last = render.datetime(int(info["last_run"])) if "last_run" in info else "never"
    upcoming = render.datetime(int(info["next_run"])) if "next_run" in info else "unknown"
    return f"{info['timer']}: last run: {last}, next run: {upcoming}"


def skip_reason(params: dict, info: dict[str, str]) -> str | None:
    """Why the update check is skipped at the moment, None if it is not."""
    week_mode = params.get("update_week", "any")
    if week_mode != "any" and info.get("iso_week", "").isdigit():
        week = int(info["iso_week"])
        if (week % 2 == 0) != (week_mode == "even"):
            return f"ISO week {week} is no update week (updates in {week_mode} weeks), updates are not checked"

    if "last_run" not in info:
        return None
    if info.get("last_run_day") and info.get("last_run_day") == info.get("today"):
        return "Updates already ran today, updates are not checked"

    window_mode, days = params.get("window", ("days", 3))
    if window_mode == "days":
        last_run = int(info["last_run"])
        now = int(info.get("now", last_run))
        if not last_run <= now <= last_run + int(days) * 86400:
            return f"The {days} day window after the last update run has expired, updates are not checked"
    return None


def reboot_result(params: dict, section: Section) -> Result | None:
    """Result if installed updates need a reboot."""
    state = State(params["state_reboot"])
    needs_restarting = section.command("needs_restarting")
    if needs_restarting is not None and needs_restarting.exit_code in (0, 1):
        if needs_restarting.exit_code == 0:
            return None
        return Result(
            state=state,
            summary="Reboot required to fully utilize the installed updates",
            details="\n".join(line for line in needs_restarting.lines if line.strip()),
        )

    kernel = section.command("kernel")
    if kernel is None:
        return None
    values = dict(line.partition("=")[::2] for line in kernel.lines)
    running, latest = values.get("running"), values.get("latest")
    if running and latest and running != latest:
        return Result(
            state=state,
            summary=f"Reboot required, kernel {latest} is installed but {running} is running",
        )
    return None


def discover_dnf_update(section: Section) -> DiscoveryResult:
    """One service per host that runs the agent plug-in."""
    if section.command("check_update") is not None:
        yield Service()


def check_dnf_update(params: dict, section: Section) -> CheckResult:
    """Evaluate repositories, veto file, update window, reboot state and pending updates."""
    info = section.info
    timer = Result(state=State.OK, notice=timer_details(info))
    check_update = section.command("check_update")
    stderr = section.command("check_update_stderr")

    repos, urls = failed_repos(stderr)
    if repos:
        yield Result(
            state=State(params["state_repo"]),
            summary=f"Repository not reachable: {', '.join(repos)}",
            details="Affected URLs:\n" + ("\n".join(urls) if urls else "none found in the dnf output"),
        )
        yield timer
        return

    if check_update is None or check_update.exit_code not in (0, 100):
        message = next(
            (line.strip() for line in reversed(stderr.lines if stderr else []) if line.strip()),
            "no error message",
        )
        yield Result(state=State.UNKNOWN, summary=f"dnf check-update failed: {message}")
        yield timer
        return

    if info.get("veto") == "1":
        yield Result(
            state=State(params["state_veto"]),
            summary=f"Veto file {info.get('veto_file', '')} exists, automatic updates are disabled",
        )
        yield timer
        return

    if reason := skip_reason(params, info):
        yield Result(state=State.OK, summary=reason)
        yield timer
        return

    if reboot := reboot_result(params, section):
        yield reboot

    total = packages(check_update)
    security_command = section.command("security")
    if security_command is None or security_command.exit_code not in (0, 100):
        yield Result(state=State.UNKNOWN, summary="Security updates could not be determined")
        security = set()
    else:
        security = packages(security_command) & total if total else packages(security_command)
    normal = len(total - security)

    yield Result(
        state=State(params["state_security"]) if security else State.OK,
        summary=f"{len(security)} security updates available",
    )
    yield Result(
        state=State(params["state_normal"]) if normal else State.OK,
        summary=f"{normal} non-security updates available",
    )
    yield Result(state=State.OK, notice=f"{len(total | security)} total updates available")
    yield Metric("security_updates", len(security))
    yield Metric("normal_updates", normal)
    yield timer


check_plugin_dnf_update = CheckPlugin(
    name="dnf_update",
    service_name="DNF updates",
    discovery_function=discover_dnf_update,
    check_function=check_dnf_update,
    check_ruleset_name="dnf_update",
    check_default_parameters={
        "window": ("days", 3),
        "update_week": "any",
        "state_security": 2,
        "state_normal": 1,
        "state_reboot": 2,
        "state_veto": 2,
        "state_repo": 2,
    },
)
