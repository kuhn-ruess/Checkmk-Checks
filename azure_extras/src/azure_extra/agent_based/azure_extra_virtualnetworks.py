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


def parse_virtualnetworks(string_table):
    """
    Parse Azure Virtual Networks Properties Data
    """
    if not string_table or not string_table[0]:
        return {'vnets': {}, 'subnets': {}, 'peerings': {}}
    
    try:
        raw_data = json.loads(string_table[0][0])
        result = {'vnets': {}, 'subnets': {}, 'peerings': {}}
        
        # Check if this is a single VNet object
        if isinstance(raw_data, dict) and 'addressSpace' in raw_data:
            # Extract VNet name from first subnet ID or use default
            vnet_name = "main-vnet"
            if raw_data.get('subnets') and raw_data['subnets']:
                subnet_id = raw_data['subnets'][0].get('id', '')
                if '/virtualNetworks/' in subnet_id:
                    vnet_name = subnet_id.split('/virtualNetworks/')[1].split('/')[0]
            
            # Add VNet data
            result['vnets'][vnet_name] = {
                'name': vnet_name,
                'addressSpace': raw_data.get('addressSpace', {}),
                'enableDdosProtection': raw_data.get('enableDdosProtection'),
                'provisioningState': raw_data.get('provisioningState'),
                'resourceGuid': raw_data.get('resourceGuid'),
                'flowLogConfiguration': raw_data.get('flowLogConfiguration', {}),
                'flowLogs': raw_data.get('flowLogs', []),
                '_raw_data': raw_data
            }
            
            # Add Subnet data
            for subnet in raw_data.get('subnets', []):
                subnet_name = subnet.get('name', 'unknown')
                result['subnets'][subnet_name] = {
                    'name': subnet_name,
                    'addressPrefix': subnet.get('properties', {}).get('addressPrefix'),
                    'provisioningState': subnet.get('properties', {}).get('provisioningState'),
                    'delegations': subnet.get('properties', {}).get('delegations', []),
                    'ipConfigurations': subnet.get('properties', {}).get('ipConfigurations', []),
                    'serviceEndpoints': subnet.get('properties', {}).get('serviceEndpoints', []),
                    'serviceAssociationLinks': subnet.get('properties', {}).get('serviceAssociationLinks', []),
                    'routeTable': subnet.get('properties', {}).get('routeTable'),
                    'privateEndpointNetworkPolicies': subnet.get('properties', {}).get('privateEndpointNetworkPolicies'),
                    'privateLinkServiceNetworkPolicies': subnet.get('properties', {}).get('privateLinkServiceNetworkPolicies'),
                    '_raw_data': subnet
                }
            
            # Add Peering data
            for peering in raw_data.get('virtualNetworkPeerings', []):
                peering_name = peering.get('name', 'unknown')
                result['peerings'][peering_name] = {
                    'name': peering_name,
                    'peeringState': peering.get('properties', {}).get('peeringState'),
                    'peeringSyncLevel': peering.get('properties', {}).get('peeringSyncLevel'),
                    'provisioningState': peering.get('properties', {}).get('provisioningState'),
                    'allowForwardedTraffic': peering.get('properties', {}).get('allowForwardedTraffic'),
                    'allowGatewayTransit': peering.get('properties', {}).get('allowGatewayTransit'),
                    'allowVirtualNetworkAccess': peering.get('properties', {}).get('allowVirtualNetworkAccess'),
                    'useRemoteGateways': peering.get('properties', {}).get('useRemoteGateways'),
                    'remoteAddressSpace': peering.get('properties', {}).get('remoteAddressSpace', {}),
                    'remoteVirtualNetwork': peering.get('properties', {}).get('remoteVirtualNetwork', {}),
                    '_raw_data': peering
                }
            
            return result
        
        # Original logic for list of VNets
        elif isinstance(raw_data, list):
            for vnet in raw_data:
                result['vnets'][vnet['name']] = vnet
            return result
        
        return result
    except (json.JSONDecodeError, IndexError) as e:
        return {'vnets': {}, 'subnets': {}, 'peerings': {}}




# Discovery functions for each resource type
def discover_virtualnetworks(section):
    """
    Discover Azure Virtual Networks
    """
    vnets = section.get('vnets', {})
    for name in vnets:
        yield Service(item=name)


def discover_subnets(section):
    """
    Discover Azure Virtual Network Subnets
    """
    subnets = section.get('subnets', {})
    for name in subnets:
        yield Service(item=name)


def discover_peerings(section):
    """
    Discover Azure Virtual Network Peerings
    """
    peerings = section.get('peerings', {})
    for name in peerings:
        yield Service(item=name)


# Check functions for each resource type
def check_virtualnetwork(item, section):
    """
    Check Azure Virtual Network
    """
    vnets = section.get('vnets', {})
    data = vnets.get(item)
    if not data:
        yield Result(state=State.UNKNOWN, summary=f"No data for VNet {item}")
        return

    # Check provisioning state
    provisioning_state = data.get('provisioningState', 'Unknown')
    if provisioning_state == 'Succeeded':
        state = State.OK
    elif provisioning_state in ['Failed', 'Canceled']:
        state = State.CRIT
    else:
        state = State.WARN
    
    # Get address space info
    address_prefixes = data.get('addressSpace', {}).get('addressPrefixes', [])
    ddos_protection = data.get('enableDdosProtection', False)
    
    summary_parts = [
        f"State: {provisioning_state}",
        f"Address Space: {', '.join(address_prefixes) if address_prefixes else 'None'}",
        f"DDoS Protection: {'Enabled' if ddos_protection else 'Disabled'}"
    ]
    
    yield Result(
        state=state,
        summary="; ".join(summary_parts),
        details=f"VNet Details:\n{json.dumps(data, indent=2)}"
    )
    
    # Add flow log information if available
    flow_logs = data.get('flowLogs', [])
    if flow_logs:
        yield Result(
            state=State.OK,
            summary=f"Flow Logs: {len(flow_logs)} configured"
        )


