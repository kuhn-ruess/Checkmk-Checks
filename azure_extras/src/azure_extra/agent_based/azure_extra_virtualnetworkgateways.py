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
    Parse Azure Virtual Network Gateways Properties Data
    """
    if not string_table or not string_table[0]:
        return {'gateways': {}, 'ip_configs': {}, 'bgp_settings': {}, 'vpn_clients': {}, 'remote_peerings': {}, 'nat_rules': {}, 'policy_groups': {}}
    
    try:
        raw_data = json.loads(string_table[0][0])
        result = {'gateways': {}, 'ip_configs': {}, 'bgp_settings': {}, 'vpn_clients': {}, 'remote_peerings': {}, 'nat_rules': {}, 'policy_groups': {}}
        
        # Check if this is a single Gateway object
        if isinstance(raw_data, dict):
            # Extract gateway name from resource GUID or use a default
            gateway_name = raw_data.get('resourceGuid', 'unknown-gateway')
            
            # Add Gateway main data
            result['gateways'][gateway_name] = {
                'name': gateway_name,
                'provisioningState': raw_data.get('provisioningState'),
                'resourceGuid': raw_data.get('resourceGuid'),
                'packetCaptureDiagnosticState': raw_data.get('packetCaptureDiagnosticState'),
                'enablePrivateIpAddress': raw_data.get('enablePrivateIpAddress'),
                'isMigrateToCSES': raw_data.get('isMigrateToCSES'),
                'gatewayType': raw_data.get('gatewayType'),
                'vpnType': raw_data.get('vpnType'),
                'enableBgp': raw_data.get('enableBgp'),
                'activeActive': raw_data.get('activeActive'),
                'sku': raw_data.get('sku', {}),
                'vpnGatewayGeneration': raw_data.get('vpnGatewayGeneration'),
                'allowRemoteVnetTraffic': raw_data.get('allowRemoteVnetTraffic'),
                'allowVirtualWanTraffic': raw_data.get('allowVirtualWanTraffic'),
                'virtualNetworkGatewayMigrationStatus': raw_data.get('virtualNetworkGatewayMigrationStatus', {}),
                '_raw_data': raw_data
            }
            
            # Add IP Configuration data
            for ip_config in raw_data.get('ipConfigurations', []):
                ip_config_name = ip_config.get('name', 'unknown')
                full_name = f"{gateway_name}_{ip_config_name}"
                result['ip_configs'][full_name] = {
                    'name': ip_config_name,
                    'gateway_name': gateway_name,
                    'provisioningState': ip_config.get('properties', {}).get('provisioningState'),
                    'privateIPAllocationMethod': ip_config.get('properties', {}).get('privateIPAllocationMethod'),
                    'publicIPAddress': ip_config.get('properties', {}).get('publicIPAddress', {}),
                    'subnet': ip_config.get('properties', {}).get('subnet', {}),
                    '_raw_data': ip_config
                }
            
            # Add BGP Settings data
            bgp_settings = raw_data.get('bgpSettings', {})
            if bgp_settings:
                bgp_name = f"{gateway_name}_bgp"
                result['bgp_settings'][bgp_name] = {
                    'name': bgp_name,
                    'gateway_name': gateway_name,
                    'asn': bgp_settings.get('asn'),
                    'bgpPeeringAddress': bgp_settings.get('bgpPeeringAddress'),
                    'peerWeight': bgp_settings.get('peerWeight'),
                    'bgpPeeringAddresses': bgp_settings.get('bgpPeeringAddresses', []),
                    '_raw_data': bgp_settings
                }
            
            # Add VPN Client Configuration data
            vpn_client_config = raw_data.get('vpnClientConfiguration', {})
            if vpn_client_config:
                vpn_client_name = f"{gateway_name}_vpnclient"
                result['vpn_clients'][vpn_client_name] = {
                    'name': vpn_client_name,
                    'gateway_name': gateway_name,
                    'vpnClientProtocols': vpn_client_config.get('vpnClientProtocols', []),
                    'vpnAuthenticationTypes': vpn_client_config.get('vpnAuthenticationTypes', []),
                    'vpnClientRootCertificates': vpn_client_config.get('vpnClientRootCertificates', []),
                    'vpnClientRevokedCertificates': vpn_client_config.get('vpnClientRevokedCertificates', []),
                    'vngClientConnectionConfigurations': vpn_client_config.get('vngClientConnectionConfigurations', []),
                    'radiusServers': vpn_client_config.get('radiusServers', []),
                    'vpnClientIpsecPolicies': vpn_client_config.get('vpnClientIpsecPolicies', []),
                    '_raw_data': vpn_client_config
                }
            
            # Add Remote Virtual Network Peerings data
            for idx, peering in enumerate(raw_data.get('remoteVirtualNetworkPeerings', [])):
                if isinstance(peering, dict) and peering.get('id'):
                    peering_id = peering['id']
                    # Extract peering name from ID
                    peering_name = peering_id.split('/')[-1] if peering_id else f'unknown-peering-{idx}'
                    full_name = f"{gateway_name}_{peering_name}"
                    result['remote_peerings'][full_name] = {
                        'name': peering_name,
                        'gateway_name': gateway_name,
                        'peering_id': peering_id,
                        '_raw_data': peering
                    }
            
            # Add NAT Rules data
            for nat_rule in raw_data.get('natRules', []):
                nat_rule_name = nat_rule.get('name', 'unknown')
                full_name = f"{gateway_name}_{nat_rule_name}"
                result['nat_rules'][full_name] = {
                    'name': nat_rule_name,
                    'gateway_name': gateway_name,
                    '_raw_data': nat_rule
                }
            
            # Add Virtual Network Gateway Policy Groups data
            for policy_group in raw_data.get('virtualNetworkGatewayPolicyGroups', []):
                policy_group_name = policy_group.get('name', 'unknown')
                full_name = f"{gateway_name}_{policy_group_name}"
                result['policy_groups'][full_name] = {
                    'name': policy_group_name,
                    'gateway_name': gateway_name,
                    '_raw_data': policy_group
                }
            
            return result
        
        return result
    except (json.JSONDecodeError, IndexError):
        return {'gateways': {}, 'ip_configs': {}, 'bgp_settings': {}, 'vpn_clients': {}, 'remote_peerings': {}, 'nat_rules': {}, 'policy_groups': {}}


# Discovery functions for each resource type
def discover_gateways(section):
    """
    Discover Azure Virtual Network Gateways
    """
    gateways = section.get('gateways', {})
    for name in gateways:
        yield Service(item=name)


def discover_ip_configs(section):
    """
    Discover Azure VPN Gateway IP Configurations
    """
    ip_configs = section.get('ip_configs', {})
    for name in ip_configs:
        yield Service(item=name)


def discover_bgp_settings(section):
    """
    Discover Azure VPN Gateway BGP Settings
    """
    bgp_settings = section.get('bgp_settings', {})
    for name in bgp_settings:
        yield Service(item=name)


def discover_vpn_clients(section):
    """
    Discover Azure VPN Gateway VPN Client Configurations
    """
    vpn_clients = section.get('vpn_clients', {})
    for name in vpn_clients:
        yield Service(item=name)


def discover_remote_peerings(section):
    """
    Discover Azure VPN Gateway Remote VNet Peerings
    """
    remote_peerings = section.get('remote_peerings', {})
    for name in remote_peerings:
        yield Service(item=name)


def discover_nat_rules(section):
    """
    Discover Azure VPN Gateway NAT Rules
    """
    nat_rules = section.get('nat_rules', {})
    for name in nat_rules:
        yield Service(item=name)


def discover_policy_groups(section):
    """
    Discover Azure VPN Gateway Policy Groups
    """
    policy_groups = section.get('policy_groups', {})
    for name in policy_groups:
        yield Service(item=name)


# Check functions for each resource type
def check_gateway(item, section):
    """
    Check Azure Virtual Network Gateway Main Properties
    """
    gateways = section.get('gateways', {})
    data = gateways.get(item)
    if not data:
        yield Result(state=State.UNKNOWN, summary=f"No data for Gateway {item}")
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
    gateway_type = data.get('gatewayType', 'Unknown')
    vpn_type = data.get('vpnType', 'Unknown')
    sku = data.get('sku', {})
    sku_name = sku.get('name', 'Unknown')
    sku_tier = sku.get('tier', 'Unknown')
    sku_capacity = sku.get('capacity', 'Unknown')
    active_active = data.get('activeActive', False)
    enable_bgp = data.get('enableBgp', False)
    generation = data.get('vpnGatewayGeneration', 'Unknown')
    
    summary_parts = [
        f"State: {provisioning_state}",
        f"Type: {gateway_type} ({vpn_type})",
        f"SKU: {sku_name} ({sku_tier})",
        f"Capacity: {sku_capacity}",
        f"Mode: {'Active-Active' if active_active else 'Active-Standby'}",
        f"BGP: {'Enabled' if enable_bgp else 'Disabled'}",
        f"Generation: {generation}"
    ]
    
    yield Result(
        state=state,
        summary="; ".join(summary_parts),
        details=f"VPN Gateway Details:\n{json.dumps(data, indent=2)}"
    )
    
    # Check migration status
    migration_status = data.get('virtualNetworkGatewayMigrationStatus', {})
    migration_state = migration_status.get('state', 'None')
    if migration_state != 'None':
        migration_phase = migration_status.get('phase', 'Unknown')
        error_message = migration_status.get('errorMessage', '')
        
        if error_message:
            yield Result(
                state=State.WARN,
                summary=f"Migration: {migration_state} ({migration_phase}) - {error_message}"
            )
        else:
            yield Result(
                state=State.OK,
                summary=f"Migration: {migration_state} ({migration_phase})"
            )


def check_ip_config(item, section):
    """
    Check Azure VPN Gateway IP Configuration
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
    
    allocation_method = data.get('privateIPAllocationMethod', 'Unknown')
    public_ip_id = data.get('publicIPAddress', {}).get('id', '')
    public_ip_name = public_ip_id.split('/')[-1] if public_ip_id else 'None'
    subnet_id = data.get('subnet', {}).get('id', '')
    subnet_name = subnet_id.split('/')[-1] if subnet_id else 'None'
    
    summary_parts = [
        f"State: {provisioning_state}",
        f"IP Allocation: {allocation_method}",
        f"Public IP: {public_ip_name}",
        f"Subnet: {subnet_name}"
    ]
    
    yield Result(
        state=state,
        summary="; ".join(summary_parts),
        details=f"IP Config Details:\n{json.dumps(data, indent=2)}"
    )


