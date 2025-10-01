#!/usr/bin/env python3

from cmk.rulesets.v1 import Title, Help, Label
from cmk.rulesets.v1.form_specs import (
    Dictionary,
    DictElement,
    String,
    Integer,
    SimpleLevels,
    Password,
    LevelDirection,
    InputHint,
    BooleanChoice,
    Percentage,
    Float,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange

from cmk.rulesets.v1.rule_specs import (
        SpecialAgent,
        Topic,
        CheckParameters,
        HostAndItemCondition,
)


def _migrate(value):
    """
    Migration function to convert old ruleset values to the new format.
    """
    # Legacy parameter migrations
    if 'cache-time' in value:
        value['cache_time'] = value.pop('cache-time')
    if 'useIP' in value:
        value['use_ip'] = value.pop('useIP')
    
    # CamelCase to snake_case parameter migrations
    camel_to_snake_mappings = {
        'disablegetSrpInfo': 'disable_get_srp_info',
        'disablegetDirectorInfo': 'disable_get_director_info',
        'disablegetHealthScoreInfo': 'disable_get_health_score_info',
        'disablegetHealthCheckInfo': 'disable_get_health_check_info',
        'disablegetArrayPerformanceInfo': 'disable_get_array_performance_info',
        'disablegetPortGroupInfo': 'disable_get_port_group_info',
        'disablegetAlertInfo': 'disable_get_alert_info',
        'disablegetMaskingViewInfo': 'disable_get_masking_view_info',
        "enableRemoteSymChecks": 'enable_remote_sym_checks'
    }
    
    for old_key, new_key in camel_to_snake_mappings.items():
        if old_key in value:
            value[new_key] = value.pop(old_key)
    
    return value

def _valuespec_special_agent_unisphere_powermax():
    return Dictionary(
            title = Title("Unisphere Powermax"),
            help_text = Help("This rules activates the special agent for Unisphere Powermax"),
            migrate=_migrate,
            elements = {
                "username": DictElement(
                    parameter_form = String(
                        title = Title("Username"),
                        help_text = Help("Enter the Unisphere API-User."),
                        custom_validate=(LengthInRange(min_value=1),),
                    ),
                    required = True,
                ),
                "password": DictElement(
                    parameter_form = Password(
                        title = Title("Password"),
                        help_text = Help("Enter the Unisphere API-User password."),
                    ),
                    required = True,
                ),
                "port": DictElement(
                    parameter_form = Integer(
                        title = Title("Port"),
                        prefill = InputHint(8443),
                    ),
                ),
                "api_version": DictElement(
                    parameter_form = Integer(
                        title = Title("API Version"),
                        prefill = InputHint(100),
                    ),
                ),
                "use_ip": DictElement(
                    parameter_form = BooleanChoice(
                        title = Title("Use IP Address for SSL connection"),
                        label = Label("use IP"),
                        help_text = Help("Check to use IP Address instead of "\
                                         "hostname for the SSL connection."),
                    ),
                ),
                "disable_get_srp_info": DictElement(
                    parameter_form = BooleanChoice(
                        title = Title("Disable SRP checks"),
                        label = Label("disable"),
                        help_text = Help("Check to disable the SRP-Info checks."),
                    ),
                ),
                "disable_get_director_info": DictElement(
                    parameter_form = BooleanChoice(
                        title = Title("Disable Director checks"),
                        label = Label("disable"),
                        help_text = Help("Check to disable the Director-Status checks."),
                    ),
                ),
                "disable_get_health_score_info": DictElement(
                    parameter_form = BooleanChoice(
                        title = Title("Disable health score checks"),
                        label = Label("disable"),
                        help_text = Help("Check to disable the Health-Score-Status checks."),
                    ),
                ),
                "disable_get_health_check_info": DictElement(
                    parameter_form = BooleanChoice(
                        title = Title("Disable health check checks"),
                        label = Label("disable"),
                        help_text = Help("Check to disable the Health-Check checks."),
                    ),
                ),
                "disable_get_array_performance_info": DictElement(
                    parameter_form = BooleanChoice(
                        title = Title("Disable array performance checks"),
                        label = Label("disable"),
                        help_text = Help("Check to disable the Array-Performance checks."),
                    ),
                ),
                "disable_get_port_group_info": DictElement(
                    parameter_form = BooleanChoice(
                        title = Title("Disable port group checks"),
                        label = Label("disable"),
                        help_text = Help("Check to disable the Port-Group checks."),
                    ),
                ),
                "disable_get_alert_info": DictElement(
                    parameter_form = BooleanChoice(
                        title = Title("Disable alert summary checks"),
                        label = Label("disable"),
                        help_text = Help("Check to disable the Alert-Summary checks."),
                    ),
                ),
                "disable_get_masking_view_info": DictElement(
                    parameter_form = BooleanChoice(
                        title = Title("Disable masking view checks"),
                        label = Label("disable"),
                        help_text = Help("Check to disable the Masking-View"\
                                         "Storage- and Volume-Summary checks."),
                    ),
                ),
                "enable_remote_sym_checks": DictElement(
                    parameter_form = BooleanChoice(
                        title = Title("Enable remote Symmetrix checks"),
                        label = Label("enable"),
                        help_text = Help("In order to avoid many duplicated check-instances,"\
                                         "only the local Symmetrix is considered in the data"\
                                         "gathering process. You can override this behaviour by"\
                                         "enabling this feature."),
                    ),
                ),
                "cache_time": DictElement(
                    parameter_form = Integer(
                        title = Title("Cache long running queries"),
                        help_text = Help("To avoid stale checks and high load on the "\
                                         "Unisphere API, long running queries can be cached. "\
                                         "The default cache time is 30 minutes. To disable "\
                                         "the cache, enter a cach time smaler than "\
                                         "the check interval."),
                        prefill = InputHint(30)
                    ),
                ),
                "no_cert_check": DictElement(
                    parameter_form = BooleanChoice(
                        title = Title("Disable SSL certificate validation"),
                        label = Label("disable SSL"),
                        help_text = Help("SSL certificate validation is disabled"),
                    ),
                ),

            }
        )

rule_spec_semu_agent = SpecialAgent(
    name = "unisphere_powermax",
    topic = Topic.STORAGE,
    parameter_form = _valuespec_special_agent_unisphere_powermax,
    title = Title("Unisphere Powermax"),
)



def _parameter_valuespec_unisphere_powermax_srp_effective_used():
    return Dictionary(
        elements={
            "levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("PowerMax SRP effective usage levels"),
                    form_spec_template=Percentage(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=InputHint(value=(80, 90))
                )
            )
        }
    )

