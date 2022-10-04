# Pure Checks

This check is an agent based check, which can do monitoring for base services on devices.
In Order that the Plugin works, you need to install the Pure Storage FlashArray REST Client (https://pypi.org/project/purestorage/) installed in
your Checkmk Site. This can be done using pip:
**pip3 install purestorage**

## Supported checks

1) Alerts<br>
It will show critical for existing open and critical alerts.
It will show warning for existing open and warning alerts.
It will show ok for existing open and informational alerts.
No wato configuration available.

2) Devices<br>
It will show one service for each device with storage type and capacity.
Service will be critical if state is not healthy. Otherwise it is ok.
No wato configuration available.

3) Hardware<br>
It will show one service for each componet with serial number, if available.
Service will be critical if state is not ok. Otherwise it is ok.
No wato configuration available.