def check_subnet(item, section):
    """
    Check Azure Virtual Network Subnet
    """
    subnets = section.get('subnets', {})
    data = subnets.get(item)
    if not data:
        yield Result(state=State.UNKNOWN, summary=f"No data for Subnet {item}")
        return

    # Check provisioning state
    provisioning_state = data.get('provisioningState', 'Unknown')
    if provisioning_state == 'Succeeded':
        state = State.OK
    elif provisioning_state in ['Failed', 'Canceled']:
        state = State.CRIT
    else:
        state = State.WARN
    
    address_prefix = data.get('addressPrefix', 'Unknown')
    delegations = data.get('delegations', [])
    ip_configs = data.get('ipConfigurations', [])
    service_endpoints = data.get('serviceEndpoints', [])
    route_table = data.get('routeTable')
    
    summary_parts = [
        f"State: {provisioning_state}",
        f"Address: {address_prefix}"
    ]
    
    if delegations:
        delegation_names = [d.get('properties', {}).get('serviceName', 'Unknown') for d in delegations]
        summary_parts.append(f"Delegations: {', '.join(delegation_names)}")
    
    if ip_configs:
        summary_parts.append(f"IP Configs: {len(ip_configs)}")
        
    if service_endpoints:
        summary_parts.append(f"Service Endpoints: {len(service_endpoints)}")
        
    if route_table:
        summary_parts.append("Route Table: Configured")
    
    yield Result(
        state=state,
        summary="; ".join(summary_parts),
        details=f"Subnet Details:\n{json.dumps(data, indent=2)}"
    )


def check_peering(item, section):
    """
    Check Azure Virtual Network Peering
    """
    peerings = section.get('peerings', {})
    data = peerings.get(item)
    if not data:
        yield Result(state=State.UNKNOWN, summary=f"No data for Peering {item}")
        return

    # Check peering state
    peering_state = data.get('peeringState', 'Unknown')
    sync_level = data.get('peeringSyncLevel', 'Unknown')
    provisioning_state = data.get('provisioningState', 'Unknown')
    
    # Determine overall state
    state = State.OK
    if peering_state != 'Connected':
        state = State.WARN
    if sync_level != 'FullyInSync':
        state = State.WARN
    if provisioning_state not in ['Succeeded']:
        state = State.WARN
        
    # Get remote network info
    remote_vnet = data.get('remoteVirtualNetwork', {})
    remote_address_space = data.get('remoteAddressSpace', {}).get('addressPrefixes', [])
    
    remote_name = 'Unknown'
    if remote_vnet.get('id'):
        # Extract remote VNet name from ID
        vnet_id = remote_vnet['id']
        if '/virtualNetworks/' in vnet_id:
            remote_name = vnet_id.split('/virtualNetworks/')[1]
    
    summary_parts = [
        f"State: {peering_state}",
        f"Sync: {sync_level}",
        f"Remote: {remote_name}",
        f"Remote Address: {', '.join(remote_address_space) if remote_address_space else 'None'}"
    ]
    
    # Add traffic settings
    allow_forwarded = data.get('allowForwardedTraffic', False)
    allow_gateway = data.get('allowGatewayTransit', False)
    use_remote_gw = data.get('useRemoteGateways', False)
    
    traffic_settings = []
    if allow_forwarded:
        traffic_settings.append("Forwarded Traffic")
    if allow_gateway:
        traffic_settings.append("Gateway Transit")
    if use_remote_gw:
        traffic_settings.append("Remote Gateway")
        
    if traffic_settings:
        summary_parts.append(f"Features: {', '.join(traffic_settings)}")
    
    yield Result(
        state=state,
        summary="; ".join(summary_parts),
        details=f"Peering Details:\n{json.dumps(data, indent=2)}"
    )

agent_section_azure_extra_virtualnetworks = AgentSection(
    name="azure_extra_virtualnetworks",
    parse_function=parse_virtualnetworks,
)

check_plugin_azure_extra_virtualnetworks = CheckPlugin(
    name="azure_extra_virtualnetworks",
    sections=["azure_extra_virtualnetworks"],
    service_name="Azure Virtual Network %s",
    discovery_function=discover_virtualnetworks,
    check_function=check_virtualnetwork,
)

check_plugin_azure_extra_virtualnetworks_subnets = CheckPlugin(
    name="azure_extra_virtualnetworks_subnets", 
    sections=["azure_extra_virtualnetworks"],
    service_name="Azure Subnet %s",
    discovery_function=discover_subnets,
    check_function=check_subnet,
)

check_plugin_azure_extra_virtualnetworks_peerings = CheckPlugin(
    name="azure_extra_virtualnetworks_peerings",
    sections=["azure_extra_virtualnetworks"], 
    service_name="Azure VNet Peering %s",
    discovery_function=discover_peerings,
    check_function=check_peering,
)