rule_spec_srp_effective_used = CheckParameters(
        name="unisphere_powermax_srp_effective_used",
        topic=Topic.STORAGE,
        parameter_form = _parameter_valuespec_unisphere_powermax_srp_effective_used,
        condition=HostAndItemCondition(
            item_title=Title("fitting item name"),
        ),
        title=Title("PowerMax SRP Effective usage")
)


def _parameter_valuespec_unisphere_powermax_srp_physical_used():
    return Dictionary(
        elements = {
            "levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("PowerMax SRP physical usage levels"),
                    form_spec_template=Percentage(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=InputHint(value=(80, 90))
                )
            ),
        },
    )

rule_spec_srp_physical_used = CheckParameters(
        name="unisphere_powermax_srp_physical_used",
        topic=Topic.STORAGE,
        parameter_form = _parameter_valuespec_unisphere_powermax_srp_physical_used,
        condition=HostAndItemCondition(
            item_title=Title("fitting item name"),
        ),
        title=Title("PowerMax SRP physical usage")
)


def _parameter_valuespec_unisphere_powermax_srp_data_reduction_ratio():
    return Dictionary(
        elements = {
            "levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("PowerMax Data Reduction Ratio levels"),
                    form_spec_template=Float(),
                    level_direction=LevelDirection.LOWER,
                    prefill_fixed_levels=InputHint(value=(3.0, 2.0))
                )
            ),
        },
    )

rule_spec_srp_data_reduction_ratio = CheckParameters(
        name="unisphere_powermax_srp_data_reduction_ratio",
        topic=Topic.STORAGE,
        parameter_form = _parameter_valuespec_unisphere_powermax_srp_data_reduction_ratio,
        condition=HostAndItemCondition(
            item_title=Title("fitting item name"),
        ),
        title=Title("PowerMax SRP Data Reduction Ratio")
)

def _parameter_valuespec_unisphere_powermax_powermax_array_performance_wp_cache():
    return Dictionary(
        elements = {
            "average_levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Average WP Cache usage levels"),
                    form_spec_template=Percentage(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=InputHint(value=(80, 90))
                )
            ),
            "maximum_levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Maximum WP Cache usage levels"),
                    form_spec_template=Percentage(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=InputHint(value=(80, 90))
                )
            ),
        },
    )

