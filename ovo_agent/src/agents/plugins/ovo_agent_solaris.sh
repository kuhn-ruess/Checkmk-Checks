#!/bin/bash


##### $meins =  get-cluster $env:computername
##### write-host "<<<labels:Sep(o)>>>"
##### Write-Host "{""win_clustername"":""$meins""}"


## [root@vlomlop002 ~]# /opt/OV/bin/ovdeploy -inv | grep -iE 'Operations-agent' | awk '{ print $(NF-2) }'
## 12.12.010
## [root@vlomlop002 ~]# /opt/OV/bin/ovdeploy -inv | grep -iE 'HPOvSecCo' | awk '{ print $(NF-2) }'
## 12.12.010
## [root@vlomlop002 ~]#
###+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

##### agent_Vers="`/opt/OV/bin/ovdeploy -inv | grep -iE 'Operations-agent' | awk '{ print $(NF-2) }'`"
##### agent_HPOvSecCo="`/opt/OV/bin/ovdeploy -inv | grep -iE 'HPOvSecCo' | awk '{ print $(NF-2) }'`"
##### 
##### echo "<<<labels:sep(0)>>>"
##### echo "{\"HP_OVO_OA_Vers_gen\": \"${agent_Vers}\"}"
##### echo "{\"HP_OVO_OA_Vers_HPOvSecCo\": \"${agent_HPOvSecCo}\"}"
##### 
###+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

function waitmax
{
#                # DEBUG=""
#                DEBUG="# ####"
#                ${DEBUG}set -vx

   if [ -z "${1}" ]; then
       TIMEOUT=70
   else
       TIMEOUT=${1}0
   fi
#                ${DEBUG}echo "TIMEOUT = ${TIMEOUT}"
   SIGNAL=9
   shift

   # Run command in background
   /usr/bin/ksh -c "$*" &
   PID=$!

   # Wait for termination within TIMOUT seconds
   while [ $TIMEOUT -gt 0 ]
   do
#                        ${DEBUG}ps -ef |grep -v grep | grep $PID
       TIMEOUT=$((TIMEOUT - 1))
#                        ${DEBUG}echo $TIMEOUT
       PROC_ANZ=`ps -ef |grep -v grep | grep $PID | wc -l | awk '{ print $NF }'`
       if [ ${PROC_ANZ} -le 0 ] ; then
#                        ${DEBUG}ps -ef |grep -v grep | grep $PID
#                        ${DEBUG}echo "FERTIG ist "
           return 0
       fi
#                        ${DEBUG}echo $TIMEOUT
       perl -e "select(undef, undef, undef, 0.1);"
   done

   # Process did not terminate in time. Kill and
   # return with an error
#        ${DEBUG}echo "Process did not terminate in time. Kill and return with an error"
   kill -9 $PID
   return 255
}




# if type waitmax >/dev/null 2>&1
# then
   agent_Vers=$(waitmax 6 UNIX95=yes /opt/OV/bin/ovdeploy -inv 2>/dev/null | egrep -i 'Operations-agent' | awk '{ print $(NF-2) }')
   agent_HPOvSecCo=$(waitmax 6 UNIX95=yes /opt/OV/bin/ovdeploy -inv 2>/dev/null | egrep -i 'HPOvSecCo' | awk '{ print $(NF-2) }')
   if [ x"$agent_Vers" == x ] ; then
   echo "<<<labels:sep(0)>>>"
   echo "{\"HP_OVO_Vers_Detect\": \"in_Place\"}"
   echo "{\"HP_OVO_OA_Installed\": \"No\"}"
   else
   echo "<<<labels:sep(0)>>>"
   echo "{\"HP_OVO_Vers_Detect\": \"in_Place\"}"
   echo "{\"HP_OVO_OA_Installed\": \"Yes\"}"
   echo "{\"HP_OVO_OA_Vers_gen\": \"${agent_Vers}\"}"
   echo "{\"HP_OVO_OA_Vers_HPOvSecCo\": \"${agent_HPOvSecCo}\"}"
   fi
# fi


# echo "WAS JETZT" 
#   SLEEPT=$(waitmax 6 sleep 33 ; echo $?)
#   agent_Vers=$(waitmax 6 UNIX95=yes /opt/OV/bin/ovdeploy -inv 2>/dev/null | egrep -i 'Operations-agent' | awk '{ print $(NF-2) }')
#   agent_HPOvSecCo=$(waitmax 6 UNIX95=yes /opt/OV/bin/ovdeploy -inv 2>/dev/null | egrep -i 'HPOvSecCo' | awk '{ print $(NF-2) }')
#
# echo "Fertig"
