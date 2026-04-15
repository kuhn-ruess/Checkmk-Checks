# Icinga Connector

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0p1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p18-blue)
<!-- compatibility-badges:end -->

Connects an Icinga instance and mirrors the hosts as piggyback data, including all services, states, outputs, and perfdata.

If the output of the Icinga check contains tables, the plugin tries to convert it to multiple Checkmk services.
