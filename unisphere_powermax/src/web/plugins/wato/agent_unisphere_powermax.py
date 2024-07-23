#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#pylint: disable=line-too-long

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    TextAscii,
    Password,
    FixedValue,
    Integer,
    TextInput,
    DropdownChoice,
    Float,
    Tuple,
)

from cmk.gui.plugins.wato.utils import (
    HostRulespec,
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersStorage,
    RulespecGroupCheckParametersOperatingSystem,
)


from cmk.gui.plugins.wato.datasource_programs import (
    RulespecGroupDatasourcePrograms,
)


def _valuespec_special_agent_unisphere_powermax():
    return Dictionary(
        elements = [
                  ("username", TextAscii(title=_("Username"),
                                         allow_empty=False,
                                         help=_("Enter the Unisphere API-User."),
                                         )
                   ),
                  ("password", Password(title=_("Password"),
                                        allow_empty=False,
                                         help=_("Enter the Unisphere API-User password."),
                                        )
                   ),
                  ("port", Integer(title=_("Port"),
                                        default_value=8443,
                                        #allow_empty=False,
                                        )
                   ),
                  ("useIP", FixedValue(
                          True,
                          title=_("Use IP Address for SSL connection"),
                          totext=_("using IP Address"),
                          help=_("Check to use IP Address instead of hostname for the SSL connection."),
                              )
                   ),
                  ("disablegetSrpInfo", FixedValue(
                          True,
                          title=_("Disable SRP checks"),
                          totext=_("SRP checks are disabled"),
                          help=_("Check to disable the Storage Resource Pool checks."),
                              )
                   ),
                  ("disablegetDirectorInfo", FixedValue(
                          True,
                          title=_("Disable Director checks"),
                          totext=_("Director checks are disabled"),
                          help=_("Check to disable the Director-Status checks."),
                              )
                   ),
                  ("disablegetHealthScoreInfo", FixedValue(
                          True,
                          title=_("Disable health score checks"),
                          totext=_("Health score checks are disabled"),
                          help=_("Check to disable the Health-Score-Status checks."),
                              )
                   ),
                  ("disablegetHealthCheckInfo", FixedValue(
                          True,
                          title=_("Disable health check checks"),
                          totext=_("Health check checks are disabled"),
                          help=_("Check to disable the Health-Check checks."),
                              )
                   ),
                  ("disablegetArrayPerformanceInfo", FixedValue(
                          True,
                          title=_("Disable array performance checks"),
                          totext=_("Array performance checks are disabled"),
                          help=_("Check to disable the Array-Performance checks."),
                              )
                   ),
                  ("disablegetPortGroupInfo", FixedValue(
                          True,
                          title=_("Disable port group checks"),
                          totext=_("Port group checks are disabled"),
                          help=_("Check to disable the Port-Group checks."),
                              )
                   ),
                  ("disablegetAlertInfo", FixedValue(
                          True,
                          title=_("Disable alert summary checks"),
                          totext=_("Alert summary checks are disabled"),
                          help=_("Check to disable the Alert-Summary checks."),
                              )
                   ),
                  ("disablegetMaskingViewInfo", FixedValue(
                          True,
                          title=_("Disable masking view checks"),
                          totext=_("Masking view checks are disabled"),
                          help=_("Check to disable the Masking-View Storage- and Volume-Summary checks."),
                              )
                   ),
                  ("enableRemoteSymChecks", FixedValue(
                          True,
                          title=_("Enable remote Symmetrix checks"),
                          totext=_("Remote Symmetrix checks are enabled"),
                          help=_("In order to avoid many duplicated check-instances, only the local Symmetrix is considered in the data gathering process."
                                 "You can override this behaviour by enabling this feature."),
                              )
                   ),
                  ("cache-time", Integer(title=_("Cache long running queries"),
                                        default_value=30,
                                        #allow_empty=True,
                                        help=_("To avoid stale checks and high load on the Unisphere API, long running queries can be cached."
                                               "The default cache time is 30 minutes. To disable the cache, enter a cach time smaler than the check interval."),
                                        )
                   ),
                  ("no_cert_check", FixedValue(
                          True,
                          title=_("Disable SSL certificate validation"),
                          totext=_("SSL certificate validation is disabled"),
                              )
                   )
        ],
        optional_keys=['no_cert_check', 'disablegetSrpInfo', 'disablegetDirectorInfo', 'disablegetHealthScoreInfo', 'disablegetHealthCheckInfo', 'disablegetArrayPerformanceInfo', 'disablegetPortGroupInfo', 'disablegetAlertInfo', 'disablegetMaskingViewInfo', 'cache-time', 'enableRemoteSymChecks', 'useIP'],
        title=_("Unisphere Powermax Special Agent"),
        help=_("This rule selects the Unisphere Powermax agent instead of the " "Check_MK Agent."
               "You can configure your connection settings here."),
        )

rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupDatasourcePrograms,
        name="special_agents:unisphere_powermax",
        valuespec=_valuespec_special_agent_unisphere_powermax,
    )
)

def _parameter_valuespec_unisphere_powermax_srp_effective_used():
    return Dictionary(
        elements = [
            ( 'levels', Tuple(
                title = _("PowerMax SRP effective usage levels"),
                elements = [
                    Integer(title = _("warning level"), unit = "%", default_value = 80 ),
                    Integer(title = _("critical level"), unit = "%",  default_value = 90 ),
                ]
            )),
        ],
    )
def _item_valuespec_unisphere_powermax_srp_effective_used():
    return TextInput(title="fitting item name", help="inline help text")

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="unisphere_powermax_srp_effective_used",
        group=RulespecGroupCheckParametersStorage,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_unisphere_powermax_srp_effective_used,
        item_spec=_item_valuespec_unisphere_powermax_srp_effective_used,
        title=lambda: _("PowerMax SRP effective usage"),
    ))



def _parameter_valuespec_unisphere_powermax_srp_physical_used():
    return Dictionary(
        elements = [
            ( 'levels', Tuple(
                title = _("PowerMax SRP physical usage levels"),
                elements = [
                    Integer(title = _("warning level"), unit = "%", default_value = 80 ),
                    Integer(title = _("critical level"), unit = "%",  default_value = 90 ),
                ]
            )),
        ],
    )
def _item_valuespec_unisphere_powermax_srp_physical_used():
    return TextInput(title="fitting item name", help="inline help text")

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="unisphere_powermax_srp_physical_used",
        group=RulespecGroupCheckParametersStorage,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_unisphere_powermax_srp_physical_used,
        item_spec=_item_valuespec_unisphere_powermax_srp_physical_used,
        title=lambda: _("PowerMax SRP physical usage"),
    ))

def _parameter_valuespec_unisphere_powermax_srp_data_reduction_ratio():
    return Dictionary(
        elements = [
            ( 'levels', Tuple(
                title = _("PowerMax Data Reduction Ratio levels"),
                elements = [
                    Float(title = _("warning level"), default_value = 3.0 ),
                    Float(title = _("critical level"), default_value = 2.0 ),
                ]
            )),
        ],
    )
def _item_valuespec_unisphere_powermax_srp_data_reduction_ratio():
    return TextInput(title="fitting item name", help="inline help text")

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="unisphere_powermax_srp_data_reduction_ratio",
        group=RulespecGroupCheckParametersStorage,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_unisphere_powermax_srp_data_reduction_ratio,
        item_spec=_item_valuespec_unisphere_powermax_srp_data_reduction_ratio,
        title=lambda: _("PowerMax SRP Data Reduction Ratio"),
    ))

def _parameter_valuespec_unisphere_powermax_powermax_array_performance_wp_cache():
    return Dictionary(
        elements = [
            ( 'average_levels', Tuple(
                title = _("Average WP Cache usage levels"),
                elements = [
                    Float(title = _("warning level"), unit = "%", default_value = 80.0 ),
                    Float(title = _("critical level"), unit = "%",  default_value = 90.0 ),
                ]
            )),
            ( 'maximum_levels', Tuple(
                title = _("Maximum WP Cache usage levels"),
                elements = [
                    Float(title = _("warning level"), unit = "%", default_value = 80.0 ),
                    Float(title = _("critical level"), unit = "%",  default_value = 90.0 ),
                ]
            )),
        ],
    )
def _item_valuespec_unisphere_powermax_powermax_array_performance_wp_cache():
    return TextInput(title="fitting item name", help="inline help text")

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="unisphere_powermax_powermax_array_performance_wp_cache",
        group=RulespecGroupCheckParametersStorage,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_unisphere_powermax_powermax_array_performance_wp_cache,
        item_spec=_item_valuespec_unisphere_powermax_powermax_array_performance_wp_cache,
        title=lambda: _("PowerMax WP Cache usage"),
    ))

