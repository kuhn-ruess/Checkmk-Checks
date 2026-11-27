#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
import json

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Service,
    State,
    Result,
    check_levels,
    render,
)


def short_id(resource_id):
    """
    Return the last path segment (the resource name) of an Azure resource ID.
    """
    if not resource_id or not isinstance(resource_id, str):
        return None
    return resource_id.rstrip('/').split('/')[-1]


def render_details(pairs):
    """
    Render a list of (label, value) pairs as readable multi-line details.
    Empty values are skipped so we never show noise or dump raw JSON.
    """
    lines = []
    for label, value in pairs:
        if value in (None, '', {}, [], 'None', 'Unknown'):
            continue
        lines.append(f"{label}: {value}")
    return "\n".join(lines)


def parse_properties(string_table):
    """
    Parse Azure Firewalls Properties Data
    """
    if not string_table:
        return {'firewalls': {}, 'ip_configs': {}, 'rule_collections': {}, 'policies': {}}
    result = {'firewalls': {}, 'ip_configs': {}, 'rule_collections': {}, 'policies': {}}

    for line in string_table:
        if not line:
            continue
        try:
            raw_data = json.loads(line[0])
        except (json.JSONDecodeError, IndexError):
            continue

        if not isinstance(raw_data, dict):
            continue

        firewall_name = raw_data.get('_resource_name', 'unknown-firewall')

        result['firewalls'][firewall_name] = {
            'name': firewall_name,
            'provisioningState': raw_data.get('provisioningState'),
            'sku': raw_data.get('sku', {}),
            'threatIntelMode': raw_data.get('threatIntelMode'),
            'additionalProperties': raw_data.get('additionalProperties', {}),
            'firewallPolicy': raw_data.get('firewallPolicy', {}),
            'resource_group': raw_data.get('_resource_group'),
            'resource_id': raw_data.get('_resource_id'),
        }

        # Data-plane IP configurations (list) plus the management IP
        # configuration (single object, used for forced tunneling). The
        # management config was previously not parsed, so its service showed
        # "No data" even though Azure returns it.
        ip_configs = [(ipc, 'data') for ipc in raw_data.get('ipConfigurations', [])]
        mgmt_ip_config = raw_data.get('managementIpConfiguration')
        if isinstance(mgmt_ip_config, dict) and mgmt_ip_config.get('name'):
            ip_configs.append((mgmt_ip_config, 'management'))

        for ip_config, ip_kind in ip_configs:
            ip_config_name = ip_config.get('name', 'unknown')
            ip_props = ip_config.get('properties', {})
            full_name = f"{firewall_name}_{ip_config_name}"
            result['ip_configs'][full_name] = {
                'name': ip_config_name,
                'firewall_name': firewall_name,
                'kind': ip_kind,
                'provisioningState': ip_props.get('provisioningState'),
                'privateIPAddress': ip_props.get('privateIPAddress'),
                'privateIPAllocationMethod': ip_props.get('privateIPAllocationMethod'),
                'publicIPAddress': ip_props.get('publicIPAddress', {}),
                'subnet': ip_props.get('subnet', {}),
            }

        rule_collections = []
        rule_collections.extend([(rc, 'network') for rc in raw_data.get('networkRuleCollections', [])])
        rule_collections.extend([(rc, 'application') for rc in raw_data.get('applicationRuleCollections', [])])
        rule_collections.extend([(rc, 'nat') for rc in raw_data.get('natRuleCollections', [])])

        for rule_collection, rule_type in rule_collections:
            rc_name = rule_collection.get('name', 'unknown')
            full_name = f"{firewall_name}_{rc_name}"
            result['rule_collections'][full_name] = {
                'name': rc_name,
                'firewall_name': firewall_name,
                'type': rule_type,
                'priority': rule_collection.get('properties', {}).get('priority'),
                'action': rule_collection.get('properties', {}).get('action', {}),
                'provisioningState': rule_collection.get('properties', {}).get('provisioningState'),
                'rules': rule_collection.get('properties', {}).get('rules', []),
            }

        policy = raw_data.get('firewallPolicy', {})
        if policy.get('id'):
            policy_name = policy.get('id', '').split('/')[-1] if policy.get('id') else 'unknown-policy'
            full_name = f"{firewall_name}_{policy_name}"
            result['policies'][full_name] = {
                'name': policy_name,
                'firewall_name': firewall_name,
                'policy_id': policy.get('id'),
            }

    return result


