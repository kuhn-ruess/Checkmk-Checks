# Bacula Backup Monitoring

Complete Monitoring for Bacula Backup Jobs. Including Age and State.
Allowed states can be set in WATO. Also the Agent Bakery is supported.

The Plugin directly accesses the local mysql database to get the states for the Backups
of the last 30 Days, then parses for the newest one to check the state. 

