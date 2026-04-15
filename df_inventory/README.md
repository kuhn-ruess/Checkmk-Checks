# Filesystem Inventory

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p13-blue)
<!-- compatibility-badges:end -->

Adds filesystem ownership data to the Checkmk HW/SW inventory by looking up the owner of each mount point in `/etc/passwd` and collecting their email address. A wrapper for the built-in `mail` notification script then redirects Filesystem service notifications to that owner instead of the normal contact.

## How it works

Shell plugins for Linux, AIX and Solaris are deployed to the agent host. Each iterates over local mount points from `df -lP` (skipping `tmpfs`), resolves the directory owner via `ls -od`, looks the user up in `/etc/passwd`, extracts email and full name, and prints one CSV line per mount that has a mail address:

```text
<<<inventorize_df:sep(59)>>>
/;root;root;root@example.com
/var;webuser;Web User;web@example.com
```

The inventory plugin `inventorize_df` parses the section and writes rows under `software -> filesystem_owners` with columns `filesystem`, `owner`, `owner_name`, `owner_email`.

The notification script `df_mail` wraps Checkmk's built-in mail plugin. For services whose name starts with `Filesystem `, it reads `var/check_mk/inventory/<host>`, finds the matching `filesystem_owners` row and overwrites `NOTIFY_CONTACTEMAIL` with the owner address before handing off to `cmk.notification_plugins.mail.main()`.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/agents/plugins/df_inventory_linux.sh` | Linux agent plugin. |
| `src/agents/plugins/df_inventory_aix.sh` | AIX agent plugin. |
| `src/agents/plugins/df_inventory_solaris.sh` | Solaris agent plugin. |
| `src/df_inventory/agent_based/inventorize_df.py` | Section parser and HW/SW inventory plugin. |
| `src/df_inventory/agent_based/bakery.py` | Bakery hook for deployment of the agent plugin. |
| `src/df_inventory/rulesets/df_inventory.py` | `AgentConfig` rule controlling deployment (sync / cached / off). |
| `src/df_inventory/rulesets/notification_parameter.py` | Registers the `df_mail` notification parameter set by subclassing the built-in mail parameter. |
| `src/notifications/df_mail` | Notification script that rewrites the contact email from inventory. |

## Installation

1. Install the MKP on the Checkmk site.
2. Enable **DF Inventory: Filesystem Ownership Data** in the Bakery for the target hosts and bake / deploy agents. Without Bakery, copy the matching plugin from `src/agents/plugins/` into the agent plugins directory.
3. Create a **Notifications** rule that uses the `df_mail` script for Filesystem services; pick the owner via inventory by routing through this script.

## Configuration

Rule: **Setup -> Agents -> Agent rules -> DF Inventory: Filesystem Ownership Data**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `deployment` | CascadingSingleChoice | `sync` (deploy and run), `cached` (deploy and run every N minutes), or `do_not_deploy`. |

## Known limitations

- Linux plugin uses `cut -d ";"` while `/etc/passwd` uses `:` as the delimiter — the shipped Linux plugin as committed will only emit a row if `$MAIL` already contains an `@`, so behaviour depends on whether the `cut` output lines up on your distribution.
- `notification_parameter.py` takes a "risky path" into `cmk.gui.wato._notification_parameter._mail` and subclasses the private `NotificationParameterMail`. A comment flags that this can break across Checkmk updates.
- The `df_mail` wrapper depends on the inventory file existing; if it is missing for a host the wrapper falls through to the default mail script without overriding the contact.