# Discovery functions for each resource type
def discover_firewalls(section):
    """
    Discover Azure Firewalls
    """
    firewalls = section.get('firewalls', {})
    for name in firewalls:
        yield Service(item=name)


def ip_addresses(data):
    """
    Return the private IP, public IP address and public IP resource of an IP configuration.
    """
    public_ip = data.get('publicIPAddress', {})
    return {
        'private_ip': data.get('privateIPAddress'),
        'public_ip': public_ip.get('ipAddress'),
        'public_ip_resource': short_id(public_ip.get('id')),
    }


def discover_ip_configs(section):
    """
    Discover Azure Firewall IP Configurations and remember their addresses
    """
    ip_configs = section.get('ip_configs', {})
    for name, data in ip_configs.items():
        discovered = {key: value for key, value in ip_addresses(data).items() if value}
        yield Service(item=name, parameters={'discovered_addresses': discovered})


def discover_rule_collections(section):
    """
    Discover Azure Firewall Rule Collections
    """
    rule_collections = section.get('rule_collections', {})
    for name in rule_collections:
        yield Service(item=name)


def discover_policies(section):
    """
    Discover Azure Firewall Policies
    """
    policies = section.get('policies', {})
    for name in policies:
        yield Service(item=name)


# Check functions for each resource type
def check_firewall(item, section):
    """
    Check Azure Firewall Main Properties
    """
    firewalls = section.get('firewalls', {})
    data = firewalls.get(item)
    if not data:
        yield Result(state=State.UNKNOWN, summary=f"No data for Firewall {item}")
        return

    # Check provisioning state
    provisioning_state = data.get('provisioningState', 'Unknown')
    if provisioning_state == 'Succeeded':
        state = State.OK
    elif provisioning_state in ['Failed', 'Canceled']:
        state = State.CRIT
    else:
        state = State.WARN
    
    # Get main properties
    sku = data.get('sku', {})
    sku_name = sku.get('name', 'Unknown')
    sku_tier = sku.get('tier', 'Unknown')
    threat_intel_mode = data.get('threatIntelMode', 'Unknown')
    policy_name = short_id(data.get('firewallPolicy', {}).get('id'))

    summary_parts = [
        f"State: {provisioning_state}",
        f"SKU: {sku_name} ({sku_tier})",
        f"Threat Intel: {threat_intel_mode}",
        f"Policy: {'Configured' if policy_name else 'Not configured'}",
    ]

    details = render_details([
        ("Provisioning State", provisioning_state),
        ("SKU", f"{sku_name} ({sku_tier})"),
        ("Threat Intel Mode", threat_intel_mode),
        ("Firewall Policy", policy_name or 'Not configured'),
        ("Resource Group", data.get('resource_group')),
    ])

    yield Result(
        state=state,
        summary="; ".join(summary_parts),
        details=details,
    )


