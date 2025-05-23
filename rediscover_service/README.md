# Rediscovery services

Notification plugin is doing a rediscovery on services, which are matching. It will make this service undecided and monitoried again.
Stored parameters will be updated. It is useful for mount options, interfaces, smart, ...

## Configuration example
Add a new notification rule and choose Rediscovery service as a plugin.

Now specify the hostname of the Checkmk server or the master server and sitename:
![Plugin configuration](https://github.com/user-attachments/assets/658a71e9-7547-4824-9db8-8d01cb19deb3)

After that, you should select a user, which will be used for the notification. Easiest selection is cmkadmin. This user exists and will always be available:

![User selection](https://github.com/user-attachments/assets/a7ccf30f-196c-4d1a-9100-defafc1c460d)

Last step is to select which hosts and services are matched. I have some interfaces, which change speed, if
it is not needed to save energy. To take care about it, I have choosen the hosts, services and state of service:
![Conditions](https://github.com/user-attachments/assets/5a4b3102-750b-480e-9d2e-a41c012d7188)
