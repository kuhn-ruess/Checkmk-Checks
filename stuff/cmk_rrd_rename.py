#!/usr/bin/env python3
"""
Rename for Checkmk RRD Files
"""
import sys
import os

def main(hostname, old_sn, new_sn, path):
    old_path = "{}/{}/{}".format(path, hostname, old_sn)
    new_path = "{}/{}/{}".format(path, hostname, new_sn)

    for ftype in ['rrd', 'info']:
        os.rename(old_path+"."+ftype, new_path+"."+ftype)
    new_data = open(new_path+".info").read().replace("SERVICE "+old_sn, "SERVICE "+new_sn)
    open(new_path+".info", "w").write(new_data)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("""
        Usage:
        ./cmk_rrd_rename.py HOSTNAME OLD_SVN NEW_SVN
        optional: Path for rrd dir, otherwise var/check_mk/rrd/ is used
        """)
        sys.exit(1)
    try:
        path = sys.argv[4]
    except IndexError:
        path = 'var/check_mk/rrd/'


    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3], path))


