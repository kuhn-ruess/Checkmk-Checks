from cmk.gui.plugins.metrics import perfometer_info
from cmk.gui.plugins.metrics.utils import TB


perfometer_info.append(
    {
        "type": "logarithmic",
        "metric": "quota_used_bytes",
        "half_value": TB,
        "exponent": 2,
    }
)
