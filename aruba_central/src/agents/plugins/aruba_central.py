#!/usr/bin/env python3

"""
Aruba Central access point data via cencli

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

import json
import os
import re
import subprocess
import sys

COMMAND = os.environ.get("ARUBA_CENCLI", "cencli").split() + [
    "show", "aps", "-v", "--json",
]
TIMEOUT = int(os.environ.get("ARUBA_CENCLI_TIMEOUT", "300"))

COUNTS = re.compile(r"ap:\s*(\d+)\s*\((\d+):(\d+)\)")
CLIENTS = re.compile(r"clients:\s*(\d+)")
RATE_LIMIT = re.compile(r"API Rate Limit:\s*(\d+)\s+of\s+(\d+)\s+remaining")


def run_cencli():
    """Return stdout and stderr of the cencli call."""
    proc = subprocess.run(
        COMMAND,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=TIMEOUT,
        check=False,
    )
    return (
        proc.returncode,
        proc.stdout.decode("utf-8", "replace"),
        proc.stderr.decode("utf-8", "replace"),
    )


def split_json(text):
    """Split the JSON document from the status lines cencli mixes into its output."""
    start = text.find("{")
    if start < 0:
        return None, text

    try:
        data, end = json.JSONDecoder().raw_decode(text[start:])
    except ValueError:
        return None, text

    return data, text[:start] + text[start + end:]


def parse_status(text):
    """Pick the AP counts and the API rate limit out of the remaining output."""
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
    try:
        returncode, stdout, stderr = run_cencli()
    except Exception as error:
        sys.stderr.write(f"aruba_central: {error}\n")
        return 1

    aps, rest = split_json(stdout)
    if aps is None:
        aps, rest = split_json(stderr)
        rest = stdout + rest
    else:
        rest = rest + stderr

    status = parse_status(rest)
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

    return 0


if __name__ == "__main__":
    sys.exit(main())