def _parameter_valuespec_unisphere_powermax_health_check():
    return Dictionary(
        elements = [
            ( "criticality",
                 DropdownChoice(
                     title = _("Powermax Health Check criticality"),
                     help = _('default is crit'),
                     choices = [
                           ( 'crit',  _("a negaitve health check, results in critical state") ),
                           ( 'warn',  _("a negaitve health check, results in warning state") ),
                     ],
                     default_value = "crit",
                 )
            ),
            ( "max_age", Integer(
                title=_("maximum health check age in hours"),
                help = _('default is 168 hours = 1 week'),
                )
            ),
        ],
    )
def _item_valuespec_unisphere_powermax_health_check():
    return TextInput(title="fitting item name", help="inline help text")

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="unisphere_powermax_health_check",
        group=RulespecGroupCheckParametersStorage,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_unisphere_powermax_health_check,
        item_spec=_item_valuespec_unisphere_powermax_health_check,
        title=lambda: _("PowerMax Health Check"),
    ))

def _parameter_valuespec_unisphere_powermax_health_score():
    return Dictionary(
        elements = [
            ( 'levels', Tuple(
                title = _("PowerMax Health Score levels"),
                elements = [
                    Float(title = _("warning level"), default_value = 90.0 ),
                    Float(title = _("critical level"), default_value = 80.0 ),
                ]
            )),
        ],
    )
def _item_valuespec_unisphere_powermax_health_score():
    return TextInput(title="fitting item name", help="inline help text")

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="unisphere_powermax_health_score",
        group=RulespecGroupCheckParametersStorage,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_unisphere_powermax_health_score,
        item_spec=_item_valuespec_unisphere_powermax_health_score,
        title=lambda: _("PowerMax Health Score"),
    ))

def _parameter_valuespec_unisphere_powermax_masking_view_port_summary():
    return Dictionary(
        elements = [
            ( 'levels', Tuple(
                title = _("PowerMax Masking View Port Sumary levels"),
                elements = [
                    Float(title = _("warning level"), default_value = 100.0 ),
                    Float(title = _("critical level"), default_value = 50.0 ),
                ]
            )),
        ],
    )
def _item_valuespec_unisphere_powermax_masking_view_port_summary():
    return TextInput(title="fitting item name", help="inline help text")

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="unisphere_powermax_masking_view_port_summary",
        group=RulespecGroupCheckParametersStorage,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_unisphere_powermax_masking_view_port_summary,
        item_spec=_item_valuespec_unisphere_powermax_masking_view_port_summary,
        title=lambda: _("PowerMax Masking View Port Summary"),
    ))

def _parameter_valuespec_unisphere_powermax_masking_view_volume_summary():
    return Dictionary(
        elements = [
            ( 'levels', Tuple(
                title = _("PowerMax Masking View Volume Sumary levels"),
                elements = [
                    Float(title = _("warning level"), default_value = 100.0 ),
                    Float(title = _("critical level"), default_value = 50.0 ),
                ]
            )),
        ],
    )
def _item_valuespec_unisphere_powermax_masking_view_volume_summary():
    return TextInput(title="fitting item name", help="inline help text")

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="unisphere_powermax_masking_view_volume_summary",
        group=RulespecGroupCheckParametersStorage,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_unisphere_powermax_masking_view_volume_summary,
        item_spec=_item_valuespec_unisphere_powermax_masking_view_volume_summary,
        title=lambda: _("PowerMax Masking View Volume Summary"),
    ))

def _parameter_valuespec_unisphere_port_group_state():
    return Dictionary(
        elements = [
            ( 'levels', Tuple(
                title = _("PowerMax Port Group state levels"),
                elements = [
                    Float(title = _("warning level"), default_value = 100.0 ),
                    Float(title = _("critical level"), default_value = 50.0 ),
                ]
            )),
        ],
    )
def _item_valuespec_unisphere_port_group_state():
    return TextInput(title="fitting item name", help="inline help text")

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="unisphere_powermax_port_group_state",
        group=RulespecGroupCheckParametersStorage,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_unisphere_port_group_state,
        item_spec=_item_valuespec_unisphere_port_group_state,
        title=lambda: _("PowerMax Port Group state"),
    ))
