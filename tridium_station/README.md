# Tridium Station Custom Monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-1.2.8-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-1.5.0p9-blue)
<!-- compatibility-badges:end -->

Tirdium overs a SNMP Interface for the devices, whos kind of special (as this check).
This checks alows not only to set levels for all of the probes, it also enables a special
ruled based config, which is able to set alarms based on conditions from other probes.
This is not exaxclty what the Check_MK Guidlines want, but the best way to handle these devices.



# Functions
 - Probes and Sensors
 - Fuel Levels for Gasoline
 - Rule based alarms like: State A is allowed on Probe A if on Probe B state is B, Otherwise require State C for Probe A.
 