def check_bgp_settings(item, section):
    """
    Check Azure VPN Gateway BGP Settings
    """
    bgp_settings = section.get('bgp_settings', {})
    data = bgp_settings.get(item)
    if not data:
        yield Result(state=State.UNKNOWN, summary=f"No data for BGP Settings {item}")
        return

    asn = data.get('asn', 'Unknown')
    bgp_peering_address = data.get('bgpPeeringAddress', 'Unknown')
    peer_weight = data.get('peerWeight', 'Unknown')
    peering_addresses = data.get('bgpPeeringAddresses', [])
    
    summary_parts = [
        f"ASN: {asn}",
        f"Peering Address: {bgp_peering_address}",
        f"Peer Weight: {peer_weight}",
        f"Peering IPs: {len(peering_addresses)}"
    ]
    
    yield Result(
        state=State.OK,
        summary="; ".join(summary_parts),
        details=f"BGP Settings Details:\n{json.dumps(data, indent=2)}"
    )
    
    # Check individual peering addresses
    for peering_addr in peering_addresses:
        tunnel_ips = peering_addr.get('tunnelIpAddresses', [])
        default_bgp_ips = peering_addr.get('defaultBgpIpAddresses', [])
        
        if tunnel_ips:
            yield Result(
                state=State.OK,
                summary=f"Tunnel IPs: {', '.join(tunnel_ips)}, BGP IPs: {', '.join(default_bgp_ips)}"
            )


