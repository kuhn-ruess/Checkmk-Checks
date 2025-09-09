#!/usr/bin/env python3
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

# Migration auf Checkmk 2.4 API
from cmk.rulesets.v1 import Title, Help
from cmk.rulesets.v1.form_specs import (
   Dictionary,
   DictElement,
   Float,
   Integer,
   String,
   InputHint,
   SimpleLevels,
   LevelDirection,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic

def _parameter_galera_repl_health() -> Dictionary:
   return Dictionary(
      help_text=Help("Monitor the Cluster Replication Health"),
      elements={
         "wsrep_local_recv_queue_avg": DictElement(
            parameter_form=SimpleLevels(
               title=Title("Recv queue length average"),
               help_text=Help("Recv queue length averaged over interval since the last FLUSH STATUS command. Values considerably larger than 0.0 mean that the node cannot apply write-sets as fast as they are received and will generate a lot of replication throttling."),
               level_direction=LevelDirection.UPPER,
               prefill_fixed_levels=InputHint(value=(0.5, 1.0)),
               form_spec_template=Float(),
            ),
            required=True,
         ),
         "wsrep_local_send_queue_avg": DictElement(
            parameter_form=SimpleLevels(
               title=Title("Send queue length average"),
               help_text=Help("Send queue length averaged over time since the last FLUSH STATUS command. Values considerably larger than 0.0 indicate replication throttling or network throughput issue."),
               level_direction=LevelDirection.UPPER,
               prefill_fixed_levels=InputHint(value=(0.5, 1.0)),
               form_spec_template=Float(),
            ),
            required=True,
         ),
         "wsrep_flow_control_paused": DictElement(
            parameter_form=SimpleLevels(
               title=Title("Flow control paused"),
               help_text=Help("The fraction of time since the last FLUSH STATUS command that replication was paused due to flow control. In other words, how much the slave lag is slowing down the cluster"),
               level_direction=LevelDirection.UPPER,
               prefill_fixed_levels=InputHint(value=(0.5, 0.7)),
               form_spec_template=Float(),
            ),
            required=True,
         ),
      },
   )

rule_spec_galera_repl_health = CheckParameters(
   name="galera_repl_health",
   topic=Topic.APPLICATIONS,
   condition=HostCondition(),
   parameter_form=_parameter_galera_repl_health,
   title=Title("MySQL Galera Replication Health"),
)

def _parameter_galera_node_state() -> Dictionary:
   return Dictionary(
      help_text=Help("Monitor the Cluster Node state"),
      elements={
         "wsrep_local_state_comment": DictElement(
            parameter_form=String(
               title=Title("wsrep_local_state_comment"),
               help_text=Help("Shows the node state in a human readable format. When the node is part of the Primary Component, the typical return values are Joining, Waiting on SST, Joined, Synced or Donor. In the event that the node is part of a nonoperational component, the return value is Initialized. Normaly you want to keep 'Initialized' (the relevant value to alert on)."),
               prefill=InputHint("Initialized"),
            ),
            required=True,
         ),
         "wsrep_ready": DictElement(
            parameter_form=String(
               title=Title("wsrep_ready"),
               help_text=Help("Shows whether the node can accept queries. When the node returns a value of ON it can accept write-sets from the cluster. When it returns the value OFF, almost all queries fail with the error: 'ERROR 1047 (08501) Unknown Command'. Normally you want to keep ON, the default."),
               prefill=InputHint("On"),
            ),
            required=True,
         ),
         "wsrep_connected": DictElement(
            parameter_form=String(
               title=Title("wsrep_connected"),
               help_text=Help("Shows whether the node has network connectivity with any other nodes. When the value is ON, the node has a network connection to one or more other nodes forming a cluster component. When the value is OFF, the node does not have a connection to any cluster components. Normally you want to keep ON, the default."),
               prefill=InputHint("On"),
            ),
            required=True,
         ),
      },
   )

rule_spec_galera_node_state = CheckParameters(
   name="galera_node_state",
   topic=Topic.APPLICATIONS,
   condition=HostCondition(),
   parameter_form=_parameter_galera_node_state,
   title=Title("MySQL Galera Node State"),
)

def _parameter_galera_cluster_state() -> Dictionary:
   return Dictionary(
      help_text=Help("This check monitors the current state of the Cluster"),
      elements={
         "wsrep_cluster_size": DictElement(
            parameter_form=SimpleLevels(
               title=Title("Number of Members of the Cluster"),
               help_text=Help("Monitor the number of members in the cluster."),
               level_direction=LevelDirection.LOWER,
               prefill_fixed_levels=InputHint(value=(4, 3)),
               form_spec_template=Integer(),
            ),
            required=True,
         ),
         "wsrep_cluster_status": DictElement(
            parameter_form=String(
               title=Title("Expected Cluster Status"),
               prefill=InputHint("Primary"),
               help_text=Help("Cluster Node component status. Possible values are 'Primary' (primary group configuration, quorum present), 'Non_primary' (non-primary group configuration, quorum lost) or 'Disconnected' (not connected to group, retrying). Normally you want keep PRIMARY (the default)."),
            ),
            required=True,
         ),
      },
   )

rule_spec_galera_cluster_state = CheckParameters(
   name="galera_cluster_state",
   topic=Topic.APPLICATIONS,
   condition=HostCondition(),
   parameter_form=_parameter_galera_cluster_state,
   title=Title("MySQL Galera Cluster State"),
)
