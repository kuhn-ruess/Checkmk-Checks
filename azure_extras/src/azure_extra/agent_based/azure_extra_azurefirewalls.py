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
)


def parse_properties(string_table):
    """
    Parse Azure Firewalls Properties Data
    """
    if not string_table or not string_table[0]:
        return {'firewalls': {}, 'ip_configs': {}, 'rule_collections': {}, 'policies': {}}
    
    try:
        raw_data = json.loads(string_table[0][0])
        result = {'firewalls': {}, 'ip_configs': {}, 'rule_collections': {}, 'policies': {}}
        
        # Check if this is a single Firewall object
        if isinstance(raw_data, dict):
            firewall_name = raw_data.get('name', 'unknown-firewall')
            
            # Add Firewall main data
            result['firewalls'][firewall_name] = {
                'name': firewall_name,
                'provisioningState': raw_data.get('provisioningState'),
                'sku': raw_data.get('sku', {}),
                'threatIntelMode': raw_data.get('threatIntelMode'),
                'additionalProperties': raw_data.get('additionalProperties', {}),
                'firewallPolicy': raw_data.get('firewallPolicy', {}),
                '_raw_data': raw_data
            }
            
            # Add IP Configuration data
            for ip_config in raw_data.get('ipConfigurations', []):
                ip_config_name = ip_config.get('name', 'unknown')
                full_name = f"{firewall_name}_{ip_config_name}"
                result['ip_configs'][full_name] = {
                    'name': ip_config_name,
                    'firewall_name': firewall_name,
                    'provisioningState': ip_config.get('properties', {}).get('provisioningState'),
                    'privateIPAddress': ip_config.get('properties', {}).get('privateIPAddress'),
                    'privateIPAllocationMethod': ip_config.get('properties', {}).get('privateIPAllocationMethod'),
                    'publicIPAddress': ip_config.get('properties', {}).get('publicIPAddress', {}),
                    'subnet': ip_config.get('properties', {}).get('subnet', {}),
                    '_raw_data': ip_config
                }
            
            # Add Rule Collections data
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
                    '_raw_data': rule_collection
                }
            
            # Add Policy data if available
            policy = raw_data.get('firewallPolicy', {})
            if policy.get('id'):
                policy_name = policy.get('id', '').split('/')[-1] if policy.get('id') else 'unknown-policy'
                full_name = f"{firewall_name}_{policy_name}"
                result['policies'][full_name] = {
                    'name': policy_name,
                    'firewall_name': firewall_name,
                    'policy_id': policy.get('id'),
                    '_raw_data': policy
                }
            
            return result
        
        return result
    except (json.JSONDecodeError, IndexError):
        return {'firewalls': {}, 'ip_configs': {}, 'rule_collections': {}, 'policies': {}}


# Discovery functions for each resource type
def discover_firewalls(section):
    """
    Discover Azure Firewalls
    """
    firewalls = section.get('firewalls', {})
    for name in firewalls:
        yield Service(item=name)


def discover_ip_configs(section):
    """
    Discover Azure Firewall IP Configurations
    """
    ip_configs = section.get('ip_configs', {})
    for name in ip_configs:
        yield Service(item=name)


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
    policy_id = data.get('firewallPolicy', {}).get('id', 'None')
    
    summary_parts = [
        f"State: {provisioning_state}",
        f"SKU: {sku_name} ({sku_tier})",
        f"Threat Intel: {threat_intel_mode}",
        f"Policy: {'Configured' if policy_id != 'None' else 'Not configured'}"
    ]
    
    yield Result(
        state=state,
        summary="; ".join(summary_parts),
        details=f"Firewall Details:\n{json.dumps(data, indent=2)}"
    )


def check_ip_config(item, section):
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
    
    private_ip = data.get('privateIPAddress', 'Unknown')
    allocation_method = data.get('privateIPAllocationMethod', 'Unknown')
    public_ip_id = data.get('publicIPAddress', {}).get('id', 'None')
    subnet_id = data.get('subnet', {}).get('id', 'None')
    
    summary_parts = [
        f"State: {provisioning_state}",
        f"Private IP: {private_ip} ({allocation_method})",
        f"Public IP: {'Configured' if public_ip_id != 'None' else 'None'}",
        f"Subnet: {'Configured' if subnet_id != 'None' else 'None'}"
    ]
    
    yield Result(
        state=state,
        summary="; ".join(summary_parts),
        details=f"IP Config Details:\n{json.dumps(data, indent=2)}"
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
        f"Rules: {rules_count}"
    ]
    
    yield Result(
        state=state,
        summary="; ".join(summary_parts),
        details=f"Rule Collection Details:\n{json.dumps(data, indent=2)}"
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

    policy_id = data.get('policy_id', 'Unknown')
    policy_name = data.get('name', 'Unknown')
    
    yield Result(
        state=State.OK,
        summary=f"Policy: {policy_name}, ID: {policy_id.split('/')[-1] if policy_id != 'Unknown' else 'Unknown'}",
        details=f"Policy Details:\n{json.dumps(data, indent=2)}"
    )


agent_section_azure_extra_azurefirewalls = AgentSection(
    name="azure_extra_azurefirewalls",
    parse_function=parse_properties,
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
