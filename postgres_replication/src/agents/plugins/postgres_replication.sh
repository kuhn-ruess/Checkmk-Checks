psql_version=$(su - postgres -c 'psql -V' | cut -d " " -f3)
if [ ${psql_version%\.*} -eq 9 ]; then
    DIFF=pg_xlog_location_diff
    LAST_LOC=pg_last_xlog_receive_location
    CURRENT_LOC=pg_current_xlog_location
else
    DIFF=pg_wal_lsn_diff
    LAST_LOC=pg_last_wal_receive_lsn
    CURRENT_LOC=pg_current_wal_lsn
fi

echo "<<<postgres_replication>>>"
echo "WITH slots AS (SELECT slot_name, slot_type, coalesce(restart_lsn, '0/0'::pg_lsn) AS slot_lsn, coalesce(${DIFF}(coalesce(${LAST_LOC}(), ${CURRENT_LOC}()), restart_lsn),0) AS delta, active FROM pg_replication_slots) SELECT *, pg_size_pretty(delta) AS delta_pretty FROM slots; " | su - postgres -c "psql -d postgres -A -t -F' '"
