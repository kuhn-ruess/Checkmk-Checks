# Check for Palo Alto Versions (superseded)

> **Superseded by [`palo_alto`](../palo_alto/) 1.1.0 or newer.**
> Both the ThreatID and the URL-Filtering version checks are now part of the
> consolidated `palo_alto` MKP and have been rewritten for the Checkmk 2.4
> Plugin API. Install `palo_alto` instead of this package.

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.0.0p22-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-2.3-informational) ![packaged](https://img.shields.io/badge/packaged-2.0.0p22-blue)
<!-- compatibility-badges:end -->

Legacy SNMP checks for Palo Alto firewalls (ThreatID and URL-Filtering
content versions). Last packaged MKP is `palo_alto_versions-1.0.1.mkp`; it
targets the legacy `register.*` agent-based API and will not load under
Checkmk 2.4.

## Migration

Uninstall `palo_alto_versions` and install `palo_alto` >= 1.1.0. The check
plugin names stay `palo_alto_threadid` and `palo_alto_urlfilter`, so existing
services keep their identity. The historical typo "TheadID" in the service
name is preserved for the same reason.
