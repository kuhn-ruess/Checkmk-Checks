# HTML Email Notification to LDAP Groups

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0b1-2f4f4f) ![packaged](https://img.shields.io/badge/packaged-2.5.0-blue)
<!-- compatibility-badges:end -->

Checkmk notification plugin that lets an **LDAP/AD group be used as mail
recipient**. It wraps the built-in HTML mail plugin: only the recipient is
resolved, everything else — layout, graphs, subject, SMTP settings — is the
normal Checkmk email configuration.

## How it works

The contact's email address (or one entry of it) names a group instead of a
mailbox, e.g. `Monitoring-Team` or
`CN=Monitoring-Team,OU=Groups,DC=example,DC=com`.

1. The recipient list from `CONTACTEMAIL` is split on `,` / `;`. A DN contains
   commas itself and is kept together; use `;` to separate several DNs.
2. Entries containing an `@` are mailboxes and are passed through untouched —
   groups and plain addresses can be mixed.
3. Every other entry is looked up in the **LDAP connections that are already
   configured in the site** (`Setup → Users → LDAP connections`): server list,
   TLS, bind DN, bind password (via the Checkmk password store), group DN and
   group scope all come from there. No second set of credentials.
4. The value of the group's mail attribute (`mail` by default) becomes the
   recipient. Optionally the addresses of the group members are used when the
   group itself is not mail enabled.
5. The rewritten recipient is handed to the built-in `mail` plugin, which sends
   the notification as usual. Bulk notifications are supported.

An entry that looks like a DN (`cn=…`) is read directly; anything else is
searched below the connection's group DN with
`(&(|(objectclass=group)(objectclass=groupOfNames)(objectclass=groupOfUniqueNames)(objectclass=posixGroup))(|(cn=…)(sAMAccountName=…)))`,
which can be replaced by a custom filter.

If a group cannot be resolved, the reason is written to stderr and shown in the
notification history. Recipients that did resolve are still notified; only when
nothing is left the notification fails permanently (exit code 2, no retry).

## Package contents

| Path | Purpose |
| --- | --- |
| `src/notifications/mail_ldap_group` | Notification script (Python, uses `python-ldap` shipped with Checkmk). |
| `src/mail_ldap_group/rulesets/notification_parameter.py` | Notification parameters: the LDAP options plus the complete built-in HTML mail form. |

## Configuration

`Setup → Notifications → Add rule`, notification method **HTML Email (LDAP
group recipients)**. The parameters are the ones of the built-in HTML email
plus:

| Option | Meaning |
| --- | --- |
| LDAP connection | ID of the connection to query. Empty = try all enabled connections. |
| Mail attribute of the group | Attribute holding the address, default `mail`. |
| Custom group filter | LDAP filter with the macro `$GROUP$`, replaces the default group filter. |
| Member attribute of the group | Only needed for member attributes other than `member`, `uniqueMember`, `memberUid`. |
| Fall back to the group members | Use the members' addresses if the group has none of its own. |

## Requirements

An LDAP connection configured in the site. The plugin reads
`etc/check_mk/multisite.d/wato/user_connections.mk` and resolves the bind
password through `cmk.utils.password_store`.
