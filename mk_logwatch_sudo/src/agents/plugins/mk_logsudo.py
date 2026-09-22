#!/usr/bin/env python3

"""
Runs the mk_logwatch of the agent as another user through sudo

The file name is deliberately sorted before 'mk_logwatch.py': the agent walks its
plug-in directory in collation order and asks for the execute bit of every entry
right before it runs it. Running first is what lets this plug-in take the shipped
mk_logwatch out of that same run.

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

import os
import pwd
import stat
import subprocess
import sys
import time

# Read by the agent for the <<<checkmk_agent_plugins_lnx>>> section, so that the
# agent output names the version of this plug-in.
CMK_VERSION = "1.0.0"

CONFIG_NAME = "mk_logsudo.cfg"
LOG_NAME = "mk_logsudo.log"
CHILD_ARG = "--run"
# Exit code of the child when it has written its own logwatch message already.
REPORTED = 99
LOGWATCH_NAMES = ("mk_logwatch.py", "mk_logwatch")
MAX_LOG_SIZE = 64 * 1024

DEFAULT_CONFDIR = "/etc/check_mk"
DEFAULT_VARDIR = "/var/lib/check_mk_agent"
DEFAULT_TIMEOUT = 120


def get_libdir():
    """The agent library directory, from the environment or from our own path."""
    if libdir := os.environ.get("MK_LIBDIR"):
        return libdir.rstrip("/")

    # <libdir>/plugins/mk_logsudo.py, or <libdir>/plugins/<interval>/... when the
    # plug-in is deployed with a cache age.
    here = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
    if os.path.basename(here).isdigit():
        here = os.path.dirname(here)
    return os.path.dirname(here)


def get_dirs():
    """Library, configuration and state directory of the agent.

    sudo drops the environment, so the child has to find the directories itself.
    Both layouts the agent supports are derived from the library directory: the
    classic one with its fixed paths, and the single directory deployment of the
    rule 'Customize agent package', where the library directory is
    <installdir>/package.
    """
    libdir = get_libdir()

    if os.path.basename(libdir) == "package":
        confdir = os.path.join(libdir, "config")
        vardir = os.path.join(os.path.dirname(libdir), "runtime")
    else:
        confdir = DEFAULT_CONFDIR
        vardir = DEFAULT_VARDIR

    return (
        libdir,
        os.environ.get("MK_CONFDIR") or confdir,
        os.environ.get("MK_VARDIR") or vardir,
    )


def read_config(confdir):
    """Read the config file the bakery writes, KEY=VALUE per line."""
    config = {}
    try:
        with open(os.path.join(confdir, CONFIG_NAME), encoding="utf-8", errors="replace") as cfg:
            for line in cfg:
                key, sep, value = line.strip().partition("=")
                if sep and not key.startswith("#"):
                    config[key.strip()] = value.strip().strip("\"'")
    except OSError:
        pass
    return config


def logwatch_candidates(libdir):
    """The places the mk_logwatch of the 'Text logfiles' rule can be in."""
    plugins_dir = os.path.join(libdir, "plugins")

    directories = [plugins_dir]
    try:
        # Deployed with a cache age, the agent puts it into plugins/<interval>.
        directories += [
            os.path.join(plugins_dir, entry)
            for entry in sorted(os.listdir(plugins_dir))
            if entry.isdigit()
        ]
    except OSError:
        pass

    return [
        os.path.join(directory, name) for directory in directories for name in LOGWATCH_NAMES
    ]


def find_plugin(config, libdir):
    """Path of the original mk_logwatch, wherever the agent package put it."""
    if plugin := config.get("PLUGIN"):
        return plugin

    for candidate in logwatch_candidates(libdir):
        if os.path.isfile(candidate):
            return candidate
    return ""


def note(vardir, message):
    """Write a line about a change on the host, next to the state files."""
    path = os.path.join(vardir, LOG_NAME)
    try:
        if os.path.exists(path) and os.path.getsize(path) > MAX_LOG_SIZE:
            return
        with open(path, "a", encoding="utf-8") as log:
            log.write("%s %s\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), message))
    except OSError:
        pass


def take_execute_bit(plugin, vardir):
    """Keep the agent from running the shipped mk_logwatch by itself.

    The agent only runs files that carry an execute bit and checks that right
    before it runs them, so this is what takes it out of the same agent call.
    Nothing but the mode of the file is changed, an agent update brings the bit
    back and the next run removes it again.
    """
    try:
        mode = stat.S_IMODE(os.stat(plugin).st_mode)
    except OSError:
        return True

    if not mode & 0o111:
        return True

    try:
        os.chmod(plugin, mode & ~0o111)
    except OSError as error:
        note(vardir, "could not take the execute bit from %s: %s" % (plugin, error))
        return False

    note(vardir, "took the execute bit from %s (was 0%o, undo: chmod 0%o %s)" % (
        plugin, mode, mode, plugin))
    return True


def current_user():
    """Name of the user this plug-in runs as."""
    try:
        return pwd.getpwuid(os.geteuid()).pw_name
    except KeyError:
        return ""


def report(message, state="C"):
    """Report a problem as a logwatch message, so that it shows up in Checkmk."""
    sys.stdout.write(
        "<<<logwatch>>>\n[[[mk_logsudo]]]\n%s %s\n" % (state, message.replace("\n", " "))
    )
    # os.execve does not flush what Python has buffered.
    sys.stdout.flush()


def interpreter(plugin):
    """The call of the plug-in, with its shebang when it is not executable."""
    if os.access(plugin, os.X_OK):
        return [plugin]
    try:
        with open(plugin, encoding="utf-8", errors="replace") as plugin_file:
            first_line = plugin_file.readline().strip()
    except OSError:
        first_line = ""
    if first_line.startswith("#!"):
        return first_line[2:].split() + [plugin]
    return [sys.executable or "python3", plugin]


def run_child(config, dirs):
    """Replace this process with mk_logwatch, with the agent directories set."""
    libdir, confdir, vardir = dirs

    if not (plugin := find_plugin(config, libdir)):
        report(
            "No mk_logwatch below %s/plugins. It is deployed by the rule "
            "'Text logfiles (Linux, UNIX, Windows)'." % libdir
        )
        return REPORTED

    state_dir = config.get("STATE_DIR") or vardir

    if not take_execute_bit(plugin, state_dir):
        report(
            "%s is still executable, %s may not change its mode. The agent runs it as "
            "well and logwatch reports everything twice. Do it by hand: "
            "chmod a-x %s" % (plugin, current_user(), plugin),
            state="W",
        )

    environ = dict(os.environ)
    environ["MK_LIBDIR"] = libdir
    environ["MK_CONFDIR"] = confdir
    environ["MK_VARDIR"] = state_dir

    try:
        os.makedirs(environ["MK_VARDIR"], mode=0o700, exist_ok=True)
    except OSError as error:
        report("Cannot create the state directory %s: %s" % (environ["MK_VARDIR"], error))
        return REPORTED

    command = interpreter(plugin)
    try:
        os.execve(command[0], command, environ)
    except OSError as error:
        report("Cannot run %s: %s" % (plugin, error))
    return REPORTED


def have_sudo():
    """Whether sudo can be called."""
    for directory in (os.environ.get("PATH") or "/usr/bin:/bin:/usr/sbin:/sbin").split(":"):
        if directory and os.access(os.path.join(directory, "sudo"), os.X_OK):
            return True
    return False


def build_command(user):
    """The call of this plug-in as the configured user."""
    child = [os.path.realpath(os.path.abspath(__file__)), CHILD_ARG]

    if have_sudo():
        return ["sudo", "--non-interactive", "--user", user] + child
    if os.geteuid() == 0:
        return ["su", "-s", "/bin/sh", user, "-c", " ".join(child)]
    return []


def run_parent(config, dirs):
    """Call mk_logwatch as the configured user and pass its output through."""
    user = config.get("USER") or "root"
    timeout = int(config.get("TIMEOUT") or DEFAULT_TIMEOUT)

    if user == current_user():
        return run_child(config, dirs)

    if not (command := build_command(user)):
        report("sudo is not available, cannot run mk_logwatch as %s" % user)
        return 1

    try:
        # stdout is inherited, so the logwatch sections reach the agent unchanged.
        proc = subprocess.run(
            command,
            stdout=None,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
    except OSError as error:
        report("Cannot run %s: %s" % (command[0], error))
        return 1
    except subprocess.TimeoutExpired:
        report("mk_logwatch did not finish within %d seconds as user %s" % (timeout, user))
        return 1

    if proc.returncode == REPORTED:
        # The child has written its own logwatch message.
        return 1

    if proc.returncode != 0:
        error = proc.stderr.decode("utf-8", "replace").strip() or "exit code %d" % proc.returncode
        report("mk_logwatch failed as user %s: %s" % (user, " | ".join(error.splitlines()[-3:])))
        return 1

    return 0


def main():
    """Parent or child, depending on the argument sudo was called with."""
    dirs = get_dirs()
    config = read_config(dirs[1])

    if CHILD_ARG in sys.argv[1:]:
        return run_child(config, dirs)
    return run_parent(config, dirs)


if __name__ == "__main__":
    sys.exit(main())
