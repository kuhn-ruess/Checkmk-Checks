# CMK API Script


## activate_changes.py
Activate changes with the CMK2.x API. Please set Url, User and Password inside the Script

Note: If the Activation fails, the Checkmk API as least of 2.2.0p14 still returns an OK state.
The Script therfore can't detect that.
### Features:
- Detect open Changes
- Trigger Activate Changes
- Waits for Activate to be finsh
- Exits if changes are made while the script is started.
- use -d for Debug Outputs
