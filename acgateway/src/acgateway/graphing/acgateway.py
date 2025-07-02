#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.graphing.v1.metrics import Metric, Title, Color, Unit, DecimalNotation, StrictPrecision

metric_info_acpgateway_active_alarms = Metric(
    name = "active_alarms",
    title = Title("Active Alarms"),
    unit = Unit(DecimalNotation(""), StrictPrecision(1)),
    color = Color.GREEN,
)
metric_info_acpgateway_archived_alarms = Metric(
    name ="archived_alarms",
    title = Title("Archived Alarms"),
    unit = Unit(DecimalNotation(""), StrictPrecision(1)),
    color = Color.RED,
)

metric_info_acpgateway_active_calls = Metric(
    name = "active_calls",
    title = Title("Active Calls"),
    unit = Unit(DecimalNotation(""), StrictPrecision(1)),
    color = Color.RED,
)
metric_info_acpgateway_calls_per_sec = Metric(
    name = "calls_per_sec",
    title = Title("Calls per Second"),
    unit = Unit(DecimalNotation("1/s"), StrictPrecision(1)),
    color = Color.BLUE,
)
metric_info_acpgateway_average_success_ratio = Metric(
    name = "average_success_ratio",
    title = Title("Average Success Ratio"),
    unit = Unit(DecimalNotation("%"), StrictPrecision(1)),
    color = Color.GREEN,
)
metric_info_acpgateway_average_call_duration = Metric(
    name = "average_call_duration",
    title = Title("Average Call Duration"),
    unit = Unit(DecimalNotation("s"), StrictPrecision(1)),
    color = Color.ORANGE,
)

metric_info_acpgateway_tel2ip_sip_calls_attempted = Metric(
    name = "tel2ip_sip_calls_attempted",
    title = Title("Number of Attempted SIP/H323 calls"),
    unit = Unit(DecimalNotation("1/s"), StrictPrecision(1)),
    color = Color.RED,
)
metric_info_acpgateway_tel2ip_sip_calls_established = Metric(
    name = "tel2ip_sip_calls_established",
    title = Title("Number of established (connected and voice activated) SIP/H323 calls"),
    unit = Unit(DecimalNotation("1/s"), StrictPrecision(1)),
    color = Color.RED,
)
metric_info_acpgateway_tel2ip_sip_destination_busy = Metric(
    name = "tel2ip_sip_destination_busy",
    title = Title("Number of Destination Busy SIP/H323 calls"),
    unit = Unit(DecimalNotation("1/s"), StrictPrecision(1)),
    color = Color.RED,
)
metric_info_acpgateway_tel2ip_sip_no_answer = Metric(
    name = "tel2ip_sip_no_answer",
    title = Title("Number of No Answer SIP/H323 calls"),
    unit = Unit(DecimalNotation("1/s"), StrictPrecision(1)),
    color = Color.RED,
)
metric_info_acpgateway_tel2ip_sip_no_route = Metric(
    name = "tel2ip_sip_no_route",
    title = Title("Number of No Route SIP/H323 calls. Most likely to be due to wrong number"),
    unit = Unit(DecimalNotation("1/s"), StrictPrecision(1)),
    color = Color.RED,
)
metric_info_acpgateway_tel2ip_sip_no_capability = Metric(
    name = "tel2ip_sip_no_capability",
    title = Title("Number of No capability match between peers on SIP/H323 calls"),
    unit = Unit(DecimalNotation("1/s"), StrictPrecision(1)),
    color = Color.RED,
)
metric_info_acpgateway_tel2ip_sip_failed = Metric(
    name = "tel2ip_sip_failed",
    title = Title("Number of failed SIP/H323 calls"),
    unit = Unit(DecimalNotation("1/s"), StrictPrecision(1)),
    color = Color.RED,
)
metric_info_acpgateway_tel2ip_sip_fax_attempted = Metric(
    name = "tel2ip_sip_fax_attempted",
    title = Title("Number of Attempted SIP/H323 fax calls"),
    unit = Unit(DecimalNotation("1/s"), StrictPrecision(1)),
    color = Color.RED,
)
metric_info_acpgateway_tel2ip_sip_fax_success = Metric(
    name = "tel2ip_sip_fax_success",
    title = Title("Number of SIP/H323 fax success calls"),
    unit = Unit(DecimalNotation("1/s"), StrictPrecision(1)),
    color = Color.RED,
)
metric_info_acpgateway_tel2ip_sip_total_duration = Metric(
    name = "tel2ip_sip_total_duration",
    title = Title("total duration of SIP/H323 calls"),
    unit = Unit(DecimalNotation("s"), StrictPrecision(1)),
    color = Color.RED,
)

