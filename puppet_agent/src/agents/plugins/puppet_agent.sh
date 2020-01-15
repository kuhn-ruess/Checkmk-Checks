#!/bin/bash

SUMMARY_1="/var/lib/puppet/state/last_run_summary.yaml"
SUMMARY_2="/opt/puppetlabs/puppet/cache/state/last_run_summary.yaml"

if [ -f $SUMMARY_1 ]; then
    LASTRUN=$SUMMARY_1
else
    LASTRUN=$SUMMARY_2
fi

if [ -e "${LASTRUN}" ]; then
  OUT="$(cat ${LASTRUN} | sed 's/[[:space:]]\{2,\}//g')"
  echo "<<<puppet_agent>>>"
  echo "${OUT}" | grep 'last_run'
  echo "${OUT}" | grep -A8 '^resources: *$' | sed 's/^/resources_/g'
  echo "${OUT}" | grep -A3 '^events: *$' | sed 's/^/events_/g'
fi
