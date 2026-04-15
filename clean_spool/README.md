# Clean Spoolfiles

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.3.0p9-blue)
<!-- compatibility-badges:end -->
In case you use the Notification spooler, and have an outburst of Notification, these will block the spooler some time to process them. At this time, it can happen that Recovery Notifications are sent, but stuck behind the Problem Notification, which are still not sent out.  This Script checks the Spool directory and deletes all Notifications who met these criteria.
