#!/usr/bin/env python3
"""
mk_logwatch via sudo - agent plugin deployment

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.rulesets.v1 import Help, Label, Title
from cmk.rulesets.v1.form_specs import (
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
    DefaultValue,
    DictElement,
    Dictionary,
    FixedValue,
    InputHint,
    String,
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange
from cmk.rulesets.v1.rule_specs import AgentConfig, Topic


def _sudoers() -> Dictionary:
    return Dictionary(
        title=Title("Deploy the sudo rule"),
        help_text=Help(
            "Writes <tt>/etc/sudoers.d/check_mk_mk_logsudo</tt> with the one "
            "line the agent user needs to start the wrapper as the configured user. "
            "Leave this out when the sudo configuration is managed elsewhere, the "
            "rule is then expected on the host as "
            "<tt>&lt;agent user&gt; ALL=(&lt;user&gt;) NOPASSWD: "
            "&lt;plug-in directory&gt;/mk_logsudo.py --run</tt>. "
            "An agent that runs as root needs no sudo rule at all."
        ),
        elements={
            "agent_user": DictElement(
                required=True,
                parameter_form=String(
                    title=Title("User the Checkmk agent runs as"),
                    help_text=Help(
                        "The user of the rule <i>Customize agent package (Linux)</i>, "
                        "<tt>cmk-agent</tt> by default in a non-root deployment."
                    ),
                    custom_validate=(LengthInRange(min_value=1),),
                    prefill=DefaultValue("cmk-agent"),
                ),
            ),
        },
    )


def _agent_config_mk_logwatch_sudo() -> Dictionary:
    return Dictionary(
        help_text=Help(
            "Runs the <tt>mk_logwatch</tt> that is installed on the host as another "
            "user through <tt>sudo</tt>, for log files the user of the agent cannot "
            "read, or for log files that must not be read as root.<br>"
            "Nothing of logwatch is deployed by this rule: the wrapper looks for the "
            "mk_logwatch of the rule <i>Text logfiles (Linux, UNIX, Windows)</i> in "
            "the plug-in directory of the agent and calls exactly that file, so the "
            "version on the host always stays the one of the agent package. "
            "<tt>logwatch.cfg</tt> and <tt>logwatch.d</tt> are read as usual and the "
            "output reaches the agent unchanged, so the logwatch services stay the "
            "same.<br>"
            "<b>The wrapper takes the execute bit from the shipped mk_logwatch</b> on "
            "its first run, otherwise the agent would run it a second time as the "
            "agent user and every message would be reported twice. Nothing else about "
            "that file is changed, it is not moved and not deleted. The wrapper is "
            "called before it in the same agent run, so this already works on the "
            "first call. An agent update brings the bit back, the next agent call "
            "removes it again; every change is written to <tt>mk_logsudo.log</tt> in "
            "the state directory of the agent, including the command to undo it "
            "(<tt>chmod 0755 &lt;path&gt;</tt>). If the configured user may not change "
            "the file, the wrapper reports that as a warning of the log file "
            "<tt>mk_logsudo</tt> instead.<br>"
            "Deploy the wrapper synchronously. With a cache age it may run after the "
            "shipped plug-in, which delays the takeover."
        ),
        elements={
            "deployment": DictElement(
                required=True,
                parameter_form=CascadingSingleChoice(
                    title=Title("Deployment type"),
                    elements=(
                        CascadingSingleChoiceElement(
                            name="sync",
                            title=Title("Deploy the plug-in and run it synchronously"),
                            parameter_form=FixedValue(
                                value=None,
                                label=Label(
                                    "The normal deployment of mk_logwatch: every agent "
                                    "call delivers the new log lines."
                                ),
                            ),
                        ),
                        CascadingSingleChoiceElement(
                            name="cached",
                            title=Title("Deploy the plug-in and run it asynchronously"),
                            parameter_form=TimeSpan(
                                title=Title("Cache age"),
                                help_text=Help(
                                    "Only for hosts with very many or very large log "
                                    "files. Between two runs the log lines stay on the "
                                    "host, the state file makes sure that none of them "
                                    "are lost."
                                ),
                                displayed_magnitudes=(
                                    TimeMagnitude.HOUR,
                                    TimeMagnitude.MINUTE,
                                ),
                                prefill=DefaultValue(300.0),
                            ),
                        ),
                        CascadingSingleChoiceElement(
                            name="do_not_deploy",
                            title=Title("Do not deploy the plug-in"),
                            parameter_form=FixedValue(value=None),
                        ),
                    ),
                    prefill=DefaultValue("sync"),
                ),
            ),
            "user": DictElement(
                required=True,
                parameter_form=String(
                    title=Title("Run mk_logwatch as this user"),
                    help_text=Help(
                        "The user the log files are read as. It needs read access to "
                        "the log files, to the agent configuration directory and to "
                        "the state directory, and it should be able to change the mode "
                        "of the shipped mk_logwatch, which normally belongs to root. "
                        "The agent user needs a sudo rule for it."
                    ),
                    custom_validate=(LengthInRange(min_value=1),),
                    prefill=DefaultValue("root"),
                ),
            ),
            "timeout": DictElement(
                parameter_form=TimeSpan(
                    title=Title("Maximum runtime"),
                    help_text=Help(
                        "The wrapper stops the call after this time and reports it as "
                        "a logwatch message. Keep it below the timeout of the agent."
                    ),
                    displayed_magnitudes=(
                        TimeMagnitude.MINUTE,
                        TimeMagnitude.SECOND,
                    ),
                    prefill=DefaultValue(120.0),
                ),
            ),
            "plugins_dir": DictElement(
                parameter_form=String(
                    title=Title("Agent plug-in directory on the host"),
                    help_text=Help(
                        "Only needed for the sudo rule, the wrapper itself finds its "
                        "directories on its own. Default is "
                        "<tt>/usr/lib/check_mk_agent/plugins</tt>; "
                        "with a single directory deployment of the rule <i>Customize "
                        "agent package (Linux)</i> it is "
                        "<tt>&lt;installation directory&gt;/default/package/plugins</tt>, "
                        "<tt>/opt/checkmk/agent/default/package/plugins</tt> by default."
                    ),
                    prefill=InputHint("/usr/lib/check_mk_agent/plugins"),
                ),
            ),
            "plugin_path": DictElement(
                parameter_form=String(
                    title=Title("Path of mk_logwatch"),
                    help_text=Help(
                        "Only needed when the wrapper does not find mk_logwatch by "
                        "itself. It searches the plug-in directory of the agent and "
                        "the interval subdirectories below it for "
                        "<tt>mk_logwatch.py</tt> and <tt>mk_logwatch</tt>."
                    ),
                    prefill=InputHint("/usr/lib/check_mk_agent/plugins/mk_logwatch.py"),
                ),
            ),
            "state_dir": DictElement(
                parameter_form=String(
                    title=Title("State directory for the other user"),
                    help_text=Help(
                        "mk_logwatch remembers how far it has read a log file in "
                        "<tt>logwatch.state</tt> below the variable directory of the "
                        "agent. Set a directory of its own here when the configured "
                        "user may not write there. The wrapper creates it on the first "
                        "run with mode 0700 when it may, otherwise create it by hand "
                        "and give it to the user: <tt>mkdir -p &lt;directory&gt; &amp;&amp; "
                        "chown &lt;user&gt; &lt;directory&gt; &amp;&amp; chmod 0700 "
                        "&lt;directory&gt;</tt>."
                    ),
                    prefill=InputHint("/var/lib/check_mk_agent/logwatch_sudo"),
                ),
            ),
            "sudoers": DictElement(
                parameter_form=_sudoers(),
            ),
        },
    )


rule_spec_mk_logwatch_sudo_bakery = AgentConfig(
    name="mk_logwatch_sudo",
    title=Title("Run mk_logwatch as another user (sudo)"),
    topic=Topic.OPERATING_SYSTEM,
    parameter_form=_agent_config_mk_logwatch_sudo,
)
