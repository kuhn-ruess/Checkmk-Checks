# LNX sensors

This check is using the output of sensors (lm-sensors) and transfers all data to server. For easy setup there is a baklet available to bake a agent with plugin. On the server side there is a discovery rule "Sensors" available to select the needed CPUs of the output. Only matched CPUs are activated during discovery.

At the moment only CPUs are supported.
