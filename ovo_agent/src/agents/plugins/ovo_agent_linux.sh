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

if type waitmax >/dev/null 2>&1
then
   agent_Vers=$(waitmax -s 9 2 /opt/OV/bin/ovdeploy -inv 2>/dev/null | grep -iE 'Operations-agent' | awk '{ print $(NF-2) }')
   agent_HPOvSecCo=$(waitmax -s 9 2 /opt/OV/bin/ovdeploy -inv 2>/dev/null | grep -iE 'HPOvSecCo' | awk '{ print $(NF-2) }')
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
fi

