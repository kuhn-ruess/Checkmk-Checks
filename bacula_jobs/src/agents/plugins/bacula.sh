#!/bin/sh
echo "<<<bacula_jobs:sep(9)>>>"
/usr/bin/mysql --defaults-file=/root/.my.cnf bacula -B  -e "Select JobId, Name, JobStatus, EndTime FROM Job WHERE EndTime BETWEEN CURDATE() - INTERVAL 30 DAY AND CURDATE();"

