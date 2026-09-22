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

    if sudoers := conf.get("sudoers"):
        yield SystemConfig(
            base_os=OS.LINUX,
            lines=get_sudoers(conf, sudoers, interval),
            target=Path("sudoers.d") / SUDOERS_FILE,
            include_header=True,
        )


def get_sudoers(conf: Any, sudoers: Any, interval: int | None) -> list[str]:
    """The sudo rule that lets the agent user start the wrapper as the other user.

    sudo needs the absolute path of the command, and the bakery plug-in does not
    know the installation directory of the agent, so the rule has to name the
    plug-in directory. 'mk_logsudo.py --diag' prints the needed line on the host.
    """
    plugin_dir = sudoers["plugin_dir"].rstrip("/")
    wrapper = "/".join(part for part in (plugin_dir, str(interval or ""), PLUGIN) if part)
    return [
        "# Lets the Checkmk agent run mk_logwatch as another user.",
        f"{sudoers['agent_user']} ALL=({get_user(conf)}) NOPASSWD: {wrapper} --run",
    ]


register.bakery_plugin(
    name="mk_logwatch_sudo",
    files_function=get_files,
)
