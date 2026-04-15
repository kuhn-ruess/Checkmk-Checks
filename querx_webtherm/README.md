# Querx Webtherm monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.3.0p35-blue)
<!-- compatibility-badges:end -->

SNMP monitoring for Querx Webtherm environmental sensors. Creates a
temperature and a humidity service per device using the built-in Checkmk
temperature and humidity check helpers, so standard WATO thresholds apply.

## How it works

Both sections are auto-detected with `contains(sysDescr, "Querx")` and
fetch from `.1.3.6.1.4.1.3444.1.14.1.2.1.5`:

| Section | OID | Parse | Service item |
| --- | --- | --- | --- |
| `querx_webtherm_temp` | `.1` | raw value / 10 (deg C) | `Temperature Sensor` |
| `querx_webtherm_humidity` | `.2` | raw value (percent) | `Humidity Sensor` |

The temperature check delegates to `cmk.plugins.lib.temperature.check_temperature`
(using a shared value store for trend calculations) and the humidity
check delegates to `cmk.plugins.lib.humidity.check_humidity`. Because they
use the standard check groups, any existing WATO rules for temperature /
humidity thresholds apply.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/querx_webtherm/agent_based/temp.py` | SNMP section and check plugin for the temperature sensor. |
| `src/querx_webtherm/agent_based/humidity.py` | SNMP section and check plugin for the humidity sensor. |

## Installation

1. Install the MKP on the Checkmk site.
2. Add the Querx device as an SNMP host. Run service discovery to create
   the services `Temperature Sensor` and `Humidity Sensor`.

## Configuration

Because the checks reuse the built-in `temperature` and `humidity` check
groups, no dedicated WATO rules are shipped. Configure thresholds through
the standard Checkmk rules *Temperature* and *Humidity Levels*.

## Services & metrics

- `Temperature Sensor` - delegates to the standard Checkmk temperature
  check (metric `temp`).
- `Humidity Sensor` - delegates to the standard Checkmk humidity check
  (metric `humidity`).
