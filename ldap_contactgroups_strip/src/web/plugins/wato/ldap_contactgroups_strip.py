#!/usr/bin/env python3
"""LDAP sync plugin: contact group membership with characters stripped from the group CN

Like the builtin "Contact group membership" plugin, but an LDAP group matches a
contact group when its CN equals the contact group name after removing the
configured characters (default: "$"). Example: LDAP group "GRP$Admins" -> "GRPAdmins".
"""

from cmk.gui.watolib.groups_io import load_contact_group_information
from cmk.gui.ldap_integration.ldap_connector import (
    _get_group_member_cmp_val,
    _group_membership_parameters,
    get_connection,
    LDAPAttributePlugin,
    ldap_attribute_plugin_registry,
)
from cmk.gui.valuespec import Dictionary, TextInput


def _strip(cn, chars):
    """Return the CN without the given characters, lowercased for matching."""
    return "".join(c for c in cn if c not in chars).lower()


def _candidate_cns(conn, cg_by_key, chars):
    """Return {ldap_cn: contact_group} for all LDAP groups matching a contact group."""
    cache_key = ("strip_cn_candidates", chars)
    if cache_key not in conn._group_search_cache:
        found = {}
        for _dn, obj in conn._ldap_search(
            conn.get_group_dn(),
            conn._ldap_filter("groups"),
            ["cn"],
            conn._config["group_scope"],
        ):
            for cn in obj.get("cn", []):
                if (cg := cg_by_key.get(_strip(cn, chars))) is not None:
                    found[cn] = cg
        conn._group_search_cache[cache_key] = found
    return conn._group_search_cache[cache_key]


class LDAPAttributePluginGroupsToContactgroupsStrip(LDAPAttributePlugin):
    def __init__(self):
        super().__init__(
            builtin=False,
            ident="groups_to_contactgroups_strip",
            title="Contact group membership (strip characters from CN)",
            help_text=(
                "Adds the user to existing contact groups based on the group memberships in LDAP. "
                "The name of the contact group must match the common name (cn) of the LDAP group "
                "after the configured characters have been removed, compared case-insensitively. "
                "Use this instead of the builtin plug-in when LDAP group names contain characters "
                "that are not allowed in contact group names, like '$'."
            ),
        )

    def lock_attributes(self, _params):
        return ["contactgroups"]

    def needed_attributes(self, _connection, _params):
        return []

    def sync_func(self, connection, params, user_id, ldap_user, _user, _user_attributes):
        chars = params.get("strip_chars") or "$"
        cg_by_key = {cg.lower(): cg for cg in load_contact_group_information()}
        user_cmp_val = _get_group_member_cmp_val(connection, user_id, ldap_user)

        connections = {connection}
        for connection_id in params.get("other_connections", []):
            if c := get_connection(connection_id):
                connections.add(c)

        contactgroups = set()
        for conn in connections:
            candidates = _candidate_cns(conn, cg_by_key, chars)
            if not candidates:
                continue
            groups = conn._get_group_memberships(
                sorted(candidates), nested=params.get("nested", False)
            )
            for group in groups.values():
                if user_cmp_val in group["members"] and group["cn"] in candidates:
                    contactgroups.add(candidates[group["cn"]])

        return {"contactgroups": sorted(contactgroups)}

    def parameters(self, _connection):
        return Dictionary(
            title=self.title,
            help=self.help,
            elements=[
                (
                    "strip_chars",
                    TextInput(
                        title="Characters to remove from the LDAP group CN",
                        help="Every one of these characters is removed from the CN before "
                        "it is compared with the contact group names.",
                        default_value="$",
                        size=10,
                    ),
                ),
                *_group_membership_parameters(),
            ],
        )


ldap_attribute_plugin_registry.register(LDAPAttributePluginGroupsToContactgroupsStrip())
