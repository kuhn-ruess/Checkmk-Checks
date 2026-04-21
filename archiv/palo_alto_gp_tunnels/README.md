# PaloAlto Globalprotect Tunnels (superseded)

> **Superseded by [`palo_alto`](../palo_alto/) 1.1.0 or newer.**
> The GlobalProtect tunnel check is now part of the consolidated `palo_alto`
> MKP and has been rewritten for the Checkmk 2.4 Plugin API with configurable
> WARN/CRIT thresholds. Install `palo_alto` instead of this package.

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.0.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-2.3-informational) ![packaged](https://img.shields.io/badge/packaged-2.0.0p20-blue)
<!-- compatibility-badges:end -->

Legacy SNMP check for Palo Alto GlobalProtect gateways. Reports how many
GlobalProtect VPN tunnels are currently active compared to the configured
maximum on the device. Last packaged MKP in this directory is
`palo_alto_gp_tunnels-1.0.4.mkp`; it targets the legacy `register.*`
agent-based API and will not load under Checkmk 2.4.

## Migration

Uninstall `palo_alto_gp_tunnels` and install `palo_alto` >= 1.1.0. The check
plugin name stays `palo_alto_gp_tunnels`, so existing services and rules keep
their identity. Thresholds on remaining free tunnel slots can now be set via
the ruleset **Palo Alto GlobalProtect tunnels**.
