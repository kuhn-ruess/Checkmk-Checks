# Data Mover

Various Tools to move Data between OMD Sites or
to convert (rrd) data etc.


## Host Mover
Usage:

    host_mover -s SOURCE_SITE -t TARGET_SITE -H HOSTNAME

or:

    host_mover -s SOURCE_SITE -t TARGET_SITE -H "HOST1, HOST2, HOST3"

This program moves hosts between sites.
You can choice which data you want to be moved.

Even logfiles (history) will be handled. Note
that new files in format history-timestamp-hostname will
be created for the moved data. So you can do a easy cleanup

When copying files to the target site, uid and gid will be autodetected.

Options:
```
  -v, --verbose     Verbose mode
  -s, --source      Source OMD Site
  -t, --target      Target OMD Site
  -H, --host        Hostname or comma seperated list
  -L, --logfiles    Handle Logfiles
  -P, --perfdata    Handle Perfdata
  -A, --autochecks  Handle Autocheck files
  -I, --inventory   Handle Inventory Data
  -a, --all         Copy all Data
  -d, --debug       Output Debug Messages
```
## RRD Renamer

Usage:

    rrd_renamer -H HOSTNAME -c config.py / -s source -t target

This program renames RRD files.

* Rename a single file:
 `./rrd_renamer -H HOSTNAME -s old_name -t new_name`

* Rename multiple files:
 Create a config file:
 [('old_name', 'new_name')...]
 `./rrd_rename -H HOSTNAME -c config.py`

Options:

```
  -v, --verbose     Verbose mode
  -h, --help        Print Usage
  -s, --source      Source Name
  -t, --target      Target Name
  -c, --config      Config File
  -p, --path        Optional RRD Path
```
