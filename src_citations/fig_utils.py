

import matplotlib.style
import matplotlib as mpl
from cycler import cycler

FONT_MONOSPACE = {'fontname':'monospace'}
MARKERS = "o^s*DP1"
COLORS = [
    "cornflowerblue",
    "darkseagreen",
    "seagreen",
    "salmon",
    "orange",
    "dimgray",
    "violet",
]

# COLOR1="#751d37"
# COLOR2="#1d6375"
COLOR1 = COLORS[0]
COLOR2 = COLORS[1]

mpl.rcParams['axes.prop_cycle'] = cycler(color=COLORS)
mpl.rcParams['lines.linewidth'] = 2
mpl.rcParams['lines.markersize'] = 7
mpl.rcParams['axes.linewidth'] = 1.5

COLORS_EXTRA = ["#9c2963", "#fb9e07"]