def check_ip_config(item, params, section):
    """
    Check Azure Firewall IP Configuration
    """
    ip_configs = section.get('ip_configs', {})
    data = ip_configs.get(item)
    if not data:
        yield Result(state=State.UNKNOWN, summary=f"No data for IP Config {item}")
        return

    # Check provisioning state
    provisioning_state = data.get('provisioningState', 'Unknown')
    if provisioning_state == 'Succeeded':
        state = State.OK
    elif provisioning_state in ['Failed', 'Canceled']:
        state = State.CRIT
    else:
        state = State.WARN
    
    kind = data.get('kind', 'data')
    config_type = 'Management' if kind == 'management' else 'Data plane'
    addresses = ip_addresses(data)
    private_ip = addresses['private_ip']
    allocation_method = data.get('privateIPAllocationMethod')
    public_ip = addresses['public_ip']
    public_ip_resource = addresses['public_ip_resource']
    subnet = short_id(data.get('subnet', {}).get('id'))

    public_ip_text = public_ip or public_ip_resource or 'None'
    if public_ip and public_ip_resource:
        public_ip_text = f"{public_ip} ({public_ip_resource})"

    summary_parts = [f"State: {provisioning_state}", f"Type: {config_type}"]
    if private_ip:
        summary_parts.append(f"Private IP: {private_ip}")
    summary_parts.append(f"Public IP: {public_ip_text}")

    private_ip_text = None
    if private_ip:
        private_ip_text = f"{private_ip} ({allocation_method})" if allocation_method else private_ip

    details = render_details([
        ("Provisioning State", provisioning_state),
        ("Configuration Type", config_type),
        ("Private IP", private_ip_text),
        ("Public IP", public_ip),
        ("Public IP Resource", public_ip_resource),
        ("Subnet", subnet),
    ])

    yield Result(
        state=state,
        summary="; ".join(summary_parts),
        details=details,
    )

    discovered = params.get('discovered_addresses')
    if discovered is None:
        yield Result(
            state=State.OK,
            notice="No addresses stored at discovery, rediscover the service to enable change detection",
        )
        return

    labels = {
        'private_ip': "Private IP",
        'public_ip': "Public IP",
        'public_ip_resource': "Public IP resource",
    }
    change_state = State(params.get('state_changed', State.CRIT.value))
    for key, label in labels.items():
        expected = discovered.get(key)
        current = addresses[key]
        if expected and current != expected:
            yield Result(
                state=change_state,
                summary=f"{label} changed from {expected} to {current or 'None'} "
                        "(rediscover the service to accept)",
            )


def check_rule_collection(item, section):
    """
    Check Azure Firewall Rule Collection
    """
    rule_collections = section.get('rule_collections', {})
    data = rule_collections.get(item)
    if not data:
        yield Result(state=State.UNKNOWN, summary=f"No data for Rule Collection {item}")
        return

    # Check provisioning state
    provisioning_state = data.get('provisioningState', 'Unknown')
    if provisioning_state == 'Succeeded':
        state = State.OK
    elif provisioning_state in ['Failed', 'Canceled']:
        state = State.CRIT
    else:
        state = State.WARN
    
    rule_type = data.get('type', 'Unknown')
    priority = data.get('priority', 'Unknown')
    action = data.get('action', {})
    action_type = action.get('type', 'Unknown') if isinstance(action, dict) else str(action)
    rules_count = len(data.get('rules', []))
    
    summary_parts = [
        f"State: {provisioning_state}",
        f"Type: {rule_type}",
        f"Priority: {priority}",
        f"Action: {action_type}",
        f"Rules: {rules_count}",
    ]

    details = render_details([
        ("Provisioning State", provisioning_state),
        ("Type", rule_type),
        ("Priority", priority),
        ("Action", action_type),
        ("Number of Rules", rules_count),
    ])

    yield Result(
        state=state,
        summary="; ".join(summary_parts),
        details=details,
    )


def check_policy(item, section):
    """
    Check Azure Firewall Policy
    """
    policies = section.get('policies', {})
    data = policies.get(item)
    if not data:
        yield Result(state=State.UNKNOWN, summary=f"No data for Policy {item}")
        return

    policy_id = data.get('policy_id')
    policy_name = data.get('name', 'Unknown')

    details = render_details([
        ("Policy Name", policy_name),
        ("Policy", short_id(policy_id)),
        ("Firewall", data.get('firewall_name')),
    ])

    yield Result(
        state=State.OK,
        summary=f"Policy: {policy_name}",
        details=details,
    )


def parse_metrics(string_table):
    """
    Parse Azure Firewall Metrics Data
    """
    parsed_data = {}
    for line in string_table:
        if not line:
            continue
        try:
            metric_data = json.loads(line[0])
            resource_name = metric_data.get('resource_name', 'unknown')
            if resource_name not in parsed_data:
                parsed_data[resource_name] = {}
            metric_name = metric_data.get('metric_name', '')
            parsed_data[resource_name][metric_name] = metric_data
        except (json.JSONDecodeError, IndexError):
            continue
    return parsed_data