def check_vpn_client(item, section):
    """
    Check Azure VPN Gateway VPN Client Configuration
    """
    vpn_clients = section.get('vpn_clients', {})
    data = vpn_clients.get(item)
    if not data:
        yield Result(state=State.UNKNOWN, summary=f"No data for VPN Client Config {item}")
        return

    protocols = data.get('vpnClientProtocols', [])
    auth_types = data.get('vpnAuthenticationTypes', [])
    root_certs = data.get('vpnClientRootCertificates', [])
    revoked_certs = data.get('vpnClientRevokedCertificates', [])
    radius_servers = data.get('radiusServers', [])
    ipsec_policies = data.get('vpnClientIpsecPolicies', [])
    
    summary_parts = [
        f"Protocols: {', '.join(protocols) if protocols else 'None'}",
        f"Auth Types: {', '.join(auth_types) if auth_types else 'None'}",
        f"Root Certs: {len(root_certs)}",
        f"Revoked Certs: {len(revoked_certs)}",
        f"RADIUS: {len(radius_servers)}",
        f"IPSec Policies: {len(ipsec_policies)}"
    ]
    
    yield Result(
        state=State.OK,
        summary="; ".join(summary_parts),
        details=f"VPN Client Config Details:\n{json.dumps(data, indent=2)}"
    )


