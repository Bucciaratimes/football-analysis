import pandas as pd
import numpy as np
import seaborn as sns

import matplotlib.pyplot as plt
from matplotlib.projections import get_projection_class
import matplotlib.cm as cm
from matplotlib import colors
from mplsoccer import Pitch, add_image, VerticalPitch, FontManager
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patheffects as path_effects
import matplotlib as mpl

from highlight_text import fig_text

from utils.config import *
from utils.formation import *

import warnings
warnings.filterwarnings("ignore")

def plotInsetPassSoner(axes, pdf, x, y, name):
    
    if len(name.split(" "))>=3:
        try:
            first = name.split(" ")[0].title()
            second = name.split(" ")[1].title()
            third = name.split(" ")[2].title()
            name = first[0] + "." + second[0] + "." + third
        except IndexError:
            name = name.split(" ")[0].title()
    else:
        try:
            first = name.split(" ")[0].title()
            second = name.split(" ")[1].title()
            name = first[0] + "." + second
        except IndexError:
            name = name.split(" ")[0].title()

    pos = inset_axes(axes,width=1.5,height=3,loc=10,
                     bbox_to_anchor=(x,y),bbox_transform=axes.transAxes,borderpad=0.0,
                     axes_class=get_projection_class("polar")) 
    pos.set_title(name,color=textColor,fontweight='bold',fontsize=15,fontname='serif') 
    
    cmap = mpl.colors.LinearSegmentedColormap.from_list('cmap', ["#13B9D6","#D61327"])
    colors = cmap(pdf['count']/pdf['count'].max())
    
    multiplier = 2*np.pi/24
    bars = pos.bar(pdf['angle_bin']*multiplier, pdf['avg_length'], width=0.2, bottom=0, 
                      alpha=0.9, 
                      color=colors, zorder=3)
    pos.set_xticklabels([])
    pos.set_yticks([])
#     ax_sub.grid(True, alpha=.5)
    pos.grid(False)
#     ax_sub.spines['polar'].set_visible(True)
    pos.spines['polar'].set_visible(False)

#     ax_sub.spines['polar'].set_color(main_color)
    pos.patch.set_alpha(0)
#     return axes
    return pos

def get_angle(val):
    x1, y1, x2, y2 = val
    dx = x2 - x1
    dy = y2 - y1
    result = np.arctan2(dy, dx)
    return result if result>=0 else result + 2*np.pi
        
def plotPassSoner(ax, df, formationType, team_players_dict):
    
    posLoc = formations[formationType]

    playerPossitions = {}
    count = 0
    for key,val in team_players_dict.items():
        if val == "Sub":
            continue
        if not(isinstance(posLoc[val],list)):
            try:
                playerPossitions[key] = posLoc[val]
            except:
                pass
        else:
            try:
                playerPossitions[key] = posLoc[val][count]
                count+=1
                posLen = len(posLoc[val])
                if count == posLen:
                    count -= posLen
            except:
                pass
    
    for (playerId,playerName), (x,y) in playerPossitions.items():
        playerDf = df[df['playerId']==playerId]
        plotInsetPassSoner(axes=ax, pdf=playerDf, x=x, y=y, name=playerName)
        # player_df = df.query("playerId == @player_id")
        
def main(ax, df, teamId, formationType, team_players_dict):

    df = df[df["teamId"]==teamId]
    df = df[(df['satisfiedEventsTypes'].apply(str).str.contains('passAccurate', na=False)) | (df['eventId'].apply(str).str.contains('passInaccurate', na=False))]    
    df["playerId"] = df["playerId"].astype("int")
    df.reset_index(inplace=True,drop=True)
    
    df['x']=df['x']*1.2
    df['endX']=df['endX']*1.2
    df['y']=df['y']*0.8
    df['endY']=df['endY']*0.8
    df['dist']=np.sqrt((df["endX"]-df["x"])**2 + (df["endY"]-df["y"])**2)
    
    df['y']=80-(df['y'])
    df['endY']=80-(df['endY'])
    df['length'] = np.sqrt(np.square(df["x"] - df["endX"]) + np.square(df["y"] - df["endY"]))
    df['angle'] = df[['y', 'x', 'endY', 'endX']].apply(get_angle, axis=1)
    df['angle_bin'] = pd.cut(df['angle'], bins=np.linspace(0, 2*np.pi, 25), right=True, labels=False)
    df = df.groupby(['playerId', 'angle_bin']).agg(count = ('angle_bin', 'count'), avg_length = ('length', 'mean')).reset_index()

    plotPassSoner(ax, df, formationType, team_players_dict)

#     path_eff = [path_effects.Stroke(linewidth=2, foreground='black'),
#                 path_effects.Normal()]

    # venueColor = {"home":homeColor, "away":awayColor}
    # axes[0].set_title(f"{teamName}".title(),color=venueColor[venue],fontsize=18,fontweight='bold')

#     fig_text(x=0.302, y=0.81, s=f'<{teamName}>'.title(),
#              fontsize=48, ha='center', highlight_colors=[homeColor], highlight_weights=['bold'], path_effects=path_eff)

#     fig_text(x=0.722, y=0.81, s=f'<{opponentName}>'.title(),
#              fontsize=48, ha='center', highlight_colors=[awayColor], highlight_weights=['bold'], path_effects=path_eff)