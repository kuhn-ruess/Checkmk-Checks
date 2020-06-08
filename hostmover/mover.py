#!/usr/bin/env python3
"""
Host Mover
"""
# pylint: disable=invalid-name
import getopt
import sys
import os
from shutil import copytree, copyfile, rmtree

def usage():
    """
    Print Usage
    """
    sys.stdout.write("""Usage: mover -s SOURCE_SITE -t TARGET_SITE -H HOSTNAME

This program moves hosts in between sites.

Options:

  -v, --verbose     Verbose mode
  -s, --source      Source OMD Site
  -t, --target      Target OMD Site
  -H, --host        Hostname
  -L, --logfiles    Handle Logfiles
  -P, --perfdata    Handle Perfdata
  -A, --autochecks  Handle Autocheck files
  -a, --all         Copy all Data
  -u, --uid         UID for chown
  -g, --gid         GID for chown

""")


short_options = 'vs:t:hH:aLPu:g:A'
long_options = [
    'verbose', 'source=', 'target=', 'host=', 'help', 'all',
    'logfiles', 'perfdata', 'uid=', 'guid=', 'autochecks',
]

opt_verbose = False
opt_source = ""
opt_target = ""
opt_host = ""
opt_logfiles = False
opt_perfdata = False
opt_omd_base = '/opt/omd/sites/'
opt_uid = 0
opt_gid = 0
opt_autochecks = False

try:
    opts, args = getopt.getopt(sys.argv[1:], short_options, long_options)
except getopt.GetoptError as err:
    sys.stderr.write("%s\n\n" % err)
    usage()
    sys.exit(1)

for o, a in opts:
    if o in ['-h', '--help']:
        usage()
        sys.exit(0)

    elif o in ['-v', '--verbose']:
        opt_verbose = True
    elif o in ['-s', '--source']:
        opt_source = a
    elif o in ['-t', '--target']:
        opt_target = a
    elif o in ['-H', '--host']:
        opt_host = a
    elif o in ['-a', '--all']:
        opt_logfiles = True
        opt_perfdata = True
        opt_autochecks = True
    elif o in ['-L', '--logfiles']:
        opt_logfiles = True
    elif o in ['-P', '--perfdata']:
        opt_perfdata = True
    elif o in ['-A', '--autochecks']:
        opt_autochecks = True
    elif o in ['-g', '--gid']:
        opt_gid = int(a)
    elif o in ['-u', '--uid']:
        opt_uid = int(a)

if not opt_host or not opt_target or not opt_source:
    usage()
    sys.exit(1)

# Helpers
def verbose(msg):
    """
    Print Verbose
    """
    if opt_verbose:
        sys.stdout.write(msg + "\n")

def find_loglines(path, searchhost):
    """
    Find all to Host related lines for a host
    """
    try:
        logfiles = list(os.walk(path))[0][2]
    except IndexError:
        sys.stderr.write("Path not found or empty: {}".format(path))
    found_lines = {}
    verbose("+++Start Parsing+++")
    for logfile in logfiles:
        with open(path+logfile) as data:
            verbose("... Parse: " + path+logfile)
            for line in data.readlines():
                splited = line.split()
                if splited[1] not in ["INITAL", "SERVICE", "HOST"]:
                    continue

                message = line.split(":")[1].strip().split(';')
                if splited[2].startswith('NOTIFICATION'):
                    hostname = message[1]
                else:
                    hostname = message[0]

                if searchhost != hostname:
                    continue

                found_lines.setdefault(logfile, [])
                found_lines[logfile].append(line)
    return found_lines


def write_logfiles(path, hostname, config):
    """
    Write new logfiles
    """
    verbose("+++Start Writing+++")
    for logfile, lines in config.items():
        outfilename = logfile+'-'+hostname
        if logfile.endswith('-'+hostname):
            outfilename = logfile
        with open(path+outfilename, "w+") as outfile:
            verbose("... Write "+path+outfilename)
            for line in lines:
                outfile.write(line)

        if opt_uid and opt_gid:
            os.chown(path+outfilename, opt_uid, opt_gid)

source_site = opt_omd_base+opt_source+"/"
target_site = opt_omd_base+opt_target+"/"

if opt_logfiles:
    verbose("Start Logfiles")
    logfile_path = 'var/check_mk/core/archive/'

    logfile_data = find_loglines(source_site+logfile_path, opt_host)
    write_logfiles(target_site+logfile_path, opt_host, logfile_data)

if opt_perfdata:
    verbose("Start Perfdata")
    perfdata_path = 'var/check_mk/rrd'
    perf_source = source_site+perfdata_path+"/"+opt_host
    perf_target = target_site+perfdata_path+"/"+opt_host
    rmtree(perf_target)
    copytree(perf_source, perf_target)
    if opt_uid and opt_gid:
        verbose("... Set UID")
        os.chown(perf_target, opt_uid, opt_gid)
    verbose("... Copied {} to {}".format(perf_source, perf_target))

if opt_autochecks:
    verbose("Start Autochecks")
    autocheck_path = 'var/check_mk/autochecks'
    autochecks_source = source_site+autocheck_path+"/"+opt_host+".mk"
    autochecks_target = target_site+autocheck_path+"/"+opt_host+".mk"
    copyfile(autochecks_source, autochecks_target)
    if opt_uid and opt_gid:
        verbose("... Set UID")
        os.chown(autochecks_target, opt_uid, opt_gid)
    verbose("... Copied {} to {}".format(autochecks_source, autochecks_target))
