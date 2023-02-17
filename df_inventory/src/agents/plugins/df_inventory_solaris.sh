#!/bin/bash
echo "<<<inventorize_df:sep(59)>>>"
for MP in $(/usr/xpg4/bin/df -lP | grep -vi "Filesystem" |  grep -vi 'tmpfs' | awk '{ print $NF }')
do
    USER="`ls -od ${MP} |grep ^d |awk '{print $3}'`"
    PWENTRY="`cat /etc/passwd |grep \"^${USER}:\"`"

    MAIL=`echo ${PWENTRY} |grep "^${USER}:" | cut -d ";" -f 3`
    OWNER=`echo ${PWENTRY} |grep "^${USER}:" | cut -d ";" -f 2`

    FOUND=NO
    echo ${MAIL} | grep -i '.*@.*' 1>/dev/null 2>&1 && FOUND=YES
    if [ "${FOUND}" = "YES" ]
    then
        echo "${MP};${USER};${OWNER};${MAIL}"
    fi
done
