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
    WindowsConfigGenerator,
    WindowsConfigItems,
)

try:
    from cmk.base.cee.plugins.bakery.bakery_api.v1 import password_store
except ImportError:
    from cmk.utils import password_store

WINDOWS_PATTERN = "$CUSTOM_PLUGINS_PATH$\\aruba_central.ps1"
DEFAULT_TIMEOUT = 300


def get_deployment(conf: Any) -> tuple[bool, int | None]:
    """Whether the plugin is deployed, and its cache age when it runs asynchronously."""
    match conf.get("deployment", ("do_not_deploy", None)):
        case "cached", float(raw_interval):
            return True, int(raw_interval)
        case "sync", _:
            return True, None
    return False, None


def get_timeout(conf: Any) -> int:
    """The maximum runtime of the cencli call."""
    return int(conf.get("timeout", DEFAULT_TIMEOUT))


def get_password(password: Any) -> str:
    """Resolve a password of the ruleset against the password store."""
    match password:
        case "cmk_postprocessed", "explicit_password", (_ident, str(secret)):
            return secret
        case "cmk_postprocessed", "stored_password", (str(ident), _):
            return password_store.extract(ident)
        case ("password" | "store", _):
            return password_store.extract(password)
    return ""


def get_config(conf: Any, base_os: OS) -> list[str]:
    """Lines of the plugin configuration file."""
    lines = [f'TIMEOUT="{get_timeout(conf)}"']

    if cencli := conf.get("cencli"):
        lines.append(f'CENCLI="{cencli}"')

    # On Windows the agent itself starts the plugin as the configured user.
    if base_os is OS.LINUX and (run_as := conf.get("run_as")):
        lines.append(f'RUN_AS="{run_as["user"]}"')

    return lines


def get_files(conf: Any) -> FileGenerator:
    """Deploy the cencli plugin for Linux and Windows."""
    deploy, interval = get_deployment(conf)
    if not deploy:
        return

    yield Plugin(
        base_os=OS.LINUX,
        source=Path("aruba_central.py"),
        interval=interval,
    )
    yield PluginConfig(
        base_os=OS.LINUX,
        lines=get_config(conf, OS.LINUX),
        target=Path("aruba_central.cfg"),
        include_header=True,
    )

    # The execution entry of the Windows plugin is built by get_windows_config,
    # so that the cache age, the timeout and the user end up in one entry.
    yield Plugin(
        base_os=OS.WINDOWS,
        source=Path("aruba_central.ps1"),
    )
    yield PluginConfig(
        base_os=OS.WINDOWS,
        lines=get_config(conf, OS.WINDOWS),
        target=Path("aruba_central.cfg"),
        include_header=True,
    )


def get_windows_config(conf: Any) -> WindowsConfigGenerator:
    """Execution entry of the Windows agent, including the user context."""
    deploy, interval = get_deployment(conf)
    if not deploy:
        return

    entry: dict[str, Any] = {
        "pattern": WINDOWS_PATTERN,
        "run": True,
        "async": interval is not None,
        "timeout": get_timeout(conf),
    }

    if interval is not None:
        entry["cache_age"] = interval

    if run_as := conf.get("run_as"):
        if password := get_password(run_as.get("password")):
            entry["user"] = f"{run_as['user']} {password}"

    yield WindowsConfigItems(
        path=["plugins", "execution"],
        content=[entry],
    )


register.bakery_plugin(
    name="aruba_central",
    files_function=get_files,
    windows_config_function=get_windows_config,
)
