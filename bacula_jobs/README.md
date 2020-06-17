# Bacula / Bareos Backup Job Monitoring

Complete Monitoring for Bacula Backup Jobs. Including Age and State.
Allowed states can be set in WATO. Also the Agent Bakery is supported.

Supports MySQL / MariaDB and PostgreSQL db backends.

The Plugin directly accesses the MySQL / PostgreSQL database to get the states for the Backups
of the last 30 Days, then parses for the newest one to check the state. 

You must set a agent rule if you do not use the default values (MySQL, "bacula" db name, "bacula" db user, localhost db server)