metric_info_acpgateway_ip2tel_sip_calls_attempted = Metric(
    name = "ip2tel_sip_calls_attempted",
    title = Title("Number of Attempted SIP/H323 calls"),
    unit = Unit(DecimalNotation("1/s"), StrictPrecision(1)),
    color = Color.RED,
)
metric_info_acpgateway_ip2tel_sip_calls_established = Metric(
    name = "ip2tel_sip_calls_established",
    title = Title("Number of established (connected and voice activated) SIP/H323 calls"),
    unit = Unit(DecimalNotation("1/s"), StrictPrecision(1)),
    color = Color.RED,
)
metric_info_acpgateway_ip2tel_sip_destination_busy = Metric(
    name = "ip2tel_sip_destination_busy",
    title = Title("Number of Destination Busy SIP/H323 calls"),
    unit = Unit(DecimalNotation("1/s"), StrictPrecision(1)),
    color = Color.RED,
)
metric_info_acpgateway_ip2tel_sip_no_answer = Metric(
    name = "ip2tel_sip_no_answer",
    title = Title("Number of No Answer SIP/H323 calls"),
    unit = Unit(DecimalNotation("1/s"), StrictPrecision(1)),
    color = Color.RED,
)
metric_info_acpgateway_ip2tel_sip_no_route = Metric(
    name = "ip2tel_sip_no_route",
    title = Title("Number of No Route SIP/H323 calls. Most likely to be due to wrong number"),
    unit = Unit(DecimalNotation("1/s"), StrictPrecision(1)),
    color = Color.RED,
)
metric_info_acpgateway_ip2tel_sip_no_capability = Metric(
    name = "ip2tel_sip_no_capability",
    title = Title("Number of No capability match between peers on SIP/H323 calls"),
    unit = Unit(DecimalNotation("1/s"), StrictPrecision(1)),
    color = Color.RED,
)
metric_info_acpgateway_ip2tel_sip_failed = Metric(
    name = "ip2tel_sip_failed",
    title = Title("Number of failed SIP/H323 calls"),
    unit = Unit(DecimalNotation("1/s"), StrictPrecision(1)),
    color = Color.RED,
)
metric_info_acpgateway_ip2tel_sip_fax_attempted = Metric(
    name = "ip2tel_sip_fax_attempted",
    title = Title("Number of Attempted SIP/H323 fax calls"),
    unit = Unit(DecimalNotation("1/s"), StrictPrecision(1)),
    color = Color.RED,
)
metric_info_acpgateway_ip2tel_sip_fax_success = Metric(
    name = "ip2tel_sip_fax_success",
    title = Title("Number of SIP/H323 fax success calls"),
    unit = Unit(DecimalNotation("1/s"), StrictPrecision(1)),
    color = Color.RED,
)
metric_info_acpgateway_ip2tel_sip_total_duration = Metric(
    name = "ip2tel_sip_total_duration",
    title = Title("total duration of SIP/H323 calls"),
    unit = Unit(DecimalNotation("s"), StrictPrecision(1)),
    color = Color.RED,
)

metric_info_acgateway_rx_trans = Metric(
    name = "rx_trans",
    title = Title("RX Transactions per Second"),
    unit = Unit(DecimalNotation("s"), StrictPrecision(1)),
    color = Color.BLUE,
)
metric_info_acgateway_tx_trans = Metric(
    name = "tx_trans",
    title = Title("TX Transactions per Second"),
    unit = Unit(DecimalNotation("s"), StrictPrecision(1)),
    color = Color.RED,
)

from cmk.graphing.v1.graphs import Graph, Title

graph_acgateway_tel2ip_sip_statistics = Graph(
    name = "tel2ip_sip_statistics",
    title = Title("tel2ip SIP Statistics"),
    simple_lines = [
        "tel2ip_sip_calls_attempted",
        "tel2ip_sip_calls_established",
        "tel2ip_sip_destination_busy",
        "tel2ip_sip_no_answer",
        "tel2ip_sip_no_route",
        "tel2ip_sip_no_capability",
        "tel2ip_sip_failed",
        "tel2ip_sip_fax_attempted",
        "tel2ip_sip_fax_success"],
)
graph_acgateway_ip2tel_sip_statistics = Graph(
    name = "ip2tel_sip_statistics",
    title = Title("ip2tel SIP Statistics"),
    simple_lines = [
        "ip2tel_sip_calls_attempted",
        "ip2tel_sip_calls_established",
        "ip2tel_sip_destination_busy",
        "ip2tel_sip_no_answer",
        "ip2tel_sip_no_route",
        "ip2tel_sip_no_capability",
        "ip2tel_sip_failed",
        "ip2tel_sip_fax_attempted",
        "ip2tel_sip_fax_success"],
)

graph_acgateway_sip_totals = Graph(
    name = "sip_totals",
    title = Title("SIP Totals"),
    simple_lines = ["tel2ip_sip_total_duration", "ip2tel_sip_total_duration"],
)

graph_acgateway_transactions = Graph(
    name = "acgateway_transactions",
    title = Title("Transactions per Second"),
    simple_lines = [ "rx_trans", "tx_trans" ],
)
