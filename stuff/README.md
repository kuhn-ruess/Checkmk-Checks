Files in here:

 * cmk_rrd_rename.py: Migration Helper for RRD Files (Renaming)
 * api.py: Example to connect to the cmk API
 * ec_mkp_rule_packs_to_local.py: Converts Event Console rule packs shipped by an MKP into normal local rule packs
   inside an existing rules.mk (backup + dry run, see --help). Run as site user, e.g.
   `python3 ec_mkp_rule_packs_to_local.py --dry-run` or `-s vendor.mkp -r ~/etc/check_mk/mkeventd.d/wato/rules.mk`
