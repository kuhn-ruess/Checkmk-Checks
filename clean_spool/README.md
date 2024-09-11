# Clean Spoolfiles
In case you use the Notification spooler, and have an outburst of Notification, these will block the spooler some time to process them. At this time, it can happen that Recovery Notifications are sent, but stuck behind the Problem Notification, which are still not sent out.  This Script checks the Spool directory and deletes all Notifications who met these criteria.
