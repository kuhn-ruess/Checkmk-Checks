#!/bin/bash
echo "<<<inventorize_df:sep(59)>>>"
for MP in $(df -P -T local| grep -viE 'Filesystem' | grep -viE '^tmpfs' | awk '{ print $NF }')
do
    USER="`ls -od ${MP} |grep ^d |awk '{print $3}'`"
    PWENTRY="`cat /etc/passwd |grep \"^${USER}:\"`"

    MAIL=`echo ${PWENTRY} |grep "^${USER}:" | cut -d ";" -f 3`
    OWNER=`echo ${PWENTRY} |grep "^${USER}:" | cut -d ";" -f 2`

    FOUND=NO
    echo ${MAIL} | grep -iE '.*@.*' 1>/dev/null 2>&1 && FOUND=YES
    if [ "${FOUND}" = "YES" ]
    then
        echo "${MP};${USER};${OWNER};${MAIL}"
    fi
done
