#!/bin/sh
echo "<<<bacula_jobs:sep(9)>>>"
echo "Select JobId, Name, JobStatus, EndTime FROM Job WHERE EndTime BETWEEN NOW() - interval '30 days' AND NOW();" | sudo -u postgres psql --tuples-only -AF $'\t'  bareos
