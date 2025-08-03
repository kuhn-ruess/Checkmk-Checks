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

# Shell version of the waitmax utility, that limits the runtime of
# commands. This version does not conserve the original exit code
# of the command. It is successfull if the command terminated
# in time.
function waitmax
{
   TIMEOUT=${1}0
   SIGNAL=9
   shift

   # Run command in background
   ksh -c "$*" &
   PID=$!

   # Wait for termination within TIMOUT seconds
   while [ $TIMEOUT -gt 0 ]
   do
       TIMEOUT=$((TIMEOUT - 1))
       if [ ! -e /proc/$PID ] ; then
           return 0
       fi
       perl -e "select(undef, undef, undef, 0.1);"
   done

   # Process did not terminate in time. Kill and
   # return with an error
   kill -9 $PID
   return 255
}



# if type waitmax >/dev/null 2>&1
# then
   agent_Vers=$(waitmax 5 /opt/OV/bin/ovdeploy -inv 2>/dev/null | grep -iE 'Operations-agent' | awk '{ print $(NF-2) }')
   agent_HPOvSecCo=$(waitmax 5 /opt/OV/bin/ovdeploy -inv 2>/dev/null | grep -iE 'HPOvSecCo' | awk '{ print $(NF-2) }')
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

