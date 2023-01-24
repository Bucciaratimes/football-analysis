import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import Pitch, add_image, VerticalPitch, FontManager
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patheffects as path_effects
import matplotlib as mpl
from _scripts.metadata import *

pitch = Pitch(
    pitch_type='statsbomb',
    orientation='vertical',
    goal_type = 'box',
    pitch_color = pitchColor,
    line_color = pitchLineColor, 
    figsize=(13.5,8),
    constrained_layout = True,
    tight_layout = False,
    line_zorder=1, linewidth=0.5
)
def draw_field(ax):
    pitch.draw(ax=ax)
    ax.invert_xaxis()