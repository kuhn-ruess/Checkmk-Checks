# HTML Email Notification to LDAP Groups

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0b1-2f4f4f) ![packaged](https://img.shields.io/badge/packaged-2.5.0-blue)
<!-- compatibility-badges:end -->

Checkmk notification plugin that lets an **LDAP/AD group be used as mail
recipient**. It wraps the built-in HTML mail plugin: only the recipient is
resolved, everything else — layout, graphs, subject, SMTP settings — is the
normal Checkmk email configuration.

## How it works

The contact's email address names a group instead of a mailbox, e.g.
`Monitoring-Team`.

1. The recipient list from `CONTACTEMAIL` is split on `,` / `;`.
2. Entries containing an `@` are mailboxes and stay untouched — groups and
   plain addresses can be mixed.
3. Every other entry is searched as `cn` or `sAMAccountName` below the group DN
   of the **LDAP connections already configured in the site**
   (`Setup → Users → LDAP connections`): server, TLS, bind DN and bind password
   all come from there. No second set of credentials.
4. The `mail` attribute of the group becomes the recipient.
5. The rewritten recipient is handed to the built-in `mail` plugin, which sends
   the notification as usual. Bulk notifications are supported.

If a group has no address, the reason is written to stderr and shown in the
notification history. Recipients that did resolve are still notified; only when
nothing is left the notification fails permanently (exit code 2, no retry).

## Package contents

| Path | Purpose |
| --- | --- |
| `src/notifications/mail_ldap_group` | Notification script (Python, uses `python-ldap` shipped with Checkmk). |
| `src/mail_ldap_group/rulesets/notification_parameter.py` | Notification parameters: the complete built-in HTML mail form. |

## Configuration

`Setup → Notifications → Add rule`, notification method **HTML Email (LDAP
group recipients)**. The parameters are the ones of the built-in HTML email —
there is nothing to configure for the LDAP lookup itself.

The sender is called *Custom sender ("From")* as usual but is stored under the
key `sender`, because `from` is no valid ruleset key; the script renames it
back for the built-in plugin.

## Requirements

An LDAP connection configured in the site. The plugin reads
`etc/check_mk/multisite.d/wato/user_connections.mk` and resolves the bind
password through `cmk.utils.password_store`.
