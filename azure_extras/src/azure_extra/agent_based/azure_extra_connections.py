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
    Parse Azure Connections Properties Data to Dict
    """
    parsed_data = {}
    
    for line in string_table:
        if not line:
            continue
        try:
            raw_data = json.loads(line[0])
            connection_name = 'unknown'
            
            if 'localNetworkGateway2' in raw_data:
                # Extract name from the ID path: .../localNetworkGateways/NAME
                lng_id = raw_data['localNetworkGateway2'].get('id', '')
                if lng_id:
                    connection_name = lng_id.split('/')[-1]
            
            parsed_data[connection_name] = raw_data
        except (json.JSONDecodeError, IndexError):
            continue
    
    return parsed_data


def discover_service(section):
    """
    Discover Azure Connections
    """
    for connection_name in section:
        yield Service(item=connection_name)


def check_service(item, section):
    """
    Check Azure Connection Properties
    """
    if item not in section:
        yield Result(state=State.UNKNOWN, summary="Connection not found")
        return
    
    connection = section[item]
    
    # Add JSON debugging info
    json_debug = f"Properties JSON:\n{json.dumps(connection, indent=2)}"
    
    # Provisioning State
    provisioning_state = connection.get('provisioningState', 'Unknown')
    if provisioning_state == 'Succeeded':
        state = State.OK
    elif provisioning_state in ['Failed', 'Canceled']:
        state = State.CRIT
    else:
        state = State.WARN
    
    yield Result(
        state=state,
        summary=f"Provisioning: {provisioning_state}",
        details=json_debug
    )
    
    # Basic Connection Information
    connection_type = connection.get('connectionType', 'Unknown')
    connection_protocol = connection.get('connectionProtocol', 'Unknown')
    yield Result(
        state=State.OK,
        summary=f"Type: {connection_type}, Protocol: {connection_protocol}",
        details=json_debug
    )
    
    # Resource GUID
    resource_guid = connection.get('resourceGuid', 'Unknown')
    yield Result(
        state=State.OK,
        summary=f"Resource GUID: {resource_guid}",
        details=json_debug
    )
    
    # Packet Capture Diagnostic State
    packet_capture_state = connection.get('packetCaptureDiagnosticState', 'Unknown')
    yield Result(
        state=State.OK,
        summary=f"Packet Capture: {packet_capture_state}",
        details=json_debug
    )
    
    # Authentication and Security Settings
    auth_type = connection.get('authenticationType', 'Unknown')
    yield Result(
        state=State.OK,
        summary=f"Authentication: {auth_type}",
        details=json_debug
    )
    
    # BGP Configuration
    enable_bgp = connection.get('enableBgp', False)
    bgp_state = 'Enabled' if enable_bgp else 'Disabled'
    yield Result(
        state=State.OK,
        summary=f"BGP: {bgp_state}",
        details=json_debug
    )
    
    # Connection Mode and Settings
    connection_mode = connection.get('connectionMode', 'Unknown')
    routing_weight = connection.get('routingWeight', 0)
    yield Result(
        state=State.OK,
        summary=f"Mode: {connection_mode}, Routing Weight: {routing_weight}",
        details=json_debug
    )
    
    # Advanced Settings
    use_local_ip = connection.get('useLocalAzureIpAddress', False)
    use_policy_selectors = connection.get('usePolicyBasedTrafficSelectors', False)
    express_route_bypass = connection.get('expressRouteGatewayBypass', False)
    enable_fast_path = connection.get('enablePrivateLinkFastPath', False)
    
    advanced_settings = []
    if use_local_ip:
        advanced_settings.append('Local Azure IP')
    if use_policy_selectors:
        advanced_settings.append('Policy-based Traffic Selectors')
    if express_route_bypass:
        advanced_settings.append('ExpressRoute Bypass')
    if enable_fast_path:
        advanced_settings.append('Fast Path')
    
    if advanced_settings:
        yield Result(
            state=State.OK,
            summary=f"Advanced: {', '.join(advanced_settings)}",
            details=json_debug
        )
    
    # DPD Settings
    dpd_timeout = connection.get('dpdTimeoutSeconds', 0)
    if dpd_timeout > 0:
        yield Result(
            state=State.OK,
            summary=f"DPD Timeout: {dpd_timeout}s",
            details=json_debug
        )
    
    # Traffic Statistics
    ingress_bytes = connection.get('ingressBytesTransferred', 0)
    egress_bytes = connection.get('egressBytesTransferred', 0)
    
    def format_bytes(bytes_value):
        if bytes_value == 0:
            return "0 B"
        elif bytes_value < 1024:
            return f"{bytes_value} B"
        elif bytes_value < 1024**2:
            return f"{bytes_value/1024:.2f} KB"
        elif bytes_value < 1024**3:
            return f"{bytes_value/(1024**2):.2f} MB"
        else:
            return f"{bytes_value/(1024**3):.2f} GB"
    
    yield Result(
        state=State.OK,
        summary=f"Traffic - Ingress: {format_bytes(ingress_bytes)}, Egress: {format_bytes(egress_bytes)}",
        details=json_debug
    )
    
    # Gateway Information
    vng1 = connection.get('virtualNetworkGateway1', {})
    if vng1 and 'id' in vng1:
        vng1_name = vng1['id'].split('/')[-1]
        yield Result(
            state=State.OK,
            summary=f"Virtual Network Gateway: {vng1_name}",
            details=json_debug
        )
    
    lng2 = connection.get('localNetworkGateway2', {})
    if lng2 and 'id' in lng2:
        lng2_name = lng2['id'].split('/')[-1]
        yield Result(
            state=State.OK,
            summary=f"Local Network Gateway: {lng2_name}",
            details=json_debug
        )
    
    # IPSec Policies
    ipsec_policies = connection.get('ipsecPolicies', [])
    if ipsec_policies:
        for i, policy in enumerate(ipsec_policies):
            sa_lifetime = policy.get('saLifeTimeSeconds', 0)
            ipsec_encryption = policy.get('ipsecEncryption', 'Unknown')
            ipsec_integrity = policy.get('ipsecIntegrity', 'Unknown')
            ike_encryption = policy.get('ikeEncryption', 'Unknown')
            ike_integrity = policy.get('ikeIntegrity', 'Unknown')
            dh_group = policy.get('dhGroup', 'Unknown')
            pfs_group = policy.get('pfsGroup', 'Unknown')
            
            yield Result(
                state=State.OK,
                summary=f"IPSec Policy {i+1}: {ipsec_encryption}/{ipsec_integrity}, IKE: {ike_encryption}/{ike_integrity}",
                details=f"IPSec Policy Details:\n" +
                       f"SA Lifetime: {sa_lifetime}s\n" +
                       f"IPSec Encryption: {ipsec_encryption}\n" +
                       f"IPSec Integrity: {ipsec_integrity}\n" +
                       f"IKE Encryption: {ike_encryption}\n" +
                       f"IKE Integrity: {ike_integrity}\n" +
                       f"DH Group: {dh_group}\n" +
                       f"PFS Group: {pfs_group}\n\n" + json_debug
            )
    
    # BGP Custom IP Addresses
    bgp_custom_ips = connection.get('gatewayCustomBgpIpAddresses', [])
    if bgp_custom_ips:
        yield Result(
            state=State.OK,
            summary=f"Custom BGP IPs: {len(bgp_custom_ips)} configured",
            details=f"BGP IP Addresses: {', '.join(bgp_custom_ips)}\n\n" + json_debug
        )
    
    # Traffic Selector Policies
    traffic_policies = connection.get('trafficSelectorPolicies', [])
    if traffic_policies:
        yield Result(
            state=State.OK,
            summary=f"Traffic Selector Policies: {len(traffic_policies)} configured",
            details=f"Traffic Policies:\n{json.dumps(traffic_policies, indent=2)}\n\n" + json_debug
        )
    



agent_section_azure_extra_connections = AgentSection(
    name="azure_extra_connections",
    parse_function=parse_properties,
)

check_plugin_azure_extra_connections = CheckPlugin(
    name="azure_extra_connections",
    sections=["azure_extra_connections"],
    service_name="Azure Connection %s",
    discovery_function=discover_service,
    check_function=check_service,
)