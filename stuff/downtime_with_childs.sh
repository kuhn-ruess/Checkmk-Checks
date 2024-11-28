#!/bin/bash
DURATION=2
HOSTNAME=father
START_TIME=`date +%Y-%m-%dT%H:%M:%S%:z`
END_TIME=`date -d "now + $DURATION min" +%Y-%m-%dT%H:%M:%S%:z`
 
echo "Start Time: $START_TIME"
echo "End Time: $END_TIME"
echo "Target Hostname: $HOSTNAME"

#curl --request POST \
#  --header "Authorization: Bearer cmkadmin Test123\$" \
#  --header "Accept: application/json" \
#  --header "Content-Type: application/json" \
#  --data '{
#    "comment": "My DT TEST",
#    "downtime_type": "host_by_query",
#    "query": {
#      "op": "or",
#      "expr": [
#        {"op": ">=", "left": "parents", "right": "'"${HOSTNAME}"'"},
#        {"op": "=", "left": "name", "right": "'"${HOSTNAME}"'"}
#      ]
#    },
#    "recur": "fixed",
#    "start_time": "'"${START_TIME}"'",
#    "end_time": "'"${END_TIME}"'"
#  }' \
#  http://dev:5002/cmk/check_mk/api/1.0/domain-types/downtime/collections/host


curl --request POST --header "Authorization: Bearer cmkadmin Test123\$" --header "Accept: application/json" --header "Content-Type: application/json" --data '{"comment":"My DT TEST","downtime_type":"host_by_query","query":{"op":"or","expr":[{"op":">=","left":"parents","right":"'"${HOSTNAME}"'"},{"op":"=","left":"name","right":"'"${HOSTNAME}"'"}]},"recur":"fixed","start_time":"'"${START_TIME}"'","end_time":"'"${END_TIME}"'"}' 'http://dev:5002/cmk/check_mk/api/1.0/domain-types/downtime/collections/host'
