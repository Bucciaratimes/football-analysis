import math
import warnings
from math import pi

import matplotlib as mpl
import matplotlib.patches as patches
import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats
from scipy.spatial import ConvexHull
import seaborn as sns
from highlight_text import ax_text, fig_text
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.font_manager import FontProperties
from matplotlib.offsetbox import (AnnotationBbox, DrawingArea, OffsetImage, TextArea)
from matplotlib.projections import get_projection_class
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mplsoccer import FontManager, Pitch, VerticalPitch, add_image
from plottable import ColumnDefinition, Table

from metadata import rename_dict

from urllib.request import urlopen
from PIL import Image
import json
import pickle

warnings.filterwarnings('ignore')

font_prop = FontProperties(fname="/usr/share/fonts/Nippo-Regular.ttf")
# mpl.rcParams['font.family'] = font_prop.get_name()

def path_effect_stroke(**kwargs):
    return [path_effects.Stroke(**kwargs), path_effects.Normal()]

pe = path_effect_stroke(linewidth=3, foreground="red")
pe2 = path_effect_stroke(linewidth=3, foreground='black')

class PlayerHighlight:

    def __init__(self, axes, team, team_id, league, season, gw, player_id, venue):
        
        self.axes = axes
        self.team = team
        self.team_id = team_id
        self.league = league
        self.season = season
        self.gw = gw
        self.player_id = player_id
        self.venue = venue
        self.opponent = None
        self.team_players_dict = None
        self.note_league = None
        self.note_venue_name = None
        self.note_score = None
        
    def make_whoscore_data(self):
        
        with open(file=f"/work/assets/whoscored/{self.team}/match/{self.season}/matchData/#{self.gw}.json", mode="rb") as json:
            match_data = pickle.load(json)
        
        self.note_league = match_data["league"]
        self.note_venue_name = match_data["venueName"]
        self.note_score = match_data["score"]
        
        with open(f"/work/assets/whoscored/{self.team}/ids/{self.season}/{self.season}#{self.gw}.json", "rb") as json:
            self.team_players_dict = pickle.load(json)

        df = pd.read_csv(f"/work/assets/whoscored/{self.team}/match/{self.season}/eventsData/{self.season}#{self.gw}.csv")
        self.opponent = df.loc[0,"opponent"]

        df['x']=df['x']*1.2
        df['endX']=df['endX']*1.2
        df['y']=df['y']*0.8
        df['endY']=df['endY']*0.8
        df['dist']=np.sqrt((df["endX"]-df["x"])**2 + (df["endY"]-df["y"])**2)
        
        return df
    
    def add_xT(self, df):
        
        xT = pd.read_csv("/work/assets/xT_Grid.csv",header=None)
        xT = np.array(xT)
        xT_rows, xT_cols = xT.shape
        df = df.dropna(subset=["endY"]).reset_index(drop=True)
        df["x_bin"] = pd.cut(x=df["x"],bins=xT_cols,labels=False)
        df["y_bin"] = pd.cut(x=df["y"],bins=xT_rows,labels=False)
        df["endX_bin"] = pd.cut(x=df["endX"],bins=xT_cols,labels=False)
        df["endY_bin"] = pd.cut(x=df["endY"],bins=xT_rows,labels=False)
        df["start_zone_value"] = df[["x_bin","y_bin"]].apply(lambda x: xT[x[1]][x[0]], axis=1)
        df["end_zone_value"] = df[["endX_bin","endY_bin"]].apply(lambda x: xT[x[1]][x[0]], axis=1)
        df["xT"] = df['end_zone_value'] - df['start_zone_value']
        
        return df

    def plot_passmap(self, df, ax_num, time:int=None)->None:
        """_summary_

        Args:
            df (_type_): _description_
            player_id (_type_): _description_
            ax_num (_type_): _description_
            time (int, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        df = self.add_xT(df)
        df['beginning'] = np.sqrt(np.square(120 - df['x']) + np.square(40 - df['y']))
        df['end'] = np.sqrt(np.square(120 - df['endX']) + np.square(40 - df['endY']))
        df['progressive'] = [(df.loc[x, 'end']) / (df.loc[x, 'beginning']) < .75 for x in range(len(df['beginning']))]

        player_df = df[df['playerId'] == self.player_id]
        if time is not None:
            player_df = player_df[player_df["minute"] < time]

        cmap = mpl.colors.LinearSegmentedColormap.from_list('cmap', ["#13B9D6", "#e76f51", "#D61327"])
        color = cmap(player_df["xT"] / player_df["xT"].max())

        self.axes[ax_num].scatter(player_df["y"], player_df["x"], color=color, s=20, zorder=1)
        self.axes[ax_num].scatter(player_df["y"], player_df["x"], color=color, s=70, alpha=.3, zorder=1)

        for _, row in player_df.iterrows():

            if 'passKey' in row["satisfiedEventsTypes"]:
                self.axes[ax_num].scatter(row["y"], row["x"], color="#F5E76B", s=20, zorder=1)
                self.axes[ax_num].scatter(row["y"], row["x"], color="#F5E76B", s=70, alpha=.3, zorder=1)
                self.axes[ax_num].annotate(
                    "",
                    xy=(row['endY'], row['endX']),
                    xytext=(row["y"], row["x"]),
                    arrowprops={'arrowstyle': "-|>,head_width=.35,head_length=.5",
                                'fc': '#F5E76B', 'ec': '#F5E76B'},
                    zorder=1
                )
                
            elif row["progressive"]:
                self.axes[ax_num].scatter(row["y"], row["x"], color="#F5706C", s=20, zorder=1)
                self.axes[ax_num].scatter(row["y"], row["x"], color="#F5706C", s=70, alpha=.3, zorder=1)
                self.axes[ax_num].annotate(
                    "",
                    xy=(row['endY'], row['endX']),
                    xytext=(row["y"], row["x"]),
                    arrowprops={
                        'arrowstyle':"-|>, head_width=.35, head_length=.5",
                        'fc': '#F5706C', 
                        'ec': '#F5706C'
                    },
                    zorder=1
                )
                
            elif row["dist"] > 36.57:
                # long pass??????????????????????????????    
                if 'passAccurate' in row["satisfiedEventsTypes"]:
                    self.axes[ax_num].annotate("",
                                xy=(row['endY'], row['endX']), xytext=(
                                    row["y"], row["x"]),
                                arrowprops={'arrowstyle':"-|>, head_width=.7, head_length=.9",
                                            'fc': '#76c893',
                                            'ec': '#76c893',
                                            "connectionstyle": "angle3, angleA=0, angleB=95"
                                },
                                zorder=1)

                elif "PassInaccurate" in row["satisfiedEventsTypes"]:
                    self.axes[ax_num].annotate("",
                                xy=(row['endY'], row['endX']),
                                xytext=(row["y"], row["x"]),
                                arrowprops={'arrowstyle':"-|>, head_width=.7, head_length=.9",
                                            'fc': "#7400b8",
                                            'ec': "#7400b8",
                                            "connectionstyle": "angle3, angleA = 0, angleB = 95"
                                },
                                zorder=1)

            else:
                if 'passAccurate' in row["satisfiedEventsTypes"]:
                    self.axes[ax_num].annotate("",
                                xy=(row['endY'], row['endX']),
                                xytext=(row["y"], row["x"]),
                                arrowprops={'arrowstyle': "-|>,head_width=.7,head_length=.9",
                                            'fc': '#76c893',
                                            'ec': '#76c893'
                                },
                                zorder=1)

                elif "PassInaccurate" in row["satisfiedEventsTypes"]:
                    self.axes[ax_num].annotate("",
                                xy=(row['endY'], row['endX']),
                                xytext=(row["y"], row["x"]),
                                arrowprops={'arrowstyle': "-|>,head_width=.7,head_length=.9",
                                            'fc': "#7400b8",
                                            'ec': "#7400b8"
                                },
                                zorder=1)
        return None

    def plotShotmap(self, pitch, df, ax_num):
        
        df = df[df["playerId"] == self.player_id]
        shotDf = df[df["satisfiedEventsTypes"].apply(str).str.contains('shotsTotal')]
        goal = df[df["satisfiedEventsTypes"].apply(str).str.contains('goal')]
        onTarget = df[df["satisfiedEventsTypes"].apply(str).str.contains('shotOnTarget')]
        offTarget = df[df["satisfiedEventsTypes"].apply(str).str.contains('shotOffTarget')]
        blocked = df[df["satisfiedEventsTypes"].apply(str).str.contains('shotBlocked')]
        cmap = mpl.colors.LinearSegmentedColormap.from_list('cmap', ["#131313","#f8f8f8","#ffffff"])
        for items in zip([onTarget,goal,offTarget,blocked],["#ff5c8a","#EF8804","#4ea8de","#67b99a"]):
            for idx,row in items[0].iterrows():
                if row["y"] >= 45:
                    if row["x"] >= 105:
                        scatter = pitch.scatter(row.x+4,row.y-3.5,color=fig_color,marker="*",ax=self.axes[ax_num],zorder=10,ec=items[1],lw=2,s=200)
                        Lines = pitch.lines(xstart=row.x,ystart=row.y,xend=row.x+4,yend=row.y-3.5,cmap=cmap,comet=True,lw=4,ax=self.axes[ax_num],zorder=4)
                    else:
                        scatter = pitch.scatter(row.x+10,row.y-3.5,color=fig_color,marker="*",ax=self.axes[ax_num],zorder=10,ec=items[1],lw=2,s=200)
                        Lines = pitch.lines(xstart=row.x,ystart=row.y,xend=row.x+10,yend=row.y-3.5,cmap=cmap,comet=True,lw=4,ax=self.axes[ax_num],zorder=4)
                elif row["y"] <= 35:
                    if row["x"] >= 105:
                        scatter = pitch.scatter(row.x+4,row.y+3.5,color=fig_color,marker="*",ax=self.axes[ax_num],zorder=10,ec=items[1],lw=2,s=200)
                        Lines = pitch.lines(xstart=row.x,ystart=row.y,xend=row.x+4,yend=row.y+3.5,cmap=cmap,comet=True,lw=4,ax=self.axes[ax_num],zorder=4)
                    else:
                        scatter = pitch.scatter(row.x+10,row.y+3.5,color=fig_color,marker="*",ax=self.axes[ax_num],zorder=10,ec=items[1],lw=2,s=200)
                        Lines = pitch.lines(xstart=row.x,ystart=row.y,xend=row.x+10,yend=row.y+3.5,cmap=cmap,comet=True,lw=4,ax=self.axes[ax_num],zorder=4)
                else:
                    if row["x"] >= 105:
                        scatter = pitch.scatter(row.x+4,row.y,color=fig_color,marker="*",ax=self.axes[ax_num],zorder=10,ec=items[1],lw=2,s=200)
                        Lines = pitch.lines(xstart=row.x,ystart=row.y,xend=row.x+4,yend=row.y,cmap=cmap,comet=True,lw=4,ax=self.axes[ax_num],zorder=4)
                    else:
                        scatter = pitch.scatter(row.x+10,row.y,color=fig_color,marker="*",ax=self.axes[ax_num],zorder=10,ec=items[1],lw=2,s=200)
                        Lines = pitch.lines(xstart=row.x,ystart=row.y,xend=row.x+10,yend=row.y,cmap=cmap,comet=True,lw=4,ax=self.axes[ax_num],zorder=4)
        
        onTarget_len = len(onTarget) - len(goal)
                    
        return [len(shotDf),len(goal),onTarget_len,len(offTarget),len(blocked)]

    def plotScatterMap(self, df, ax_num, time=None)->None:
        """_summary_

        Args:
            df (_type_): _description_
            player_id (_type_): _description_
            ax_num (_type_): _description_
            time (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        df = df[df["satisfiedEventsTypes"].apply(str).str.contains("touch", na=False)]
        player_df = df[df['playerId'] == self.player_id]
        if time is not None:
            player_df = player_df[player_df["minute"] < time]

        x = player_df['x']
        y = player_df['y']
        meanX = player_df["x"].median()
        meanY = player_df["y"].median()

        self.axes[ax_num].scatter(y, x, color="#555555", s=20, marker="h", zorder=1)
        self.axes[ax_num].scatter(y, x, color="#555555", s=100, marker="h", alpha=.7, zorder=1)
        self.axes[ax_num].scatter(
            meanY, meanX, facecolor="#cccccc", edgecolor='gold', s=300 * 4,
            marker="h", alpha=.35,
            linewidth=3, linestyle="--",
            zorder=99)
        self.axes[ax_num].scatter(
            meanY, meanX, facecolor="#ffffff", edgecolor='gold', s=335 * 2,
            marker="h", alpha=1,
            linewidth=3, linestyle="--",
            label='M??l', zorder=99)

        return None

    def passSonerMap(self, df, ax_num):
        """_summary_

        Args:
            df (_type_): _description_
            player_id (_type_): _description_
            ax_num (_type_): _description_

        Returns:
            _type_: _description_
        """
        player_df = df[df['playerId'] == self.player_id]
        cmap = mpl.colors.LinearSegmentedColormap.from_list(
            'cmap', ["#13B9D6", "#D61327"])
        colors = cmap(player_df['count'] / player_df['count'].max())
        multiplier = 2 * np.pi / 24
        bars = self.axes[ax_num].bar(
            player_df['angle_bin'] * multiplier,
            player_df['avg_length'],
            width=0.2,
            bottom=0,
            alpha=0.9,
            color=colors,
            zorder=3)

        self.axes[ax_num].set_xticklabels([])
        self.axes[ax_num].set_yticks([])
        # ax_sub.grid(True, alpha=.5)
        self.axes[ax_num].grid(False)
        # ax_sub.spines['polar'].set_visible(True)
        self.axes[ax_num].spines['polar'].set_visible(False)
        # ax_sub.spines['polar'].set_color(main_color)
        self.axes[ax_num].patch.set_alpha(0)
        return self.axes[ax_num]

    def plotHeatMap(self, df, ax_num):
        """_summary_

        Args:
            df (_type_): _description_
            player_id (_type_): _description_
            ax_num (_type_): _description_

        Returns:
            _type_: _description_
        """
        df = df[df["satisfiedEventsTypes"].apply(str).str.contains("touch", na=False)]
        player_df = df[df['playerId'] == self.player_id]
        
        cmap = mpl.colors.LinearSegmentedColormap.from_list(
            'cmap', ["#131313", "#D61327"])  # 13B9D6

        kde = sns.kdeplot(
            player_df['y'],
            player_df['x'],
            shade=True,
            shade_lowest=False,
            alpha=.9,
            n_lavels=10,
            cmap=cmap,
            ax=self.axes[ax_num])

        return None

    def plotConvexfull(self, df, ax_num):
        """_summary_

        Args:
            df (_type_): _description_
            player_id (_type_): _description_
            ax_num (_type_): _description_
        """
        df = df[df["satisfiedEventsTypes"].apply(str).str.contains("touch", na=False)]
        player_df = df[df['playerId'] == self.player_id]
        maxX, maxY = player_df[["x", "y"]].mean() + player_df[['x', 'y']].std()
        minX, minY = player_df[["x", "y"]].mean() - player_df[['x', 'y']].std()
        covX = []
        covY = []
        for index, row in player_df.iterrows():
            if row["x"] < maxX and row["y"] < maxY:
                if row["x"] > minX and row["y"] > minY:
                    covX.append(row["x"])
                    covY.append(row["y"])
            else:
                continue

        covDf = pd.DataFrame(columns=["x", "y"])
        covDf["x"] = covX
        covDf["y"] = covY

        points = covDf[['x', 'y']].values
        if len(points) > 2:
            hull = ConvexHull(covDf[['x', 'y']])
            for simplex in hull.simplices:
                #             self.axes[ax_num].scatter(points[:,1],points[:,0],color="blue")
                self.axes[ax_num].plot(points[simplex, 1], points[simplex, 0],
                        linestyle='-.', color="#F5E76B", linewidth=1)
    #             self.axes[ax_num].plot(points[hull.vertices,1],points[hull.vertices,0],linestyle='-.',color="white",linewidth=.3)
                self.axes[ax_num].fill(points[hull.vertices, 1], points[hull.vertices, 0],
                        fc="white", ec='white', linewidth=6, hatch="///" * 3, alpha=.01)
        else:
            pass

    def plotBinStatHeatmap(self, pitch, ax_num, df, font, cmap, alpha):
        """_summary_

        Args:
            pitch (_type_): _description_
            ax_num (_type_): _description_
            df (_type_): _description_
            player_id (_type_): _description_
            font (_type_): _description_
            cmap (_type_): _description_
            alpha (_type_): _description_

        Returns:
            _type_: _description_
        """
        player_df = df[df['playerId'] == self.player_id]

        # bin_statistic = pitch.bin_statistic_positional(df["x"], df["y"], statistic='count',
        # positional='full', normalize=True)

        # pitch.heatmap_positional(bin_statistic, ax=ax['pitch'][idx],
        # cmap=cmap, edgecolors='#495E62',alpha=1, linewidth=.05)

        # labels = pitch.label_heatmap(bin_statistic, color=text_color, fontsize=18,
        #                             ax=ax['pitch'][idx], ha='center', va='center',
        #                             str_format='{:.0%}',fontproperties=font.prop)

        stats = pitch.bin_statistic(player_df["x"], player_df["y"], statistic='count', normalize=True)

        pitch.heatmap(stats, edgecolors='black', cmap=cmap, ax=ax_num, alpha=alpha)

        path_eff = [path_effects.Stroke(linewidth=0.5, foreground='seagreen')]

        text = pitch.label_heatmap(
            stats,
            color='white',
            ax=self.axes[ax_num],
            fontsize=14,
            ha='center',
            va='center',
            alpha=.5,
            path_effects=path_eff,
            str_format='{:.0%}')
        return None

    def plotHeatMap2(self, df, pitch, ax_num, time=None, time2=None):
        """_summary_

        Args:
            df (_type_): _description_
            player_id (_type_): _description_
            pitch (_type_): _description_
            ax_num (_type_): _description_
            time (_type_, optional): _description_. Defaults to None.
            time2 (_type_, optional): _description_. Defaults to None.
        """
        if player_id is not None:
            df = df[df["player_id"] == self.player_id]
        if time is not None:
            df = df[df["minute"] < time]
        if time2 is not None:
            df = df[df["minute"] > time2]
        cmapA = LinearSegmentedColormap.from_list(
            "my_cmap", [pitchColor, "#442D2D", "#852626", "#CB1C1C", "#FF0000"], N=100)
        stats = pitch.bin_statistic(df["x"], df["y"], bins=(12, 8))
        pitch.heatmap(stats, edgecolors='none', cmap=cmapA, alpha=.5, ax=self.axes[ax_num])

    def plotHexbin(self, pitch, df, ax_num, time=None):
        """_summary_
        """
        player_df = df[df['playerId'] == self.player_id]
        x = player_df["endX"]
        y = player_df["endY"]
        
        cmap = colors.ListedColormap([
            "#222222",
            "#2A2224",
            "#3A2027",
            "#421F28",
            "#54202B",
            "#65202E",
            "#782231",
            "#892433",
            "#9B2838",
            "#AC2B3A",
            "#BE2F3E",
            "#CF3341",
            "#E13746"
            ])
        
        pitch.hexbin(
            x,
            y,
            edgecolors='white',
            gridsize=(20, 9),
            cmap=cmap,
            ax=self.axes[ax_num],
            bins="log")

    def plotDefensiveLine(self, df, ax_num, defs, mids, highlight_team_id=65, time=None, color=None):
        """_summary_

        Args:
            df (_type_): _description_
            ax_num (_type_): _description_
            defs (_type_): _description_
            mids (_type_): _description_
            highlight_team_id (int, optional): _description_. Defaults to 65.
            time (_type_, optional): _description_. Defaults to None.
            color (_type_, optional): _description_. Defaults to None.

        Raises:
            Exception: _description_
        """
        if highlight_team_id is not None:
            df = df[df["teamId"] != highlight_team_id]
        elif time is not None:
            if isinstance(time, tuple):
                if len(time) == 2:
                    if time[0] < time[1]:
                        early = time[0]
                        later = time[1]
                    else:
                        early = time[1]
                        later = time[0]

                    df = df[(df["minute"] >= early) & (df["minute"] <= later)]
                else:
                    raise Exception
            else:
                df = df[df["minute"] <= time]

        df = df[df["satisfiedEventsTypes"].apply(
            str).str.contains("touch", na=False)]
        dfD = df[(df["player_id"] == defs[0][0]) | (df["player_id"] == defs[1][0]) | (
            df["player_id"] == defs[2][0]) | (df["player_id"] == defs[3][0])]
        dfM = df[(df["player_id"] == mids[0][0]) | (df["player_id"] == mids[1][0]) | (
            df["player_id"] == mids[2][0]) | (df["player_id"] == mids[3][0]) | (df["player_id"] == mids[4][0])]

        dAveX = dfD["x"].median()
        dAveY = dfD["y"].mean()
        mAveX = dfM["x"].median()
        mAveY = dfM["y"].mean()
        self.axes[ax_num].plot((0, 80), (120 - dAveY, 120 - dAveY),
                "#14FFFF", linestyle="-.", linewidth=1.2)
        self.axes[ax_num].plot((0, 80), (120 - mAveY, 120 - mAveY),
                "#14FFFF", linestyle="-.", linewidth=1.2)

    def plotDefensiveAct(self, df, ax_num):
        """_summary_

        Args:
            df (_type_): _description_
            player_id (_type_): _description_
            ax_num (_type_): _description_
        """
        df = df[
            (df['satisfiedEventsTypes'].apply(str).str.contains('tackleLost')) | (
            df['satisfiedEventsTypes'].apply(str).str.contains('tackleWon')) | (
            df['satisfiedEventsTypes'].apply(str).str.contains('interceptionAll')) | (
            df['satisfiedEventsTypes'].apply(str).str.contains('outfielderBlock')) | (
            df['satisfiedEventsTypes'].apply(str).str.contains('interceptionWon')) | ( 
            df['satisfiedEventsTypes'].apply(str).str.contains('outfielderBlockedPass')) | (
            df['satisfiedEventsTypes'].apply(str).str.contains('clearanceTotal'))
            ]
        
        player_df = df[(df["player_id"] == self.player_id)]
        self.axes[ax_num].plot(player_df["y"], player_df["x"], "o")

    def carryPlot(self, df, ax_num, highlight_team_id, carryDist):
        """_summary_

        Args:
            df (_type_): _description_
            ax_num (_type_): _description_
            highlight_team_id (_type_): _description_
            player_id (_type_): _description_
            carryDist (_type_): _description_
        """
        df = df[df["teamId"] == self.team_id]
        df = df[["playerId", "x", "y", "endX", "endY"]]
        df['startX'] = df['endX'].shift(+1)
        df['startY'] = df['endY'].shift(+1)
        df['carry1'] = np.sqrt((120 - df.startX)**2 + (40 - df.startY)**2)
        df['carry2'] = np.sqrt((120 - df.x)**2 + (40 - df.y)**2)
        df['carrydist'] = df['carry1'] - df['carry2']
        df = df.query(f"carrydist>={carryDist} and playerId=={self.player_id}").dropna()
        print("Carry:", len(df))
        print("CarryDist mean:", df["carrydist"].mean())
    #     Lines = pitch.lines(xstart=df["startX"],ystart=df["startY"],xend=df["x"],yend=df["y"],
    #                         cmap=cmapA,comet=True,linewidth=3,linestyle="-.",ax=ax)
    #     for idx,row in df.iterrows():
    #         self.axes[ax_num].annotate("",
    #                 xy=(row['y'],row['x']),
    #                 xytext=(row["startY"],row["startX"]),
    #                 arrowprops={'arrowstyle':"-|>,head_width=.3,head_length=.45",
    #                             'fc':'#555555',
    #                             'ec':'#555555'},
    #                 zorder=.5)
        self.axes[ax_num].plot(
            (df["startY"], df["y"]), 
            (df['startX'], df['x']), 
            "#7280D6", 
            linestyle="-.", 
            linewidth=3.2,
            zorder=.5
        )
    #     self.axes[ax_num].scatter(df["startY"],df["startX"],color="white",zorder=3,ec="#7280D6",lw=3,s=40)
    #     self.axes[ax_num].scatter(df["startY"],df["startX"],facecolor="#ffffff",edgecolor='#71C1D6',s=15,
    #                 marker="h",alpha=1,
    #                 linewidth=3,linestyle="-.",
    #                 label='M??l',zorder=99)
    #     self.axes[ax_num].scatter(df["startY"],df["startX"],facecolor="#cccccc",edgecolor='#71C1D6',s=60,
    #         marker="h",alpha=.35,
    #         linewidth=3,linestyle="-.",
    #         zorder=99)

        self.axes[ax_num].scatter(df["startY"], df["startX"], color="#D672CF", s=20, zorder=1)  
        self.axes[ax_num].scatter(df["startY"], df["startX"], color="#D672CF", s=70, alpha=.3, zorder=1)

    def make_table_data(self, type:int=2, min_time:int=500):
        """_summary_

        Args:
            type (int, optional): _description_. Defaults to 2. 1->GK, 2->Field Player
            min_time (int, optional): _description_. Defaults to 500.

        Returns:
            _type_: _description_
        """
        
        if type == 1:
            df1 = pd.read_csv(f"/work/assets/fbref/leagueStats/{self.league}/{self.season}/keeper.csv")
            df2 = pd.read_csv(f"/work/assets/fbref/leagueStats/{self.league}/{self.season}/keeper_adv.csv")
            df = df1.merge(df2, how="inner", on=["Player", "Nation"], suffixes=["", "_duplicated"])
        
        else:
            df1 = pd.read_csv(f"/work/assets/fbref/leagueStats/{self.league}/{self.season}/standard.csv")
            df2 = pd.read_csv(f"/work/assets/fbref/leagueStats/{self.league}/{self.season}/shooting.csv")
            df3 = pd.read_csv(f"/work/assets/fbref/leagueStats/{self.league}/{self.season}/passing.csv")
            df4 = pd.read_csv(f"/work/assets/fbref/leagueStats/{self.league}/{self.season}/passing_types.csv")
            df5 = pd.read_csv(f"/work/assets/fbref/leagueStats/{self.league}/{self.season}/gca.csv")
            df6 = pd.read_csv(f"/work/assets/fbref/leagueStats/{self.league}/{self.season}/defense.csv")
            df7 = pd.read_csv(f"/work/assets/fbref/leagueStats/{self.league}/{self.season}/possession.csv")
            df8 = pd.read_csv(f"/work/assets/fbref/leagueStats/{self.league}/{self.season}/playing_time.csv")
            df9 = pd.read_csv(f"/work/assets/fbref/leagueStats/{self.league}/{self.season}/misc.csv")

            df = df1.merge(df2, how="inner", on=["Player", "Nation"], suffixes=["", "_duplicated"]) \
                    .merge(df3, how="inner", on=["Player", "Nation"], suffixes=["", "_duplicated"]) \
                    .merge(df4, how="inner", on=["Player", "Nation"], suffixes=["", "_duplicated"]) \
                    .merge(df5, how="inner", on=["Player", "Nation"], suffixes=["", "_duplicated"]) \
                    .merge(df6, how="inner", on=["Player", "Nation"], suffixes=["", "_duplicated"]) \
                    .merge(df7, how="inner", on=["Player", "Nation"], suffixes=["", "_duplicated"]) \
                    .merge(df8, how="inner", on=["Player", "Nation"], suffixes=["", "_duplicated"]) \
                    .merge(df9, how="inner", on=["Player", "Nation"], suffixes=["", "_duplicated"])

            not_duplicated_cols = [col for col in df.columns if not "_duplicated" in col]
            df = df[not_duplicated_cols]
            
        df = df[df["Min_Playing Time"] > min_time]
        df.rename(columns=rename_dict, inplace=True)
        df.reset_index(inplace=True, drop=True)

        not_90_min_cols = [col for col in df.columns if not "Per90" in col or not "%" in col or not "Goal-xG(non-pen)" in col or not "xG Plus/Minus" in col]
        df.loc[:,not_90_min_cols].iloc[:, 12:] = df.loc[:,not_90_min_cols].iloc[:, 12:].apply(lambda x: x / df["90s"])
        
        return df

    def make_table(self, df:object, type:int, ax_num:int=2, target_column_num=1)->None:
        """_summary_

        Args:
            df (object): _description_
            type (int): 
                1->FW
                2->MF
                3->DF
        """

        target_cols: List[str] = ["Player"]
        if type == 1:
            target_cols.append("xG Plus/Minus")
            target_cols.append("npxG+xA")
            target_cols.append("Goal-xG(non-pen)")
            target_cols.append("Shot Create")
            target_cols.append("Successful%\nDribble")
            #target_cols.append("Dribble Attempt")
            
        elif type == 2:
            target_cols.append("xG Plus/Minus")
            target_cols.append("KP")
            target_cols.append("Carries")
            target_cols.append("Switch Pass")
            #target_cols.append("Pass Complete%")
            target_cols.append("Ball Lost")
            
        elif type == 3:
            target_cols.append("xG Plus/Minus")
            target_cols.append("Tackle Win")
            target_cols.append("Intercept")
            target_cols.append("Won% Aerial Duels")
            target_cols.append("Recovery")

        data = df[target_cols].sort_values(by=target_cols[target_column_num], ascending=False).head(10)
        data.index = np.arange(1, len(data) + 1)

        col_defs = (
            [
                ColumnDefinition(
                    name="Player",
                    textprops={"ha": "center", "weight": "bold", "fontproperties": font_prop},
                    width=1.2,
                ),
                ColumnDefinition(
                    name=target_cols[1],
                    textprops={"ha": "center", "weight": "bold", "fontproperties": font_prop },
                    width=0.6,
                ),
                ColumnDefinition(
                    name=target_cols[2],
                    textprops={"ha": "center", "weight": "bold", "fontproperties": font_prop },
                    width=0.6,
                ),
                ColumnDefinition(
                    name=target_cols[3],
                    textprops={"ha": "center", "weight": "bold", "fontproperties": font_prop },
                    width=0.6,
                ),ColumnDefinition(
                    name=target_cols[4],
                    textprops={"ha": "center", "weight": "bold", "fontproperties": font_prop },
                    width=0.6,
                )
            ]
        )
        
        table = Table(
            data.iloc[:, :-1],
            column_definitions=col_defs,
            row_dividers=True,
            footer_divider=True,
            ax=self.axes[ax_num],
            textprops={"fontsize": 15},
            row_divider_kw={"linewidth": 1, "linestyle": (0, (1, 5))},
            col_label_divider_kw={"linewidth": 1, "linestyle": "-"},
            column_border_kw={"linewidth": 1, "linestyle": "-"}
        )
        
    def plot_note(self, fig, whoscore_data, counts):
        for id_name in self.team_players_dict[self.venue].keys():
            if self.player_id in id_name:
                player_name = id_name[1]

        fig_text(
            s=f"<{player_name}>",
            x=self.axes[0].get_position().x0 + .045,
            y=.935,
            color="#ffffff",
            highlight_textprops=[{'weight': 'semibold',
                                'fontproperties': font_prop}],
            fontsize=35,
            path_effects=pe2,
            fontproperties=font_prop,
            vpad=20,
            fig=fig)

        fig_text(
            s=f"<Barcelona vs {self.opponent} | {self.note_score} | {self.note_league} | whoscored.com | @Bucciaratimes | table is sorted by npxG+xA >",
            x=self.axes[0].get_position().x0 + .045,
            y=.89,
            color="#ffffff",
            highlight_textprops=[
                {
                    'weight': 'semibold',
                    'fontproperties': font_prop}],
            fontsize=20,
            path_effects=pe2,
            fontproperties=font_prop,
            vpad=20,
            fig=fig)

        rs = self.calc_pass_comp(whoscore_data)
        print(rs)
        fig_text(
            x=self.axes[0].get_position().x0 + .1, y=self.axes[1].get_position().y0 - .09,
            s=f"Accurate pass <{rs[0]} ({rs[2]}%)>\nUnaccurate pass <{rs[1]}>\nKey pass <{counts[0]}>",
            va="bottom", ha="center",
            fontsize=17,
            color="#171717",
            font="Nippo", weight="semibold",
            highlight_textprops=[
                {'color': '#048a81', 'weight': 'semibold', 'fontproperties': font_prop},
                {'color': '#C4161C', 'weight': 'semibold', 'fontproperties': font_prop},
                {'color': '#DF9711', 'weight': 'semibold', 'fontproperties': font_prop}
            ],
            vsep=12  # ??????
        )
        
        ax_image = add_image(
            highlight_mark,
            fig,
            left=self.axes[0].get_position().x0,
            bottom=.85,
            width=0.05,
            height=0.068,
            alpha=1
        )
        
    def calc_pass_comp(self, df:object):
        df = df[df["playerId"]==self.player_id]
        pass_accurate = df[df["satisfiedEventsTypes"].apply(str).str.contains("PassAccurate",na=False)]
        pass_inaccurate = df[df["satisfiedEventsTypes"].apply(str).str.contains("PassInaccurate",na=False)]
        try:
            pass_comp = round((len(pass_accurate)/((len(pass_accurate)+len(pass_inaccurate))))*100,2)
        except:
            pass_comp = 0
        return (len(pass_accurate), len(pass_inaccurate), pass_comp)
        
def main(theme:str, type:str):
    
    if theme == "white":
        fig_color = "#ffffff"
        line_color = "#999999"
        positional_color = "#454545"
    elif theme == "black":
        fig_color = "#171717"
        line_color = "#fefefe"
        positional_color = "#cdcdcd"

    layout = [
        [0, 0, 1, 1, 2, 2],
        [0, 0, 1, 1, 2, 2],
        [0, 0, 1, 1, 2, 2]
        ]

    fig, axes = plt.subplot_mosaic(
        layout, 
        figsize=(25, 13),
        linewidth=2,
        gridspec_kw={"width_ratios": [2, 2, 2, 2, 3.5, 3.5], "height_ratios": [2, 2, 2]}
    )

    fig.set_facecolor(fig_color)
    pitch = VerticalPitch(
        figsize=(13.5, 8),
        pitch_type='statsbomb',
        pitch_color=fig_color,
        orientation='vertical',
        goal_type='box',
        line_color=line_color, line_zorder=1, linewidth=1.0,
        positional=True, positional_linestyle=":", positional_color=positional_color,
        pad_top=5,
        constrained_layout=True,
        tight_layout=True
    )
    for i in range(len(axes)):
        axes[i].set_facecolor(fig_color)
        axes[i].invert_xaxis()
        if i == len(axes)-1:
            axes[2].axis("off")
            break
        pitch.draw(ax=axes[i])
        
    player_highlight = PlayerHighlight(
        axes=axes, 
        team=highlight_team,
        team_id=highlight_team_id,
        league=highlight_league, 
        season=highlight_season, 
        gw=highlight_gw, 
        player_id=highlight_player_id,
        venue=venue
    )
    
    data = player_highlight.make_table_data(type=type)
    player_highlight.make_table(df=data, type=1, ax_num=2)
    
    whoscore_data = player_highlight.make_whoscore_data()
    counts = player_highlight.plot_passmap(whoscore_data, 0, time=95)
    carryCount = player_highlight.carryPlot(whoscore_data, 0, highlight_team_id, carryDist=1)
    shots = player_highlight.plotShotmap(pitch, 0, whoscore_data)
    player_highlight.plotBinStatHeatmap(pitch, 1, whoscore_data, font=myFont, cmap=cmapA, alpha=1)
    
    # plotConvexfull(df, axes[2],homeColor)
    # plotScatterMap(df, axes[1])
    # main(axes[2],highlight_team_id,highlight_team,season,gw,cmapA,kitNum=6)
    # plotDefensiveAct(df, axes[2])
    # plotHeatMap2(df,axes[2],pitch)
    # sumXt = plotPassMap(df, axes[3],time=95)
    
    player_highlight.plot_note(fig, whoscore_data, counts)

    fig.add_artist(mpl.lines.Line2D([0.1, .925], [.83, .83], color="#171717"))
    fig.add_artist(mpl.lines.Line2D([.565, .565], [.83, .1], color="#171717"))

    plt.savefig(
        f'/work/output/{player_id}_{highlight_gw}.png',
        dpi=250,
        bbox_inches="tight",
        facecolor=fig_color)

if __name__ == "__main__":
    
    highlight_team_id = 65
    highlight_team = 'barcelona'
    highlight_league = "liga"
    highlight_season = input("season: ....?")
    highlight_gw = input("gameweek: ....?")
    highlight_player_id = input("player_id: ....?")
    venue = input("home or away: ....?")
    
    clubMark = "https://upload.wikimedia.org/wikipedia/en/thumb/4/47/FC_Barcelona_%28crest%29.svg/1200px-FC_Barcelona_%28crest%29.svg.png"
    highlight_mark = Image.open(urlopen(clubMark))
    
    main(theme="white", type=1)
    
