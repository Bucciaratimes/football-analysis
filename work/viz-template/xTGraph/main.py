import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patheffects as path_effects
import matplotlib as mpl
from highlight_text import fig_text

from config import *
from function import *
import pickle

import warnings
warnings.filterwarnings("ignore")

team_name = "barcelona"
season = 2223
gw = 26
df = pd.read_csv(f'/work/assets/whoscored/{team_name}/match/{season}/eventsData/{season}#{gw}.csv')
df = df.fillna(0)
df = df.dropna(subset=["endY"]).reset_index(drop=True)

with open(file=f'/work/assets/whoscored/{team_name}/ids/{season}/{season}#{gw}.json', mode="rb") as json_file:
    team_players_dict = pickle.load(json_file)

xT = pd.read_csv("/work/assets/xT_Grid.csv",header=None)
xT = np.array(xT)
xT_rows, xT_cols = xT.shape

df['x']=df['x']*1.2
df['endX']=df['endX']*1.2
df['y']=df['y']*0.8
df['endY']=df['endY']*0.8

pass_df = df[df["satisfiedEventsTypes"].apply(str).str.contains("passAccurate",na=False)]
pass_df["x_bin"] = pd.cut(x=pass_df["x"],bins=xT_cols,labels=False)
pass_df["y_bin"] = pd.cut(x=pass_df["y"],bins=xT_rows,labels=False)
pass_df["endX_bin"] = pd.cut(x=pass_df["endX"],bins=xT_cols,labels=False)
pass_df["endY_bin"] = pd.cut(x=pass_df["endY"],bins=xT_rows,labels=False)
pass_df["start_zone_value"] = pass_df[["x_bin","y_bin"]].apply(lambda x: xT[x[1]][x[0]], axis=1)
pass_df["end_zone_value"] = pass_df[["endX_bin","endY_bin"]].apply(lambda x: xT[x[1]][x[0]], axis=1)
pass_df["xT"] = pass_df['end_zone_value'] - pass_df['start_zone_value']

carry_df = df[df["teamId"] == 65]
carry_df = carry_df[["playerId", "x", "y", "endX", "endY"]]
carry_df['startX'] = carry_df['endX'].shift(+1)
carry_df['startY'] = carry_df['endY'].shift(+1)
carry_df['carry1'] = np.sqrt((120 - carry_df.startX)**2 + (40 - carry_df.startY)**2)
carry_df['carry2'] = np.sqrt((120 - carry_df.x)**2 + (40 - carry_df.y)**2)
carry_df['carrydist'] = carry_df['carry1'] - carry_df['carry2']
carry_df = carry_df.dropna()
carry_df["x_bin"] = pd.cut(x=carry_df["startX"],bins=xT_cols,labels=False)
carry_df["y_bin"] = pd.cut(x=carry_df["startY"],bins=xT_rows,labels=False)
carry_df["endX_bin"] = pd.cut(x=carry_df["x"],bins=xT_cols,labels=False)
carry_df["endY_bin"] = pd.cut(x=carry_df["y"],bins=xT_rows,labels=False)
carry_df["start_zone_value"] = carry_df[["x_bin","y_bin"]].apply(lambda x: xT[x[1]][x[0]], axis=1)
carry_df["end_zone_value"] = carry_df[["endX_bin","endY_bin"]].apply(lambda x: xT[x[1]][x[0]], axis=1)
carry_df["xT"] = carry_df['end_zone_value'] - carry_df['start_zone_value']

pass_xTBar = pass_df.groupby(by=["playerId"])["xT"].mean()
carry_xTBar = carry_df.groupby(by=["playerId"])["xT"].mean()

xTBar = pd.concat([pass_xTBar, carry_xTBar]).groupby(by="playerId").sum()

home_players = []
home_xT = []
away_players = []
away_xT = []

for player_id in xTBar.index:
    for item in team_players_dict["home"].keys():
        if player_id in item:
            home_players.append(item[1])
            home_xT.append(pass_xTBar.loc[item[0]])    
            
    for item in team_players_dict["away"].keys():
        if player_id in item:
            away_xT.append(pass_xTBar.loc[item[0]])       
            
fig,axes = plt.subplots(2, 1, figsize=(11,10))
fig.set_facecolor("#131313")

def plot_xTGraph(xT, ax, players, color):
    x = np.arange(len(xT))
    y = xT
    ax.set_facecolor("#131313")
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.barh(x, y, align="center", color=color, ls="-.", edgecolor="#8C7E43") 
#     ax.set_xticks([-.5,0,0.5,1,1.5,2,2.5,3])
#     ax.set_xticklabels(np.linspace(-.5,3,8),color="white",fontproperties=myFont.prop, fontsize=12, fontweight="bold")
    ax.set_yticks(x)
    ax.set_yticklabels(players,fontproperties=myFont.prop, fontsize=12, color="white",fontweight="bold")
    ax.axvline(x=0, ymin=0, ymax=1,color="gray",lw=.2)

plot_xTGraph(home_xT, axes[0], home_players, homeColor)
plot_xTGraph(away_xT, axes[1], away_players, awayColor)

fig_text(
    s="<Sevilla> vs <Barcelona>\nExpected Threat via Passes & Crosses ",
    x=0,y=.915,
    color="#8C898C",
    highlight_colors=[homeColor,awayColor],
    highlight_weights=['regular',"regular"],
    fontsize=22,
    fontproperties=myFont.prop,fig=fig)

fig_text(
    s=f"<Barcelona vs {self.opponent} | {self.note_score} | {self.note_league} | whoscored.com | @Bucciaratimes | table is sorted by {sorted_column} >",
    x=self.axes[0].get_position().x0 + .045,
    y=.89,
    color="#ffffff",
    highlight_textprops=[{
        'weight': 'semibold',
        'fontproperties': font_prop
    }],
    fontsize=16,
    path_effects=custom_path_effect,
    fontproperties=font_prop,
    vpad=20,
    fig=fig
)
# plt.savefig('/work/output/xt.png', dpi=200, bbox_inches="tight",facecolor='#131313')