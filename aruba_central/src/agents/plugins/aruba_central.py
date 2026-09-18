#!/usr/bin/env python3

"""
Aruba Central access point data via cencli

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

import json
import os
import pwd
import re
import shlex
import subprocess
import sys

CONFIG_FILE = os.path.join(os.environ.get("MK_CONFDIR", "/etc/check_mk"), "aruba_central.cfg")

COUNTS = re.compile(r"ap:\s*(\d+)\s*\((\d+):(\d+)\)")
CLIENTS = re.compile(r"clients:\s*(\d+)")
RATE_LIMIT = re.compile(r"API Rate Limit:\s*(\d+)\s+of\s+(\d+)\s+remaining")


def read_config():
    """Read the config file the bakery writes, KEY=VALUE per line."""
    config = {}
    try:
        with open(CONFIG_FILE, encoding="utf-8", errors="replace") as config_file:
            for line in config_file:
                key, sep, value = line.strip().partition("=")
                if sep and not key.startswith("#"):
                    config[key.strip()] = value.strip().strip("\"'")
    except OSError:
        pass
    return config


CONFIG = read_config()
CENCLI = CONFIG.get("CENCLI") or "cencli"
RUN_AS = CONFIG.get("RUN_AS") or ""
TIMEOUT = int(CONFIG.get("TIMEOUT") or 300)


def cencli_command():
    """The cencli call, wrapped into su or sudo when another user is configured."""
    command = shlex.split(CENCLI) + ["show", "aps", "-v", "--json"]

    if not RUN_AS or RUN_AS == pwd.getpwuid(os.geteuid()).pw_name:
        return command
    if os.geteuid() == 0:
        return ["su", "-", RUN_AS, "-c", shlex.join(command)]
    return ["sudo", "--non-interactive", "--login", "--user", RUN_AS] + command


def decode(data):
    """Decode cencli output as UTF-8, fall back to the Windows ANSI code page."""
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("cp1252", "replace")


def run_cencli():
    """Return exit code, stdout and stderr of the cencli call."""
    proc = subprocess.run(
        cencli_command(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=TIMEOUT,
        check=False,
    )
    return proc.returncode, decode(proc.stdout), decode(proc.stderr)


def find_json(text):
    """The JSON document cencli prints between its status lines."""
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end < start:
        return None

    try:
        return json.loads(text[start:end + 1])
    except ValueError:
        return None


def parse_status(text):
    """Pick the AP counts and the API rate limit out of the status lines."""
    status = {}

    if match := COUNTS.search(text):
        status["aps_total"] = int(match.group(1))
        status["aps_up"] = int(match.group(2))
        status["aps_down"] = int(match.group(3))

    if match := CLIENTS.search(text):
        status["clients"] = int(match.group(1))

    if match := RATE_LIMIT.search(text):
        status["rate_remaining"] = int(match.group(1))
        status["rate_limit"] = int(match.group(2))

    return status


def host_name(name, ap):
    """The AP name, or its serial when the name is just the MAC address."""
    if name.strip().lower() == str(ap.get("mac", "")).strip().lower():
        return ap.get("serial") or name
    return name


def main():
    """Print one status section and one piggyback section per access point."""
    aps = None

    try:
        returncode, stdout, stderr = run_cencli()
    except Exception as error:
        status = {"error": f"cencli could not be started: {error}"}
    else:
        # cencli mixes its status lines into both streams, the JSON is on one of them
        status = parse_status(stdout + stderr)
        aps = find_json(stdout)
        if aps is None:
            aps = find_json(stderr)
        if aps is None:
            status["error"] = f"no JSON in the output of cencli (exit code {returncode})"

    print("<<<aruba_central:sep(0)>>>")
    print(json.dumps(status))

    for name, ap in sorted((aps or {}).items()):
        if not isinstance(ap, dict):
            continue
        ap.setdefault("name", name)
        print(f"<<<<{host_name(name, ap)}>>>>")
        print("<<<aruba_ap:sep(0)>>>")
        print(json.dumps(ap))
        print("<<<<>>>>")

    return 0 if aps is not None else 1


if __name__ == "__main__":
    sys.exit(main())
