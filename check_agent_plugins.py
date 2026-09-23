#!/usr/bin/env python3
"""Check agent plugins for syntax that old Python interpreters cannot parse.

Agent plug-ins run on the monitored host, not on the Checkmk site, so they have
to start on whatever Python that host brings - RHEL 8 and SLES 15 still ship
3.6. A construct from a newer version is a syntax error, and a syntax error
kills the plug-in before its first line runs: the agent delivers no section at
all and nothing in Checkmk says why.

    ./check_agent_plugins.py                 # all packages
    ./check_agent_plugins.py mk_logwatch_sudo
    ./check_agent_plugins.py --floor 3.4 mk_logwatch_sudo
    ./check_agent_plugins.py --python /usr/bin/python3.6 mk_logwatch_sudo

With --python the file is additionally compiled by that interpreter, which is
the real proof. Without it the check is done on the syntax tree.
"""
import argparse
import ast
import glob
import re
import subprocess
import sys

DEFAULT_FLOOR = (3, 6)

# Constructs that fail at parse time, with the version that introduced them.
NODE_FEATURES = [
    ("NamedExpr", (3, 8), "walrus operator ':='"),
    ("Match", (3, 10), "match statement"),
    ("TryStar", (3, 11), "except* clause"),
    ("TypeAlias", (3, 12), "type statement"),
    ("JoinedStr", (3, 6), "f-string"),
    ("AnnAssign", (3, 6), "variable annotation"),
    ("AsyncFunctionDef", (3, 5), "async def"),
    ("Await", (3, 5), "await"),
]

# Things that parse but fail when they run.
SOURCE_FEATURES = [
    (re.compile(r"""f["'][^"']*\{[^{}]*=\}"""), (3, 8), "f-string '=' specifier"),
    (re.compile(r"\.removeprefix\(|\.removesuffix\("), (3, 9), "str.removeprefix/removesuffix"),
    (re.compile(r"\bshlex\.join\("), (3, 8), "shlex.join"),
    (re.compile(r"\bmath\.prod\("), (3, 8), "math.prod"),
    (re.compile(r"\bcapture_output\s*="), (3, 7), "subprocess capture_output"),
    (re.compile(r"\bsubprocess\.run\([^)]*\btext\s*="), (3, 7), "subprocess text="),
    (re.compile(r"\bfromisoformat\("), (3, 7), "datetime.fromisoformat"),
    (re.compile(r"^\s*(from|import)\s+dataclasses\b", re.M), (3, 7), "dataclasses"),
    (re.compile(r"\bfunctools\.cached_property\b"), (3, 8), "functools.cached_property"),
    (re.compile(r"\bimportlib\.metadata\b"), (3, 8), "importlib.metadata"),
]


def version(number):
    """3.6 as a tuple."""
    return tuple(int(part) for part in number.split("."))


def find_posonly(tree):
    """Positional only parameters, 3.8 and newer."""
    for node in ast.walk(tree):
        if isinstance(node, ast.arguments) and getattr(node, "posonlyargs", []):
            return True
    return False


def check_source(path, floor):
    """Findings of one file, as (line, version, description)."""
    with open(path, encoding="utf-8", errors="replace") as source_file:
        source = source_file.read()

    try:
        tree = ast.parse(source, filename=path)
    except SyntaxError as error:
        return [(error.lineno or 0, None, "does not even parse here: %s" % error.msg)]

    findings = []

    for name, since, description in NODE_FEATURES:
        node_type = getattr(ast, name, None)
        if node_type is None or since <= floor:
            continue
        for node in ast.walk(tree):
            if isinstance(node, node_type):
                findings.append((getattr(node, "lineno", 0), since, description))

    if (3, 8) > floor and find_posonly(tree):
        findings.append((0, (3, 8), "positional only parameters"))

    for pattern, since, description in SOURCE_FEATURES:
        if since <= floor:
            continue
        for match in pattern.finditer(source):
            findings.append((source[: match.start()].count("\n") + 1, since, description))

    return sorted(set(findings))


def compile_with(interpreter, path):
    """Let another interpreter parse the file. Returns an error text or ''."""
    proc = subprocess.run(
        [interpreter, "-m", "py_compile", path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if proc.returncode == 0:
        return ""
    return proc.stdout.decode("utf-8", "replace").strip().splitlines()[-1]


def agent_plugins(packages):
    """The agent plug-in sources of the given packages, or of all of them."""
    names = packages or ["*"]
    paths = []
    for name in names:
        paths += glob.glob("%s/src/agents/**/*.py" % name, recursive=True)
    return sorted(path for path in paths if "__pycache__" not in path)


def main():
    """Check every agent plug-in and report what would break."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packages", nargs="*", help="package directories, default all")
    parser.add_argument("--floor", default="%d.%d" % DEFAULT_FLOOR,
                        help="oldest Python that has to parse the plug-ins")
    parser.add_argument("--python", help="additionally compile with this interpreter")
    args = parser.parse_args()

    floor = version(args.floor)
    paths = agent_plugins(args.packages)
    if not paths:
        print("No agent plug-ins found")
        return 1

    failed = 0
    for path in paths:
        findings = check_source(path, floor)
        if args.python:
            error = compile_with(args.python, path)
            if error:
                findings.append((0, None, "%s: %s" % (args.python, error)))

        if findings:
            failed += 1
            print("FAIL %s" % path)
            for line, since, description in findings:
                needs = "needs %d.%d" % since if since else "error"
                print("     line %-4s %-12s %s" % (line or "?", needs, description))
        else:
            print("ok   %s" % path)

    print()
    print("%d file(s) checked against Python %s, %d with findings"
          % (len(paths), args.floor, failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
