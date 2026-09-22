#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from pathlib import Path
from typing import Any  # type: ignore

from cmk.base.cee.plugins.bakery.bakery_api.v1 import (
    FileGenerator,
    OS,
    Plugin,
    PluginConfig,
    register,
    SystemConfig,
)

# Sorted before mk_logwatch.py on purpose, see the plug-in itself.
PLUGIN = "mk_logsudo.py"
DEFAULT_PLUGINS_DIR = "/usr/lib/check_mk_agent/plugins"
DEFAULT_TIMEOUT = 120
SUDOERS_FILE = "check_mk_mk_logsudo"


def get_deployment(conf: Any) -> tuple[bool, int | None]:
    """Whether the plug-in is deployed, and its cache age when it runs asynchronously."""
    match conf.get("deployment", ("do_not_deploy", None)):
        case "cached", float(raw_interval):
            return True, int(raw_interval)
        case "sync", _:
            return True, None
    return False, None


def get_user(conf: Any) -> str:
    """The user mk_logwatch is run as."""
    return conf.get("user") or "root"


def get_plugins_dir(conf: Any) -> str:
    """The agent plug-in directory on the host, needed for the sudo rule."""
    return (conf.get("plugins_dir") or DEFAULT_PLUGINS_DIR).rstrip("/")


def get_config(conf: Any) -> list[str]:
    """Lines of the plug-in configuration file."""
    lines = [
        f'USER="{get_user(conf)}"',
        f'TIMEOUT="{int(conf.get("timeout", DEFAULT_TIMEOUT))}"',
    ]

    if plugin_path := conf.get("plugin_path"):
        lines.append(f'PLUGIN="{plugin_path}"')

    if state_dir := conf.get("state_dir"):
        lines.append(f'STATE_DIR="{state_dir}"')

    return lines


def get_files(conf: Any) -> FileGenerator:
    """Deploy the wrapper and its configuration.

    mk_logwatch itself is not deployed here. The wrapper calls the one of the
    rule 'Text logfiles (Linux, UNIX, Windows)' on the host and takes its execute
    bit, so that the agent does not run it a second time.
    """
    deploy, interval = get_deployment(conf)
    if not deploy:
        return

    yield Plugin(
        base_os=OS.LINUX,
        source=Path(PLUGIN),
        interval=interval,
    )

    yield PluginConfig(
        base_os=OS.LINUX,
        lines=get_config(conf),
        target=Path("mk_logsudo.cfg"),
        include_header=True,
    )

    if agent_user := conf.get("sudoers", {}).get("agent_user"):
        yield SystemConfig(
            base_os=OS.LINUX,
            lines=get_sudoers(conf, agent_user, interval),
            target=Path("sudoers.d") / SUDOERS_FILE,
            include_header=True,
        )


def get_sudoers(conf: Any, agent_user: str, interval: int | None) -> list[str]:
    """The sudo rule that lets the agent user start the wrapper as the other user."""
    wrapper = "/".join(part for part in (get_plugins_dir(conf), str(interval or ""), PLUGIN) if part)
    return [
        "# Lets the Checkmk agent run mk_logwatch as another user.",
        f"{agent_user} ALL=({get_user(conf)}) NOPASSWD: {wrapper} --run",
    ]


register.bakery_plugin(
    name="mk_logwatch_sudo",
    files_function=get_files,
)
