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


## exchange_publish.py
Publish new plugin versions to the Checkmk Exchange (exchange.checkmk.com).
Logs in, compares the newest local `<plugin>/<plugin>-<version>.mkp` against the
version currently published on the Exchange, and uploads a new version for every
package that is behind. Uploads go to the Exchange review queue (not instantly live).

Credentials come from the environment (never hard-coded): `EXCHANGE_USER` and
`EXCHANGE_PASSWORD`. If `EXCHANGE_PASSWORD` is unset you are prompted with getpass.

```
EXCHANGE_USER=you@example.com python3 exchange_publish.py \
    --repo /path/to/Checkmk-Checks --dry-run
```
### Features / flags:
- `--dry-run` — only show what would be uploaded
- `--only name1,name2` — restrict to these plugins
- `--exclude name1,name2` — skip these plugins (e.g. packages owned by another author)
- `--limit N` — upload at most N packages
- `--description "..."` — version changelog text (`{ver}` / `{name}` placeholders)
- Auto-detects outdated packages; handles Exchange name collisions by picking the
  highest published version (the active package).
