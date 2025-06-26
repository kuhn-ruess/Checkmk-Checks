#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.graphing.v1.metrics import Metric, Title, Color, Unit, DecimalNotation, StrictPrecision

UNIT_NUMBER = Unit(DecimalNotation(""), StrictPrecision(3))

metric_mysql_status_aborted_clients = Metric(
    name = "mysql_status_aborted_clients",
    title = Title("Aborted clients"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)
metric_mysql_status_aborted_connects = Metric(
    name = "mysql_status_aborted_connects",
    title = Title("Aborted connects"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)

metric_mysql_status_bytes_received = Metric(
    name = "mysql_status_bytes_received",
    title = Title("Bytes received"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)
metric_mysql_status_bytes_sent = Metric(
    name = "mysql_status_bytes_sent",
    title = Title("Bytes sent"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)

metric_mysql_status_connections = Metric(
    name = "mysql_status_connections",
    title = Title("Connections"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)

metric_mysql_status_created_tmp_disk_tables = Metric(
    name = "mysql_status_created_tmp_disk_tables",
    title = Title("Created tmp disk tables"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)
metric_mysql_status_created_tmp_files = Metric(
    name = "mysql_status_created_tmp_files",
    title = Title("Created tmp files"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)
metric_mysql_status_created_tmp_tables = Metric(
    name = "mysql_status_created_tmp_tables",
    title = Title("Created tmp tables"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)

metric_mysql_status_innodb_buffer_pool_read_requests = Metric(
    name = "mysql_status_innodb_buffer_pool_read_requests",
    title = Title("Innodb buffer pool read requests"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)
metric_mysql_status_innodb_buffer_pool_reads = Metric(
    name = "mysql_status_innodb_buffer_pool_reads",
    title = Title("Innodb buffer pool reads"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)
metric_mysql_status_innodb_buffer_pool_write_requests = Metric(
    name = "mysql_status_innodb_buffer_pool_write_requests",
    title = Title("Innodb buffer pool write requests"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)
metric_mysql_status_innodb_log_waits = Metric(
    name = "mysql_status_innodb_log_waits",
    title = Title("Innodb log waits"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)
metric_mysql_status_innodb_os_log_written = Metric(
    name = "mysql_status_innodb_os_log_written",
    title = Title("Innodb os log written"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)
metric_mysql_status_innodb_row_lock_time = Metric(
    name = "mysql_status_innodb_row_lock_time",
    title = Title("Innodb row lock time"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)
metric_mysql_status_innodb_row_lock_waits = Metric(
    name = "mysql_status_innodb_row_lock_waits",
    title = Title("Innodb row lock waits"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)
metric_mysql_status_innodb_buffer_pool_pages_free = Metric(
    name = "mysql_status_innodb_buffer_pool_pages_free",
    title = Title("Innodb buffer pool pages free"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)

metric_mysql_status_key_read_requests = Metric(
    name = "mysql_status_key_read_requests",
    title = Title("Key read requests"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)
metric_mysql_status_key_reads = Metric(
    name = "mysql_status_key_reads",
    title = Title("Key reads"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)
metric_mysql_status_key_write_requests = Metric(
    name = "mysql_status_key_write_requests",
    title = Title("Key write requests"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)
metric_mysql_status_key_writes = Metric(
    name = "mysql_status_key_writes",
    title = Title("Key writes"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)
metric_mysql_status_key_blocks_unused = Metric(
    name = "mysql_status_key_blocks_unused",
    title = Title("Key blocks unused"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)

metric_mysql_status_qcache_hits = Metric(
    name = "mysql_status_qcache_hits",
    title = Title("Qcache hits"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)
metric_mysql_status_qcache_inserts = Metric(
    name = "mysql_status_qcache_inserts",
    title = Title("Qcache inserts"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)
metric_mysql_status_qcache_low_mem_prunes = Metric(
    name = "mysql_status_qcache_low_mem_prunes",
    title = Title("Qcache low mem prunes"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)
metric_mysql_status_qcache_lowmem_prunes = Metric(
    name = "mysql_status_qcache_lowmem_prunes",
    title = Title("Qcache lowmem prunes"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)
metric_mysql_status_qcache_not_cached = Metric(
    name = "mysql_status_qcache_not_cached",
    title = Title("Qcache not cached"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)
metric_mysql_status_qcache_free_memory = Metric(
    name = "mysql_status_qcache_free_memory",
    title = Title("Qcache free memory"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)
metric_mysql_status_qcache_free_blocks = Metric(
    name = "mysql_status_qcache_free_blocks",
    title = Title("Qcache free blocks"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)

metric_mysql_status_queries = Metric(
    name = "mysql_status_queries",
    title = Title("Queries"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)

metric_mysql_status_questions = Metric(
    name = "mysql_status_questions",
    title = Title("Questions"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)

metric_mysql_status_select_full_join = Metric(
    name = "mysql_status_select_full_join",
    title = Title("Select full join"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)
metric_mysql_status_select_range_check = Metric(
    name = "mysql_status_select_range_check",
    title = Title("Select range check"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)

metric_mysql_status_slave_retried_transactions = Metric(
    name = "mysql_status_slave_retried_transactions",
    title = Title("Slave retried transactions"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)
metric_mysql_status_slow_launch_threads = Metric(
    name = "mysql_status_slow_launch_threads",
    title = Title("Slow launch threads"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)
metric_mysql_status_slow_queries = Metric(
    name = "mysql_status_slow_queries",
    title = Title("Slow queries"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)

metric_mysql_status_sort_merge_passes = Metric(
    name = "mysql_status_sort_merge_passes",
    title = Title("Sort merge passes"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)

metric_mysql_status_table_locks_waited = Metric(
    name = "mysql_status_table_locks_waited",
    title = Title("Table locks waited"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)

metric_mysql_status_threads_cached = Metric(
    name = "mysql_status_threads_cached",
    title = Title("Threads cached"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)

metric_mysql_status_open_tables = Metric(
    name = "mysql_status_open_tables",
    title = Title("Open tables"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)
metric_mysql_status_open_files = Metric(
    name = "mysql_status_open_files",
    title = Title("Open files"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)

from cmk.graphing.v1.perfometers import FocusRange, Open, Perfometer

perfometer_mysql_status_aborted_clients = Perfometer(
    name = "mysql_status_aborted_clients",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_aborted_clients"],
)
perfometer_mysql_status_aborted_connects = Perfometer(
    name = "mysql_status_aborted_connects",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_aborted_connects"],
)

perfometer_mysql_status_bytes_received = Perfometer(
    name = "mysql_status_bytes_received",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_bytes_received"],
)
perfometer_mysql_status_bytes_sent = Perfometer(
    name = "mysql_status_bytes_sent",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_bytes_sent"],
)

perfometer_mysql_status_connections = Perfometer(
    name = "mysql_status_connections",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_connections"],
)

perfometer_mysql_status_created_tmp_disk_tables = Perfometer(
    name = "mysql_status_created_tmp_disk_tables",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_created_tmp_disk_tables"],
)
perfometer_mysql_status_created_tmp_files = Perfometer(
    name = "mysql_status_created_tmp_files",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_created_tmp_files"],
)
perfometer_mysql_status_created_tmp_tables = Perfometer(
    name = "mysql_status_created_tmp_tables",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_created_tmp_tables"],
)

perfometer_mysql_status_innodb_buffer_pool_read_requests = Perfometer(
    name = "mysql_status_innodb_buffer_pool_read_requests",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_innodb_buffer_pool_read_requests"],
)
perfometer_mysql_status_innodb_buffer_pool_reads = Perfometer(
    name = "mysql_status_innodb_buffer_pool_reads",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_innodb_buffer_pool_reads"],
)
perfometer_mysql_status_innodb_buffer_pool_write_requests = Perfometer(
    name = "mysql_status_innodb_buffer_pool_write_requests",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_innodb_buffer_pool_write_requests"],
)
perfometer_mysql_status_innodb_log_waits = Perfometer(
    name = "mysql_status_innodb_log_waits",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_innodb_log_waits"],
)
perfometer_mysql_status_innodb_os_log_written = Perfometer(
    name = "mysql_status_innodb_os_log_written",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_innodb_os_log_written"],
)
perfometer_mysql_status_innodb_row_lock_time = Perfometer(
    name = "mysql_status_innodb_row_lock_time",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_innodb_row_lock_time"],
)
perfometer_mysql_status_innodb_row_lock_waits = Perfometer(
    name = "mysql_status_innodb_row_lock_waits",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_innodb_row_lock_waits"],
)
perfometer_mysql_status_innodb_buffer_pool_pages_free = Perfometer(
    name = "mysql_status_innodb_buffer_pool_pages_free",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_innodb_buffer_pool_pages_free"],
)

perfometer_mysql_status_key_read_requests = Perfometer(
    name = "mysql_status_key_read_requests",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_key_read_requests"],
)
perfometer_mysql_status_key_reads = Perfometer(
    name = "mysql_status_key_reads",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_key_reads"],
)
perfometer_mysql_status_key_write_requests = Perfometer(
    name = "mysql_status_key_write_requests",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_key_write_requests"],
)
perfometer_mysql_status_key_writes = Perfometer(
    name = "mysql_status_key_writes",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_key_writes"],
)
perfometer_mysql_status_key_blocks_unused = Perfometer(
    name = "mysql_status_key_blocks_unused",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_key_blocks_unused"],
)

perfometer_mysql_status_qcache_hits = Perfometer(
    name = "mysql_status_qcache_hits",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_qcache_hits"],
)
perfometer_mysql_status_qcache_inserts = Perfometer(
    name = "mysql_status_qcache_inserts",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_qcache_inserts"],
)
perfometer_mysql_status_qcache_low_mem_prunes = Perfometer(
    name = "mysql_status_qcache_low_mem_prunes",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_qcache_low_mem_prunes"],
)
perfometer_mysql_status_qcache_lowmem_prunes = Perfometer(
    name = "mysql_status_qcache_lowmem_prunes",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_qcache_lowmem_prunes"],
)
perfometer_mysql_status_qcache_not_cached = Perfometer(
    name = "mysql_status_qcache_not_cached",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_qcache_not_cached"],
)
perfometer_mysql_status_qcache_free_memory = Perfometer(
    name = "mysql_status_qcache_free_memory",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_qcache_free_memory"],
)
perfometer_mysql_status_qcache_free_blocks = Perfometer(
    name = "mysql_status_qcache_free_blocks",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_qcache_free_blocks"],
)

perfometer_mysql_status_queries = Perfometer(
    name = "mysql_status_queries",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_queries"],
)

perfometer_mysql_status_questions = Perfometer(
    name = "mysql_status_questions",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_questions"],
)

perfometer_mysql_status_select_full_join = Perfometer(
    name = "mysql_status_select_full_join",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_select_full_join"],
)
perfometer_mysql_status_select_range_check = Perfometer(
    name = "mysql_status_select_range_check",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_select_range_check"],
)

perfometer_mysql_status_slave_retried_transactions = Perfometer(
    name = "mysql_status_slave_retried_transactions",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_slave_retried_transactions"],
)
perfometer_mysql_status_slow_launch_threads = Perfometer(
    name = "mysql_status_slow_launch_threads",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_slow_launch_threads"],
)

perfometer_mysql_status_slow_queries = Perfometer(
    name = "mysql_status_slow_queries",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_slow_queries"],
)

perfometer_mysql_status_sort_merge_passes = Perfometer(
    name = "mysql_status_sort_merge_passes",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_sort_merge_passes"],
)

perfometer_mysql_status_table_locks_waited = Perfometer(
    name = "mysql_status_table_locks_waited",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_table_locks_waited"],
)

perfometer_mysql_status_threads_cached = Perfometer(
    name = "mysql_status_threads_cached",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_threads_cached"],
)
perfometer_mysql_status_open_tables = Perfometer(
    name = "mysql_status_open_tables",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_open_tables"],
)
perfometer_mysql_status_open_files = Perfometer(
    name = "mysql_status_open_files",
    focus_range = FocusRange(Open(0), Open(40)),
    segments = ["mysql_status_open_files"],
)
