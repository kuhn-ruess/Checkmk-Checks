# EC Event Clean-up
In case the Event Console is flooded with events from Checkmk, which are already OK, but you have to wait for the Notification Spooler,
you can use this script to speed it up. Run: **sync_ec_events.py** from within your site. The Script will show you all Checkmk Based EC Events, which are already back to OK in Checkmk.
Then, if you confirm, the script will Archive this Events