rule_spec_powermax_array_performnace_wp_cache = CheckParameters(
        name="unisphere_powermax_powermax_array_performance_wp_cache",
        topic=Topic.STORAGE,
        parameter_form = _parameter_valuespec_unisphere_powermax_powermax_array_performance_wp_cache,
        condition=HostAndItemCondition(
            item_title=Title("fitting item name"),
        ),
        title=Title("PowerMax WP Cache usage")
)


#def _parameter_valuespec_unisphere_powermax_health_check():
#    return Dictionary(
#        elements = [
#            ( "criticality",
#                 DropdownChoice(
#                     title = _("Powermax Health Check criticality"),
#                     help = _('default is crit'),
#                     choices = [
#                           ( 'crit',  _("a negaitve health check, results in critical state") ),
#                           ( 'warn',  _("a negaitve health check, results in warning state") ),
#                     ],
#                     default_value = "crit",
#                 )
#            ),
#            ( "max_age", Integer(
#                title=_("maximum health check age in hours"),
#                help = _('default is 168 hours = 1 week'),
#                )
#            ),
#        ],
#    )

#def _item_valuespec_unisphere_powermax_health_check():
#    return TextInput(title="fitting item name", help="inline help text")
#
#rulespec_registry.register(
#    CheckParameterRulespecWithItem(
#        check_group_name="unisphere_powermax_health_check",
#        group=RulespecGroupCheckParametersStorage,
#        match_type="dict",
#        parameter_valuespec=_parameter_valuespec_unisphere_powermax_health_check,
#        item_spec=_item_valuespec_unisphere_powermax_health_check,
#        title=lambda: _("PowerMax Health Check"),
#    ))
#



def _parameter_valuespec_unisphere_powermax_health_score():
    return Dictionary(
        elements = {
            "levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("PowerMax Health Score levels"),
                    form_spec_template=Percentage(),
                    level_direction=LevelDirection.LOWER,
                    prefill_fixed_levels=InputHint(value=(90, 80))
                )
            ),
        },
    )

rule_spec_unisphere_powermax_health_score = CheckParameters(
        name="unisphere_powermax_health_score",
        topic=Topic.STORAGE,
        parameter_form = _parameter_valuespec_unisphere_powermax_health_score,
        condition=HostAndItemCondition(
            item_title=Title("fitting item name"),
        ),
        title=Title("PowerMax Health Score")
)




def _parameter_valuespec_unisphere_powermax_masking_view_port_summary():
    return Dictionary(
        elements = {
            "levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("PowerMax Masking View Port Summary levels"),
                    form_spec_template=Percentage(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=InputHint(value=(100, 50))
                )
            ),
        },
    )

rule_spec_unisphere_powermax_masking_view_port_summary = CheckParameters(
        name="unisphere_powermax_masking_view_port_summary",
        topic=Topic.STORAGE,
        parameter_form = _parameter_valuespec_unisphere_powermax_masking_view_port_summary,
        condition=HostAndItemCondition(
            item_title=Title("fitting item name"),
        ),
        title=Title("PowerMax Masking View Port Summary")
)



def _parameter_valuespec_unisphere_powermax_masking_view_volume_summary():
    return Dictionary(
        elements = {
            "levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("PowerMax Masking View Volume Sumary levels"),
                    form_spec_template=Percentage(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=InputHint(value=(100, 50))
                )
            ),
        },
    )

rule_spec_unisphere_powermax_masking_view_volume_summary = CheckParameters(
        name="unisphere_powermax_masking_view_volume_summary",
        topic=Topic.STORAGE,
        parameter_form = _parameter_valuespec_unisphere_powermax_masking_view_volume_summary,
        condition=HostAndItemCondition(
            item_title=Title("fitting item name"),
        ),
        title=Title("PowerMax Masking View Volume Summary")
)



def _parameter_valuespec_unisphere_powermax_port_group_state():
    return Dictionary(
        elements = {
            "levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("PowerMax Port Group state levels"),
                    form_spec_template=Percentage(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=InputHint(value=(100, 50))
                )
            ),
        },
    )

rule_spec_unisphere_powermax_port_group_state = CheckParameters(
        name="unisphere_powermax_port_group_state",
        topic=Topic.STORAGE,
        parameter_form = _parameter_valuespec_unisphere_powermax_port_group_state,
        condition=HostAndItemCondition(
            item_title=Title("fitting item name"),
        ),
        title=Title("PowerMax Port Group state")
)
