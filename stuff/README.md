Files in here:

 * cmk_rrd_rename.py: Migration Helper for RRD Files (Renaming)
 * api.py: Example to connect to the cmk API
 * ec_mkp_rule_packs_to_local.py: Converts Event Console rule packs shipped by an MKP into normal local rule packs
   inside an existing rules.mk, so the MKP can be disabled afterwards. Run as site user (`omd su <site>`),
   `--help` explains every option and the full procedure. Short version:
   * `python3 ec_mkp_rule_packs_to_local.py --list` shows the rule packs in rules.mk, in the enabled MKPs
     and in the stored .mkp files (`~/var/check_mk/packages_local`)
   * `--source` takes a package name from `mkp list` (`--source vendor_ec_rules`), an .mkp file
     (`--source /tmp/vendor_ec_rules-1.0.mkp`), a rule pack directory or a single `<id>.mk`.
     Without `--source`: the packs of all enabled MKPs (`~/etc/check_mk/mkeventd.d/mkp/rule_packs`)
   * `--dry-run` first, then run without it (rules.mk gets a `.bak-<timestamp>` copy), activate the
     Event Console changes, then `mkp disable <package>`