def discover_firewall_metrics(section):
    """
    Discover Azure Firewall resources that have metrics
    """
    for resource_name in section:
        yield Service(item=resource_name)


def render_bits_per_second(value):
    """
    Render a bit rate given in bits per second.
    """
    return render.networkbandwidth(value / 8)


def mbit_levels(levels):
    """
    Convert levels configured in Mbit/s to bits per second.
    """
    if not levels or levels[0] != "fixed":
        return levels
    warn, crit = levels[1]
    return ("fixed", (warn * 1000000, crit * 1000000))


def check_firewall_metrics(item, params, section):
    """
    Check Azure Firewall Metrics (FirewallHealth, NetworkRuleHit, Throughput)
    """
    metrics = section.get(item)
    if not metrics:
        yield Result(state=State.UNKNOWN, summary=f"No metrics for {item}")
        return

    def value_of(metric_name):
        """Return the value of an Azure metric or None."""
        return (metrics.get(metric_name) or {}).get('value')

    health = value_of('FirewallHealth')
    if health is not None:
        yield from check_levels(
            health,
            levels_lower=params.get('firewall_health'),
            metric_name="firewall_health",
            render_func=render.percent,
            label="Firewall health",
        )

    rule_hits = value_of('NetworkRuleHit')
    if rule_hits is not None:
        yield from check_levels(
            rule_hits,
            levels_upper=params.get('network_rule_hits'),
            metric_name="networkrulehit",
            render_func=lambda v: f"{v:.0f}/min",
            label="Network rule hits",
        )

    throughput = value_of('Throughput')
    if throughput is not None:
        yield from check_levels(
            throughput,
            levels_upper=mbit_levels(params.get('throughput_upper')),
            levels_lower=mbit_levels(params.get('throughput_lower')),
            metric_name="throughput",
            render_func=render_bits_per_second,
            label="Throughput",
        )


agent_section_azure_extra_azurefirewalls = AgentSection(
    name="azure_extra_azurefirewalls",
    parse_function=parse_properties,
)

agent_section_azure_extra_azurefirewalls_metrics = AgentSection(
    name="azure_extra_azurefirewalls_metrics",
    parse_function=parse_metrics,
)

# Check plugins for each resource type
check_plugin_azure_firewall = CheckPlugin(
    name="azure_firewall",
    sections=["azure_extra_azurefirewalls"],
    service_name="Azure Firewall %s",
    discovery_function=discover_firewalls,
    check_function=check_firewall,
)

check_plugin_azure_firewall_ipconfig = CheckPlugin(
    name="azure_firewall_ipconfig",
    sections=["azure_extra_azurefirewalls"],
    service_name="Azure Firewall IP Config %s",
    discovery_function=discover_ip_configs,
    check_function=check_ip_config,
    check_ruleset_name="azure_firewall_ipconfig",
    check_default_parameters={'state_changed': State.CRIT.value},
)

check_plugin_azure_firewall_rules = CheckPlugin(
    name="azure_firewall_rules",
    sections=["azure_extra_azurefirewalls"],
    service_name="Azure Firewall Rule Collection %s",
    discovery_function=discover_rule_collections,
    check_function=check_rule_collection,
)

check_plugin_azure_firewall_policy = CheckPlugin(
    name="azure_firewall_policy",
    sections=["azure_extra_azurefirewalls"],
    service_name="Azure Firewall Policy %s",
    discovery_function=discover_policies,
    check_function=check_policy,
)

check_plugin_azure_firewall_metrics = CheckPlugin(
    name="azure_firewall_metrics",
    sections=["azure_extra_azurefirewalls_metrics"],
    service_name="Azure Firewall Metrics %s",
    discovery_function=discover_firewall_metrics,
    check_function=check_firewall_metrics,
    check_ruleset_name="azure_firewall_metrics",
    check_default_parameters={
        'firewall_health': ("fixed", (90.0, 50.0)),
        'network_rule_hits': ("no_levels", None),
        'throughput_upper': ("no_levels", None),
        'throughput_lower': ("no_levels", None),
    },
)
