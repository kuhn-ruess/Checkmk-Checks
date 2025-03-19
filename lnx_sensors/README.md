# LNX sensors

This check is using the output of sensors (lm-sensors) and transfers all data to server. For easy setup there is a baklet called "Sensors" available to bake an agent with plugin. On server side there is a discovery rule "Sensors discovery" available to select the needed items of the output. Only matching on CPU items is currently supported and discovers all CPUs during discovery.

## Requirements
The command sensors (lm-sensors) must be available on systems. Please install m-sensors package.

## Baklet
With the baket the needed plugin is integrated in the agent. This package can be used with automativ agents updates or the install archives can be download for manual installtion.

## Discovery rule
To get services discovery, you need to setup a discovery rule for your hosts, which items shoudl be detected. Currently only CPU is supported.

## Special handling
If this plugin is activated, the output of lnx_therma is automatically blocked and can not be used.
