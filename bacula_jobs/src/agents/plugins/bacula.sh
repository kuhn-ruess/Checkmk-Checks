#!/bin/sh

# 2019 robertoschwald

# Get Jobs of last 30 days in tab delimited form
# Fields: JobId JobName Status Date

echo "<<<bacula_jobs:sep(9)>>>"
# Get job stats:
# 1. The needed fields in given order (JobId,JobName,Date,Status)
# 2. Remove first line
# 3. Remove space at line beginnings
# 4. Squeeze duplicate spaces into one
# 5. Remove commas (JobIds are printed with commas)
JOBSTATS=`echo "list jobs days=30" | bconsole | cut -s -d'|' --output-delimiter=$'\t' -f 2,3,5,10 | tail -n +2 | sed 's/^ //g' | sed 's/  */ /g' | tr -d ','`

# Re-Order fields tab-delimited. Ensures DateTime has a space between date and time.
JOBSTATS=`echo "$JOBSTATS" | awk 'BEGIN {OFS="\t"}{printf "%s\t%s\t%s\t",$1,$2,$5}{OFS=" "}{print $3,$4}'`

# Output
echo "$JOBSTATS"
