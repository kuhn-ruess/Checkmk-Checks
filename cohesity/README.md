# Cohesity Checks

This check is an agent based check, which can do monitoring for base services on a cluster.

## Supported checks

1) Alertsy<br>
It will show critical for services with existing alerts. No wato configuration available.

2) Node status<br>
It will show a service summary for good and failed services. In service detail it will
show a list of all services in both states. It can be configured to ignore services for
summary with rule "Cohesity node status ignored services".

3) Storage<br>
It will show the usage of the total filesystem size of a cluster. It can be configured
with absolut levels for the filesystem size.

4) Unprotected<br>
It will show a critical, if unprotected objects exist in configuration. In service detail
it will show size if protected objects.
