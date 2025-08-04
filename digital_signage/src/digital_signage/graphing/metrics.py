#!/usr/bin/env python3
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.graphing.v1.metrics import Metric, Title, Color, Unit, DecimalNotation, IECNotation
from cmk.graphing.v1.perfometers import Perfometer, FocusRange, Closed, Open, Bidirectional

UNIT_NUMBER = Unit(DecimalNotation(""))


metric_gpu_load_3d = Metric(
    name = "gpu_load_3d",
    title = Title("GPU Load 3D"),
    unit = UNIT_NUMBER,
    color = Color.BLUE,
)

metric_gpu_load_copy = Metric(
    name = "gpu_load_copy",
    title = Title("GPU Load Copy"),
    unit = UNIT_NUMBER,
    color = Color.LIGHT_BLUE,
)

metric_gpu_load_videodecode = Metric(
    name = "gpu_load_videodecode",
    title = Title("GPU Load Videodecode"),
    unit = UNIT_NUMBER,
    color = Color.YELLOW,
)

metric_gpu_load_videoprocessing = Metric(
    name = "gpu_load_videoprocessing",
    title = Title("GPU Load Video Processing"),
    unit = UNIT_NUMBER,
    color = Color.CYAN,
)

#perfometer_digital_signage = Perfometer(
#    name = "gpu_load_3d",
#    focus_range = FocusRange(Closed(1000000000000), Open(20000000000000)),
#    segments=["gpu_load_3d"],
#)

perfometer_digital_signage = Bidirectional(
    name="gpu_load_videoprocessing",
    left=Perfometer(
        name="gpu_load_3d",
        focus_range=FocusRange(
            Closed(0),
            Open(100),
        ),
        segments=["gpu_load_3d"],
    ),
    right=Perfometer(
        name="gpu_load_copy",
        focus_range=FocusRange(
            Closed(0),
            Open(100),
        ),
        segments=["gpu_load_videoprocessing"],
    ),
)