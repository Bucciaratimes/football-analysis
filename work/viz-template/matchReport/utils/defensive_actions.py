import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import pandas as pd

from utils.metadata import *

#from extract_data import *

def plot_defensive_actions(fig, ax, def_actions, labels, team):

    TEAM_COLORS = {'home': "crimson", 'away': away_color}

    labels_int = [int(num.replace('%', '')) for num in labels]
    
    path_eff = [path_effects.Stroke(linewidth=3, foreground='black'),
                path_effects.Normal()]
    
    x_pos = [17, 50, 83.2]
    ax.bar(17, 100, width=33, 
        align='center', color=[TEAM_COLORS[team]], alpha=labels_int[0]*0.01, linewidth=4, zorder=5)
    ax.bar(50, 100, width=33, 
        align='center', color=[TEAM_COLORS[team]], alpha=labels_int[1]*0.01, linewidth=4, zorder=5)
    ax.bar(83.2, 100, width=33, 
        align='center', color=[TEAM_COLORS[team]], alpha=labels_int[2]*0.01, linewidth=4, zorder=5)

    ax.text(s=labels[0], x=18, y=57, 
            color='w', fontsize=25, fontweight='bold', ha='center', zorder=15, path_effects=path_eff, alpha=1)
    ax.text(s=labels[1], x=52, y=57, 
            color='w', fontsize=25, fontweight='bold', ha='center', zorder=15, path_effects=path_eff, alpha=1)
    ax.text(s=labels[2], x=82, y=57, 
            color="w", fontsize=25, fontweight='bold', ha='center', zorder=15, path_effects=path_eff, alpha=1)

    #TEAM_COLORS[team]
    #plot defensive actions
#     ax.scatter(def_actions.x, def_actions.y, 
#                 s=20, color='k', alpha=0.8, zorder=10)
    #ax.scatter(def_actions.x, def_actions.y, 
    #            s=150, color='w', alpha=0.2, marker='h', zorder=4)
    
    if team == 'away':
        ax.invert_xaxis()
        #ax.invert_yaxis()
    
#     add_arrow(ax, team)
    
    # Add title
    add_ax_title(ax, 'Defensive Actions')

    
    return None
