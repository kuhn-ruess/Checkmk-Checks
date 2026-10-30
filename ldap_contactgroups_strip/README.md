# LDAP contact group membership with stripped group names

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.5.0-2f4f4f) ![packaged](https://img.shields.io/badge/packaged-2.5.0p16-blue)
<!-- compatibility-badges:end -->

Adds the LDAP attribute sync plugin *Contact group membership (strip characters from CN)*.
It works like the builtin *Contact group membership* plugin, but removes the configured
characters (default `$`) from the CN of the LDAP group before comparing it with the
contact group names. The comparison ignores upper and lower case.

Use it when LDAP group names contain characters that are not allowed in Checkmk contact
group names. Example: the LDAP group `GRP$Admins` maps to the contact group `GRPAdmins`.
Only existing contact groups are assigned; memberships removed in LDAP are removed on the
next sync.

## Setup

1. Install the MKP and run `omd restart ui-job-scheduler`, otherwise the background
   user sync does not know the plugin yet.
2. Create the contact groups with the stripped names.
3. *Setup > Users > LDAP & Active Directory*, edit the connection, under
   *Attribute sync plug-ins* enable *Contact group membership (strip characters from CN)*
   and disable the builtin *Contact group membership*.
4. Optional: change the characters to remove, enable nested groups or groups from other
   connections.

## Notes

The plugin is a GUI plugin built on Checkmk internals, not on an official plugin API.
It may need an update after a Checkmk major update. Checkmk 2.4 and older are not supported.
