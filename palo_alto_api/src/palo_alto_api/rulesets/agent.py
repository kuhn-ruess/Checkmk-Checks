#!/usr/bin/env python3
"""
Palo Alto XML API Special Agent Ruleset

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.rulesets.v1 import Help, Label, Title
from cmk.rulesets.v1.form_specs import (
    BooleanChoice,
    DefaultValue,
    DictElement,
    Dictionary,
    Integer,
    MatchingScope,
    MultipleChoice,
    MultipleChoiceElement,
    Password,
    RegularExpression,
    String,
)
from cmk.rulesets.v1.rule_specs import SpecialAgent, Topic


_SECTIONS = [
    ("certificates", "Certificates"),
    ("ipsec", "IPSec tunnels"),
    ("ike", "IKE gateways"),
    ("system", "System info"),
    ("sessions", "Sessions"),
    ("cpu", "CPU"),
    ("environment", "Environment"),
    ("ha", "High availability"),
    ("interfaces", "Interfaces"),
    ("bgp", "BGP peers"),
    ("ospf", "OSPF neighbors"),
    ("licenses", "Licenses"),
]


def _parameter_form():
    return Dictionary(
        title=Title("Palo Alto XML API"),
        help_text=Help(
            "Monitor a Palo Alto Networks firewall through its PAN-OS XML API. "
            "Select below which data should be collected; every selected topic "
            "creates its own services on the host."
        ),
        elements={
            "api_key": DictElement(
                parameter_form=Password(
                    title=Title("API key"),
                    help_text=Help(
                        "PAN-OS XML API key, generated with "
                        "https://<firewall>/api/?type=keygen&user=<user>&password=<password> . "
                        "Certificates and the device certificate require superuser rights."
                    ),
                ),
                required=True,
            ),
            "collect": DictElement(
                parameter_form=MultipleChoice(
                    title=Title("Collect the following data"),
                    help_text=Help(
                        "Only the selected topics are queried. Deselect what you "
                        "do not need to reduce the number of API calls per check."
                    ),
                    elements=[
                        MultipleChoiceElement(name=name, title=Title(title))
                        for name, title in _SECTIONS
                    ],
                    prefill=DefaultValue([name for name, _ in _SECTIONS]),
                ),
                required=True,
            ),
            "address": DictElement(
                parameter_form=String(
                    title=Title("Connection address"),
                    help_text=Help(
                        "Address used to reach the firewall API. Defaults to the "
                        "monitored host's IP address if left empty."
                    ),
                ),
            ),
            "timeout": DictElement(
                parameter_form=Integer(
                    title=Title("Request timeout"),
                    help_text=Help("Timeout for a single API request."),
                    unit_symbol="s",
                    prefill=DefaultValue(30),
                ),
            ),
            "no_verify_ssl": DictElement(
                parameter_form=BooleanChoice(
                    title=Title("Disable SSL verification"),
                    label=Label("Do not verify the firewall's SSL certificate"),
                    help_text=Help(
                        "Firewalls often use a self-signed management certificate."
                    ),
                ),
            ),
            "proxy_url": DictElement(
                parameter_form=String(
                    title=Title("Proxy URL"),
                    help_text=Help("HTTP(S) proxy to use for the API requests."),
                ),
            ),
            "fetch_ciphers": DictElement(
                parameter_form=BooleanChoice(
                    title=Title("Fetch tunnel and gateway ciphers"),
                    label=Label("Fetch the negotiated cipher per IPSec tunnel and IKE gateway"),
                    help_text=Help(
                        "Adds one API call per IPSec tunnel and IKE gateway. Only "
                        "relevant when IPSec or IKE gateways are collected."
                    ),
                    prefill=DefaultValue(True),
                ),
            ),
            "cert_include": DictElement(
                parameter_form=RegularExpression(
                    title=Title("Only monitor certificates matching"),
                    help_text=Help("Limit certificate monitoring to matching names."),
                    predefined_help_text=MatchingScope.INFIX,
                ),
            ),
            "cert_exclude": DictElement(
                parameter_form=RegularExpression(
                    title=Title("Skip certificates matching"),
                    help_text=Help(
                        "Skip certificates whose name matches, e.g. certificates "
                        "already monitored elsewhere on HA pairs."
                    ),
                    predefined_help_text=MatchingScope.INFIX,
                ),
            ),
            "if_include": DictElement(
                parameter_form=RegularExpression(
                    title=Title("Only monitor interfaces matching"),
                    help_text=Help("Limit interface monitoring to matching names."),
                    predefined_help_text=MatchingScope.INFIX,
                ),
            ),
            "if_exclude": DictElement(
                parameter_form=RegularExpression(
                    title=Title("Skip interfaces matching"),
                    help_text=Help(
                        "Skip interfaces whose name matches. Defaults to tunnel, "
                        "vlan and loopback interfaces."
                    ),
                    predefined_help_text=MatchingScope.INFIX,
                    prefill=DefaultValue("^(tunnel|vlan|loopback)"),
                ),
            ),
        },
    )


rule_spec_palo_alto_api = SpecialAgent(
    name="palo_alto_api",
    topic=Topic.NETWORKING,
    parameter_form=_parameter_form,
    title=Title("Palo Alto XML API"),
)