def check_remote_peering(item, section):
    """
    Check Azure VPN Gateway Remote VNet Peering
    """
    remote_peerings = section.get('remote_peerings', {})
    data = remote_peerings.get(item)
    if not data:
        yield Result(state=State.UNKNOWN, summary=f"No data for Remote Peering {item}")
        return

    peering_id = data.get('peering_id', 'Unknown')
    
    # Extract useful information from the peering ID
    if '/virtualNetworks/' in peering_id and '/virtualNetworkPeerings/' in peering_id:
        parts = peering_id.split('/')
        subscription_id = parts[2] if len(parts) > 2 else 'Unknown'
        resource_group = parts[4] if len(parts) > 4 else 'Unknown'
        vnet_name = parts[8] if len(parts) > 8 else 'Unknown'
        peering_name = parts[10] if len(parts) > 10 else 'Unknown'
        
        summary_parts = [
            f"VNet: {vnet_name}",
            f"Resource Group: {resource_group}",
            f"Subscription: {subscription_id[:8]}...",
            f"Peering: {peering_name}"
        ]
        
        yield Result(
            state=State.OK,
            summary="; ".join(summary_parts),
            details=f"Remote Peering Details:\n{json.dumps(data, indent=2)}"
        )
    else:
        yield Result(
            state=State.OK,
            summary=f"Peering ID: {peering_id}",
            details=f"Remote Peering Details:\n{json.dumps(data, indent=2)}"
        )


def check_nat_rule(item, section):
    """
    Check Azure VPN Gateway NAT Rule
    """
    nat_rules = section.get('nat_rules', {})
    data = nat_rules.get(item)
    if not data:
        yield Result(state=State.UNKNOWN, summary=f"No data for NAT Rule {item}")
        return

    # Since NAT rules appear to be empty in the provided data, just confirm existence
    yield Result(
        state=State.OK,
        summary=f"NAT Rule: {data.get('name', 'Unknown')}",
        details=f"NAT Rule Details:\n{json.dumps(data, indent=2)}"
    )


def check_policy_group(item, section):
    """
    Check Azure VPN Gateway Policy Group
    """
    policy_groups = section.get('policy_groups', {})
    data = policy_groups.get(item)
    if not data:
        yield Result(state=State.UNKNOWN, summary=f"No data for Policy Group {item}")
        return

    # Since policy groups appear to be empty in the provided data, just confirm existence
    yield Result(
        state=State.OK,
        summary=f"Policy Group: {data.get('name', 'Unknown')}",
        details=f"Policy Group Details:\n{json.dumps(data, indent=2)}"
    )


agent_section_azure_extra_virtualnetworkgateways = AgentSection(
    name="azure_extra_virtualnetworkgateways",
    parse_function=parse_properties,
)

# Check plugins for each resource type
check_plugin_azure_vpn_gateway = CheckPlugin(
    name="azure_vpn_gateway",
    sections=["azure_extra_virtualnetworkgateways"],
    service_name="Azure VPN Gateway %s",
    discovery_function=discover_gateways,
    check_function=check_gateway,
)

check_plugin_azure_vpn_gateway_ipconfig = CheckPlugin(
    name="azure_vpn_gateway_ipconfig",
    sections=["azure_extra_virtualnetworkgateways"],
    service_name="Azure VPN Gateway IP Config %s",
    discovery_function=discover_ip_configs,
    check_function=check_ip_config,
)

check_plugin_azure_vpn_gateway_bgp = CheckPlugin(
    name="azure_vpn_gateway_bgp",
    sections=["azure_extra_virtualnetworkgateways"],
    service_name="Azure VPN Gateway BGP %s",
    discovery_function=discover_bgp_settings,
    check_function=check_bgp_settings,
)

check_plugin_azure_vpn_gateway_vpnclient = CheckPlugin(
    name="azure_vpn_gateway_vpnclient",
    sections=["azure_extra_virtualnetworkgateways"],
    service_name="Azure VPN Gateway VPN Client %s",
    discovery_function=discover_vpn_clients,
    check_function=check_vpn_client,
)

check_plugin_azure_vpn_gateway_remotepeering = CheckPlugin(
    name="azure_vpn_gateway_remotepeering",
    sections=["azure_extra_virtualnetworkgateways"],
    service_name="Azure VPN Gateway Remote Peering %s",
    discovery_function=discover_remote_peerings,
    check_function=check_remote_peering,
)

check_plugin_azure_vpn_gateway_natrule = CheckPlugin(
    name="azure_vpn_gateway_natrule",
    sections=["azure_extra_virtualnetworkgateways"],
    service_name="Azure VPN Gateway NAT Rule %s",
    discovery_function=discover_nat_rules,
    check_function=check_nat_rule,
)

check_plugin_azure_vpn_gateway_policygroup = CheckPlugin(
    name="azure_vpn_gateway_policygroup",
    sections=["azure_extra_virtualnetworkgateways"],
    service_name="Azure VPN Gateway Policy Group %s",
    discovery_function=discover_policy_groups,
    check_function=check_policy_group,
)