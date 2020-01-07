#!/bin/bash

LASTRUN="/var/lib/puppet/state/last_run_summary.yaml"
#LASTRUN="/opt/puppetlabs/puppet/cache/state/last_run_summary.yaml"

if [ -e "${LASTRUN}" ]; then
  OUT="$(cat ${LASTRUN} | sed 's/[[:space:]]\{2,\}//g')"
  echo "<<<puppet_agent>>>"
  echo "${OUT}" | grep 'last_run'
  echo "${OUT}" | grep -A8 '^resources: *$' | sed 's/^/resources_/g'
  echo "${OUT}" | grep -A3 '^events: *$' | sed 's/^/events_/g'
fi
