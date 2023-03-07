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
import seaborn as sns
from highlight_text import ax_text, fig_text
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.font_manager import FontProperties
from matplotlib.offsetbox import (AnnotationBbox, DrawingArea, OffsetImage, TextArea)
from matplotlib.projections import get_projection_class
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mplsoccer import FontManager, Pitch, VerticalPitch, add_image
from plottable import ColumnDefinition, Table

from .metadata import cols, rename_cols

warnings.filterwarnings('ignore')

font_prop = FontProperties(fname="/usr/share/fonts/Nippo-Regular.ttf")
mpl.rcParams['font.family'] = font_prop.get_name()

class PlayerHighlight:

    def __init__(self, axes):
        
        self.axes = axes

    def plot_passmap(self, df, player_id, ax_num, time:int=None)->None:
        """_summary_

        Args:
            df (_type_): _description_
            player_id (_type_): _description_
            ax_num (_type_): _description_
            time (int, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
    
        df['beginning'] = np.sqrt(np.square(120 - df['x']) + np.square(40 - df['y']))
        df['end'] = np.sqrt(np.square(120 - df['endX']) + np.square(40 - df['endY']))
        df['progressive'] = [(df.loc[x, 'end']) / (df.loc[x, 'beginning']) < .75 for x in range(len(df['beginning']))]

        player_df = df[df['player_id'] == player_id]
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
                self.axes[ax_num].annotate("",
                            xy=(row['endY'], row['endX']),
                            xytext=(row["y"], row["x"]),
                            arrowprops={'arrowstyle': "-|>,head_width=.35,head_length=.5",
                                        'fc': '#F5E76B', 'ec': '#F5E76B'},
                            zorder=1)
                
            elif row["progressive"]:
                self.axes[ax_num].scatter(row["y"], row["x"], color="#F5706C", s=20, zorder=1)
                self.axes[ax_num].scatter(row["y"], row["x"], color="#F5706C", s=70, alpha=.3, zorder=1)
                self.axes[ax_num].annotate("",
                            xy=(row['endY'], row['endX']),
                            xytext=(row["y"], row["x"]),
                            arrowprops={'arrowstyle':"-|>, head_width=.35, head_length=.5",
                                        'fc': '#F5706C', 
                                        'ec': '#F5706C'
                            },
                            zorder=1)
                
            elif row["dist"] > 36.57:
                # long passの場合、矢印を曲げる    
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

    def plotScatterMap(self, df, player_id, ax_num, time=None)->None:
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
        player_df = df[df['player_id'] == player_id]
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
            label='Mål', zorder=99)

        return None

    def passSonerMap(self, df, player_id, ax_num):
        """_summary_

        Args:
            df (_type_): _description_
            player_id (_type_): _description_
            ax_num (_type_): _description_

        Returns:
            _type_: _description_
        """
        player_df = df[df['player_id'] == player_id]
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

    def plotHeatMap(self, df, player_id, ax_num):
        """_summary_

        Args:
            df (_type_): _description_
            player_id (_type_): _description_
            ax_num (_type_): _description_

        Returns:
            _type_: _description_
        """
        df = df[df["satisfiedEventsTypes"].apply(str).str.contains("touch", na=False)]
        if player_id is not None:
            player_df = df[df['player_id'] == player_id]
        else:
            player_df = df
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

    def plotConvexfull(self, df, player_id, ax_num):
        """_summary_

        Args:
            df (_type_): _description_
            player_id (_type_): _description_
            ax_num (_type_): _description_
        """
        df = df[df["satisfiedEventsTypes"].apply(str).str.contains("touch", na=False)]
        player_df = df[df['player_id'] == player_id]
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


    def plotBinStatHeatmap(self, pitch, ax_num, df, player_id, font, cmap, alpha):
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
        player_df = df[df['player_id'] == player_id]

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

    def plotHeatMap2(self, df, player_id, pitch, ax_num, time=None, time2=None):
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
            df = df[df["player_id"] == player_id]
        if time is not None:
            df = df[df["minute"] < time]
        if time2 is not None:
            df = df[df["minute"] > time2]
        cmapA = LinearSegmentedColormap.from_list(
            "my_cmap", [pitchColor, "#442D2D", "#852626", "#CB1C1C", "#FF0000"], N=100)
        stats = pitch.bin_statistic(df["x"], df["y"], bins=(12, 8))
        pitch.heatmap(stats, edgecolors='none', cmap=cmapA, alpha=.5, ax=self.axes[ax_num])


    def plotHexbin(self, pitch, df, player_id, ax_num, time=None):
        """_summary_
        """
        player_df = df[df['player_id'] == player_id]
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


    def plotDefensiveLine(self, df, ax_num, defs, mids, teamId=65, time=None, color=None):
        """_summary_

        Args:
            df (_type_): _description_
            ax_num (_type_): _description_
            defs (_type_): _description_
            mids (_type_): _description_
            teamId (int, optional): _description_. Defaults to 65.
            time (_type_, optional): _description_. Defaults to None.
            color (_type_, optional): _description_. Defaults to None.

        Raises:
            Exception: _description_
        """
        if teamId is not None:
            df = df[df["teamId"] != teamId]
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


    def plotDefensiveAct(self, df, player_id, ax_num):
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
        
        player_df = df[(df["player_id"] == player_id)]
        self.axes[ax_num].plot(player_df["y"], player_df["x"], "o")

    def carryPlot(self, df, ax_num, teamId, player_id, carryDist):
        """_summary_

        Args:
            df (_type_): _description_
            ax_num (_type_): _description_
            teamId (_type_): _description_
            player_id (_type_): _description_
            carryDist (_type_): _description_
        """
        df = df[df["teamId"] == teamId]
        df = df[["player_id", "x", "y", "endX", "endY"]]
        df['startX'] = df['endX'].shift(+1)
        df['startY'] = df['endY'].shift(+1)
        df['carry1'] = np.sqrt((120 - df.startX)**2 + (40 - df.startY)**2)
        df['carry2'] = np.sqrt((120 - df.x)**2 + (40 - df.y)**2)
        df['carrydist'] = df['carry1'] - df['carry2']
        df = df.query(f"carrydist>={carryDist} and player_id=={player_id}").dropna()
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
        self.axes[ax_num].plot((df["startY"], df["y"]), (df['startX'], df['x']),
                "#7280D6", linestyle="-.", linewidth=3.2, zorder=.5)
    #     self.axes[ax_num].scatter(df["startY"],df["startX"],color="white",zorder=3,ec="#7280D6",lw=3,s=40)
    #     self.axes[ax_num].scatter(df["startY"],df["startX"],facecolor="#ffffff",edgecolor='#71C1D6',s=15,
    #                 marker="h",alpha=1,
    #                 linewidth=3,linestyle="-.",
    #                 label='Mål',zorder=99)
    #     self.axes[ax_num].scatter(df["startY"],df["startX"],facecolor="#cccccc",edgecolor='#71C1D6',s=60,
    #         marker="h",alpha=.35,
    #         linewidth=3,linestyle="-.",
    #         zorder=99)

        self.axes[ax_num].scatter(df["startY"], df["startX"], color="#D672CF", s=20, zorder=1)  
        self.axes[ax_num].scatter(df["startY"], df["startX"], color="#D672CF", s=70, alpha=.3, zorder=1)

    def make_data(self, type:str=None, league:str="liga", season:str=2223, min_time:int=500):
        """_summary_

        Args:
            league (str): _description_
            season (str): _description_
            min_time (int, optional): _description_. Defaults to 500.

        Returns:
            _type_: _description_
        """
        
        if type == "GK":
            df1 = pd.read_csv(f"/work/assets/fbref/leagueStats/{league}/{season}/keeper.csv")
            df2 = pd.read_csv(f"/work/assets/fbref/leagueStats/{league}/{season}/keeper_adv.csv")
            df = df1.merge(df2)
        
        else:
            df1 = pd.read_csv(f"/work/assets/fbref/leagueStats/{league}/{season}/standard.csv")
            df2 = pd.read_csv(f"/work/assets/fbref/leagueStats/{league}/{season}/shooting.csv")
            df3 = pd.read_csv(f"/work/assets/fbref/leagueStats/{league}/{season}/passing.csv")
            df4 = pd.read_csv(f"/work/assets/fbref/leagueStats/{league}/{season}/passing_types.csv")
            df5 = pd.read_csv(f"/work/assets/fbref/leagueStats/{league}/{season}/gca.csv")
            df6 = pd.read_csv(f"/work/assets/fbref/leagueStats/{league}/{season}/defense.csv")
            df7 = pd.read_csv(f"/work/assets/fbref/leagueStats/{league}/{season}/possession.csv")
            df8 = pd.read_csv(f"/work/assets/fbref/leagueStats/{league}/{season}/playing_time.csv")
            df9 = pd.read_csv(f"/work/assets/fbref/leagueStats/{league}/{season}/misc.csv")

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
        # TODO: 全てのユニットを90分単位に変換
        df["Att_Take-Ons per90"] = round(df["Att_Take-Ons"] /
                                        df['90s_Playing Time'], 2)

        rename_dict = dict(zip(cols, rename_cols))
        df.rename(columns=rename_dict, inplace=True)
        df = df[rename_cols]
        return df

    def make_table(self, df:object, type:int)->None:
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
            target_cols.append("Goals")
            target_cols.append("Assists")
            target_cols.append("npxG+xA")
            target_cols.append("G-Create")
            target_cols.append("S-Create")
            #target_cols.append("Successful%\nDribble")
            #target_cols.append("Dribble Attempt")
            
        elif type == 2:
            target_cols.append("Pass Complete%")
            target_cols.append("Carries")
            target_cols.append("Ball Lost")
            target_cols.append("G-Create")
            target_cols.append("S-Create")

        data = df[target_cols].sort_values(by=target_cols[5], ascending=False).head(10)
        data.index = np.arange(1, len(data) + 1)

        col_defs = (
            [
                ColumnDefinition(
                    name="Player",
                    textprops={
                        "ha": "left",
                        "weight": "bold",
                        "fontproperties": font_prop},
                    width=1.2,
                ),
                ColumnDefinition(
                    name=target_cols[3],
                    textprops={
                        "ha": "center"},
                    width=0.6,
                )
            ]
        )
        
        table = Table(
            data.iloc[:, :-1],
            column_definitions=col_defs,
            row_dividers=True,
            footer_divider=True,
            ax=ax,
            textprops={"fontsize": 15},
            row_divider_kw={"linewidth": 1, "linestyle": (0, (1, 5))},
            col_label_divider_kw={"linewidth": 1, "linestyle": "-"},
            column_border_kw={"linewidth": 1, "linestyle": "-"}
        )
        
def main(theme:str, type:str, player_id):
    
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
        gridspec_kw={"width_ratios": [2, 2, 2, 2, 3.5, 3.5], "height_ratios": [2, 2, 2]})

    fig.set_facecolor(fig_color)
    pitch = VerticalPitch(
        pitch_type='statsbomb',
        pitch_color=fig_color,
        line_color=line_color,
        orientation='vertical',
        goal_type='box',
        figsize=(13.5, 8),
        constrained_layout=True,
        tight_layout=True,
        line_zorder=1, linewidth=1.0,
        pad_top=5,
        positional=True, positional_linestyle=":", positional_color=positional_color,
    )
    for i in range(len(axes)):
        axes[i].set_facecolor(fig_color)
        if i == len(axes)-1:
            axes[2].axis("off")
            break
        pitch.draw(ax=axes[i])
        axes[i].invert_xaxis()
        
    player_highlight = PlayerHighlight()   
    data = player_highlight.make_data()
    player_highlight.make_table(data)

    counts = plotVerticalAndKeyPassMap(df, player_id, axes[0], time=95)
    carryCount = carryPlot(carry_df, axes[0], player_id, teamId, carryDist=(1, 120))
    shots = plotShotmap(pitch, axes[0], carry_df, player_id)
    plotBinStatHeatmap(pitch, axes[1], df, player_id, font=myFont, cmap=cmapA, alpha=1)
    
# plotConvexfull(df,player_id,axes[2],homeColor)
# plotScatterMap(df,player_id,axes[1])
# main(axes[2],teamId,teamName,season,gw,cmapA,kitNum=6)
# plotDefensiveAct(df,player_id,axes[2])
# plotHeatMap2(df,axes[2],pitch,player_id)
# sumXt = plotPassMap(df,player_id,axes[3],time=95)


    for idName in team_players_dict[venue].keys():
        if player_id in idName:
            playerName = idName[1]

    fig_text(
        s=f"<{playerName}>",
        x=axes[0].get_position().x0 + .045,
        y=.935,
        color="#ffffff",
        highlight_textprops=[{'weight': 'semibold',
                            'fontproperties': monoBFont.prop}],
        fontsize=35,
        path_effects=pe2,
        fontproperties=font_prop,
        vpad=20,
        fig=fig)

    fig_text(
        s=f"<Barcelona vs {opponent} | {score} | {league} | whoscored.com | @Bucciaratimes | table is sorted by npxG+xA >",
        x=axes[0].get_position().x0 + .045,
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

    rs = calPassComp(df, player_id)
    fig_text(
        x=axes[0].get_position().x0 + .1, y=axes[1].get_position().y0 - .09,
        s=f"Accurate pass <{rs[0]} ({rs[2]}%)>\nUnaccurate pass <{rs[1]}>\nKey pass <{counts[0]}>",
        va="bottom", ha="center",
        fontsize=17,
        color="#171717",
        font="Nippo", weight="semibold",
        highlight_textprops=[
            {'color': '#048a81', 'weight': 'semibold', 'fontproperties': font_prop},
            {'color': '#C4161C', 'weight': 'semibold', 'fontproperties': font_prop},
            {'color': '#DF9711', 'weight': 'semibold', 'fontproperties': font_prop}],
        vsep=12  # 間隔
    )

    fig.add_artist(mpl.lines.Line2D([0.1, .925], [.83, .83], color="#171717"))
    fig.add_artist(mpl.lines.Line2D([.565, .565], [.83, .1], color="#171717"))


    ax_image = add_image(
        mark,
        fig,
        left=axes[0].get_position().x0,
        bottom=.85,
        width=0.05,
        height=0.068,
        alpha=1)

    plt.savefig(
        f'/work/output/{player_id}_{gw}.png',
        dpi=250,
        bbox_inches="tight",
        facecolor=white_fig_color)

if __name__ == "__main__":
