from config import *
from highlight_text import fig_text
from scipy.spatial import ConvexHull
import matplotlib as mpl
import matplotlib.patheffects as path_effects
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mplsoccer import Pitch, add_image, VerticalPitch, FontManager
from matplotlib import colors
import matplotlib.cm as cm
from matplotlib.projections import get_projection_class
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
class PlayerHighlight:
    def __init__(self, axes, theme):

        self.axes = axes
        if theme == "white":
            self.fig_color = "#ffffff"
            self.line_color = "#999999"
        elif theme == "black":
            self.fig_color = "#171717"
            self.line_color = "#fefefe"

    def plot_passmap():


def plotPassMap(df, playerId, ax, time=None):
    pdf = df[df['playerId'] == playerId]
    if time is not None:
        pdf = pdf[pdf["minute"] < time]

    x = pdf['x']
    y = pdf['y']
    endX = pdf['endX']
    endY = pdf['endY']

    cmap = mpl.colors.LinearSegmentedColormap.from_list(
        'cmap', ["#13B9D6", "#e76f51", "#D61327"])
    color = cmap(pdf["xT"] / pdf["xT"].max())

#     ax.scatter(y,x,color="#dc2f02",s=30)
#     ax.scatter(y,x,color="#ffba08",s=80,alpha=.3)

    ax.scatter(y, x, color=color, s=100, zorder=1)
    ax.scatter(y, x, color=color, s=350, alpha=.3, zorder=1)

    for index, row in pdf.iterrows():
        if row["dist"] > 36.57:
            if 'passAccurate' in row["satisfiedEventsTypes"]:
                ax.annotate("",
                            xy=(row['endY'], row['endX']), xytext=(
                                row["y"], row["x"]),
                            arrowprops={'arrowstyle': "-|>,head_width=.7,head_length=.9",
                                        'fc': '#76c893',
                                        'ec': '#76c893',
                                        "connectionstyle": "angle3, angleA = 0, angleB = 95"
                                        #"connectionstyle":"arc, angleA = 90, angleB = 0"
                                        })

            elif "PassInaccurate" in row["satisfiedEventsTypes"]:
                ax.annotate("",
                            xy=(row['endY'], row['endX']),
                            xytext=(row["y"], row["x"]),
                            arrowprops={'arrowstyle': "-|>,head_width=.7,head_length=.9",
                                        'fc': "#7400b8",
                                        'ec': "#7400b8",
                                        "connectionstyle": "angle3, angleA = 0, angleB = 95"})

        else:
            if 'passAccurate' in row["satisfiedEventsTypes"]:
                ax.annotate("",
                            xy=(row['endY'], row['endX']),
                            xytext=(row["y"], row["x"]),
                            arrowprops={'arrowstyle': "-|>,head_width=.7,head_length=.9",
                                        'fc': '#76c893',
                                        'ec': '#76c893'},
                            zorder=1)

            elif "PassInaccurate" in row["satisfiedEventsTypes"]:
                ax.annotate("",
                            xy=(row['endY'], row['endX']),
                            xytext=(row["y"], row["x"]),
                            arrowprops={'arrowstyle': "-|>,head_width=.7,head_length=.9",
                                        'fc': "#7400b8",
                                        'ec': "#7400b8"},
                            zorder=1)

    return None


def plotVerticalAndKeyPassMap(df, playerId, ax, time=None):
    pdf = df[df['playerId'] == playerId]
    if time is not None:
        pdf = pdf[pdf["minute"] < time]

    pdf['dist1'] = np.sqrt((120 - pdf.x)**2 + (40 - pdf.y)**2)
    pdf['dist2'] = np.sqrt((120 - pdf.endX)**2 + (40 - pdf.endY)**2)
    pdf['distdiff'] = pdf['dist1'] - pdf['dist2']

    for index, row in pdf.iterrows():

        if 'passKey' in row["satisfiedEventsTypes"]:
            ax.scatter(row["y"], row["x"], color="#F5E76B", s=20, zorder=1)
            ax.scatter(
                row["y"],
                row["x"],
                color="#F5E76B",
                s=70,
                alpha=.3,
                zorder=1)
            ax.annotate("",
                        xy=(row['endY'], row['endX']),
                        xytext=(row["y"], row["x"]),
                        arrowprops={'arrowstyle': "-|>,head_width=.35,head_length=.5",
                                    'fc': '#F5E76B', 'ec': '#F5E76B'},
                        zorder=1)

        elif ((row["x"] < 60) & (row["endX"] < 60) & (row["distdiff"] >= 30)) | \
            ((row["x"] < 60) & (row["endX"] > 60) & (row["distdiff"] >= 15)) | \
                ((row["x"] > 60) & (row["endX"] > 60) & (row["distdiff"] >= 7)):  # 30 15 10
            #             if 'passAccurate' in row["satisfiedEventsTypes"]:
            ax.scatter(row["y"], row["x"], color="#F5706C", s=20, zorder=1)
            ax.scatter(
                row["y"],
                row["x"],
                color="#F5706C",
                s=70,
                alpha=.3,
                zorder=1)
            ax.annotate("",
                        xy=(row['endY'], row['endX']),
                        xytext=(row["y"], row["x"]),
                        arrowprops={'arrowstyle': "-|>,head_width=.35,head_length=.5",
                                    'fc': '#F5706C', 'ec': '#F5706C'},
                        zorder=1)

        elif ('passAccurate' in row["satisfiedEventsTypes"]) | ("passInaccurate" in row["satisfiedEventsTypes"]):
            ax.scatter(row["y"], row["x"], color="#555555", s=20, zorder=.5)
#                 ax.scatter(row["y"],row["x"],color="#777777",s=70,alpha=.3,zorder=.5)
            ax.annotate("",
                        xy=(row['endY'], row['endX']),
                        xytext=(row["y"], row["x"]),
                        arrowprops={'arrowstyle': "-|>,head_width=.3,head_length=.45",
                                    'fc': '#555555',
                                    'ec': '#555555'},
                        zorder=.5)


def plotScatterMap(df, playerId, ax, time=None):
    df = df[df["satisfiedEventsTypes"].apply(
        str).str.contains("touch", na=False)]
    pdf = df[df['playerId'] == playerId]
    if time is not None:
        pdf = pdf[pdf["minute"] < time]

    x = pdf['x']
    y = pdf['y']
    endX = pdf['endX']
    endY = pdf['endY']
    meanX = pdf["x"].median()
    meanY = pdf["y"].median()

    ax.scatter(y, x, color="#555555", s=20, marker="h", zorder=1)
    ax.scatter(y, x, color="#555555", s=100, marker="h", alpha=.7, zorder=1)
#     ax.scatter(meanY,meanX,color=awayColor,s=200,marker="h",zorder=1)
#     ax.scatter(meanY,meanX,color=home,s=450,marker="h",alpha=.3,zorder=1)
    ax.scatter(meanY, meanX, facecolor="#cccccc", edgecolor='gold', s=300 * 4,
               marker="h", alpha=.35,
               linewidth=3, linestyle="--",
               zorder=99)
    ax.scatter(meanY, meanX, facecolor="#ffffff", edgecolor='gold', s=335 * 2,
               marker="h", alpha=1,
               linewidth=3, linestyle="--",
               label='Mål', zorder=99)
#     ax.annotate(f"{pdict[playerId]}",
#                             xy=(meanY,meanX),
#                             xytext=(meanY,meanX-5),
#                             fontweight="bold",
#                             arrowprops={'arrowstyle':"-|>,head_width=.7,head_length=.9",
#                                            'fc':"white",
#                                            'ec':"white"},
#                             zorder=1)
    #ax.scatter(endY,endX,cmap=colorB,s=100,zorder=1)
    #ax.scatter(endY,endX,cmap=colorB,s=350,alpha=.3,zorder=1)

    return None


def passSonerMap(df, playerId, ax):
    pdf = df[df['playerId'] == playerId]
    cmap = mpl.colors.LinearSegmentedColormap.from_list(
        'cmap', ["#13B9D6", "#D61327"])
    colors = cmap(pdf['count'] / pdf['count'].max())
    multiplier = 2 * np.pi / 24
    bars = ax.bar(pdf['angle_bin'] * multiplier,
                  pdf['avg_length'],
                  width=0.2,
                  bottom=0,
                  alpha=0.9,
                  color=colors,
                  zorder=3)

    ax.set_xticklabels([])
    ax.set_yticks([])
    # ax_sub.grid(True, alpha=.5)
    ax.grid(False)
    # ax_sub.spines['polar'].set_visible(True)
    ax.spines['polar'].set_visible(False)

    # ax_sub.spines['polar'].set_color(main_color)
    ax.patch.set_alpha(0)
#     return axes
    return ax


def plotHeatMap(df, playerId, ax):
    df = df[df["satisfiedEventsTypes"].apply(
        str).str.contains("touch", na=False)]
    if playerId is not None:
        pdf = df[df['playerId'] == playerId]
    pdf = df
    cmap = mpl.colors.LinearSegmentedColormap.from_list(
        'cmap', ["#131313", "#D61327"])  # 13B9D6

    kde = sns.kdeplot(
        pdf['y'],
        pdf['x'],
        shade=True,
        shade_lowest=False,
        alpha=.9,
        n_lavels=10,
        cmap=cmap,
        ax=ax)
#     pos.invert_xaxis()
    return None


def plotConvexfull(df, playerId, ax):
    df = df[df["satisfiedEventsTypes"].apply(
        str).str.contains("touch", na=False)]
    pdf = df[df['playerId'] == playerId]
    maxX, maxY = pdf[["x", "y"]].mean() + pdf[['x', 'y']].std()
    minX, minY = pdf[["x", "y"]].mean() - pdf[['x', 'y']].std()
    covX = []
    covY = []
    for index, row in pdf.iterrows():
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
            #             ax.scatter(points[:,1],points[:,0],color="blue")
            ax.plot(points[simplex, 1], points[simplex, 0],
                    linestyle='-.', color="#F5E76B", linewidth=1)
#             ax.plot(points[hull.vertices,1],points[hull.vertices,0],linestyle='-.',color="white",linewidth=.3)
            ax.fill(points[hull.vertices, 1], points[hull.vertices, 0],
                    fc="white", ec='white', linewidth=6, hatch="///" * 3, alpha=.01)
    else:
        pass
#         pos.scatter(points[:,1],points[:,0],color='blue',s=8)
#     pos.set_title(name,color=whiteTheme["textColor"],fontweight='bold',fontsize=12)


def plotBinStatHeatmap(pitch, ax, df, playerId, font, cmap, alpha):
    pdf = df[df['playerId'] == playerId]

    # bin_statistic = pitch.bin_statistic_positional(df["x"], df["y"], statistic='count',
    # positional='full', normalize=True)

    # pitch.heatmap_positional(bin_statistic, ax=ax['pitch'][idx],
    # cmap=cmap, edgecolors='#495E62',alpha=1, linewidth=.05)

    # labels = pitch.label_heatmap(bin_statistic, color=text_color, fontsize=18,
    #                             ax=ax['pitch'][idx], ha='center', va='center',
    #                             str_format='{:.0%}',fontproperties=font.prop)

    stats = pitch.bin_statistic(pdf["x"], pdf["y"],
                                statistic='count',
                                normalize=True)

    pitch.heatmap(stats, edgecolors='black', cmap=cmap, ax=ax, alpha=alpha)

    path_eff = [path_effects.Stroke(linewidth=0.5, foreground='seagreen')]

    text = pitch.label_heatmap(stats,
                               color='white',
                               ax=ax,
                               fontsize=14,
                               ha='center',
                               va='center',
                               alpha=.5,
                               path_effects=path_eff,
                               str_format='{:.0%}')


def plotHeatMap2(df, playerId, pitch, ax, time=None, time2=None):
    if playerId is not None:
        df = df[df["playerId"] == playerId]
    if time is not None:
        df = df[df["minute"] < time]
    if time2 is not None:
        df = df[df["minute"] > time2]
    cmapA = LinearSegmentedColormap.from_list(
        "my_cmap", [pitchColor, "#442D2D", "#852626", "#CB1C1C", "#FF0000"], N=100)
    stats = pitch.bin_statistic(df["x"], df["y"], bins=(12, 8))
    pitch.heatmap(stats, edgecolors='none', cmap=cmapA, alpha=.5, ax=ax)


def plotHexbin(pitch, df, playerId, ax, time=None):
    pdf = df[df['playerId'] == playerId]
    x = pdf["endX"]
    y = pdf["endY"]
    cmap = colors.ListedColormap(["#222222",
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
                                  "#E13746"])
    pitch.hexbin(
        x,
        y,
        edgecolors='white',
        gridsize=(
            20,
            9),
        cmap=cmap,
        ax=ax,
        bins="log")


def plotDefensiveLine(df, ax, defs, mids, teamId=65, time=None, color=None):
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
    dfD = df[(df["playerId"] == defs[0][0]) | (df["playerId"] == defs[1][0]) | (
        df["playerId"] == defs[2][0]) | (df["playerId"] == defs[3][0])]
    dfM = df[(df["playerId"] == mids[0][0]) | (df["playerId"] == mids[1][0]) | (
        df["playerId"] == mids[2][0]) | (df["playerId"] == mids[3][0]) | (df["playerId"] == mids[4][0])]

    dAveX = dfD["x"].median()
    dAveY = dfD["y"].mean()
    mAveX = dfM["x"].median()
    mAveY = dfM["y"].mean()
    ax.plot((0, 80), (120 - dAveY, 120 - dAveY),
            "#14FFFF", linestyle="-.", linewidth=1.2)
    ax.plot((0, 80), (120 - mAveY, 120 - mAveY),
            "#14FFFF", linestyle="-.", linewidth=1.2)


def plotDefensiveAct(df, playerId, ax):
    df = df[
        (df['satisfiedEventsTypes'].apply(str).str.contains('tackleLost')) | (
            df['satisfiedEventsTypes'].apply(str).str.contains('tackleWon')) | (
            df['satisfiedEventsTypes'].apply(str).str.contains('interceptionAll')) | (
                df['satisfiedEventsTypes'].apply(str).str.contains('outfielderBlock')) | (
                    df['satisfiedEventsTypes'].apply(str).str.contains('interceptionWon')) | (
                        df['satisfiedEventsTypes'].apply(str).str.contains('outfielderBlockedPass')) | (
                            df['satisfiedEventsTypes'].apply(str).str.contains('clearanceTotal'))]
    pdf = df[(df["playerId"] == playerId)]
    ax.plot(pdf["y"], pdf["x"], "o")


def carryPlot(df, ax, teamId, playerId, carryDist):
    df = df[df["teamId"] == teamId]
    df = df[["playerId", "x", "y", "endX", "endY"]]
    df['startX'] = df['endX'].shift(+1)
    df['startY'] = df['endY'].shift(+1)
    df['carry1'] = np.sqrt((120 - df.startX)**2 + (40 - df.startY)**2)
    df['carry2'] = np.sqrt((120 - df.x)**2 + (40 - df.y)**2)
    df['carrydist'] = df['carry1'] - df['carry2']
    df = df.query(f"carrydist>={carryDist} and playerId=={playerId}").dropna()
    print("Carry:", len(df))
    print("CarryDist mean:", df["carrydist"].mean())
#     Lines = pitch.lines(xstart=df["startX"],ystart=df["startY"],xend=df["x"],yend=df["y"],
#                         cmap=cmapA,comet=True,linewidth=3,linestyle="-.",ax=ax)
#     for idx,row in df.iterrows():
#         ax.annotate("",
#                 xy=(row['y'],row['x']),
#                 xytext=(row["startY"],row["startX"]),
#                 arrowprops={'arrowstyle':"-|>,head_width=.3,head_length=.45",
#                             'fc':'#555555',
#                             'ec':'#555555'},
#                 zorder=.5)
    ax.plot((df["startY"], df["y"]), (df['startX'], df['x']),
            "#7280D6", linestyle="-.", linewidth=3.2, zorder=.5)
#     ax.scatter(df["startY"],df["startX"],color="white",zorder=3,ec="#7280D6",lw=3,s=40)
#     ax.scatter(df["startY"],df["startX"],facecolor="#ffffff",edgecolor='#71C1D6',s=15,
#                 marker="h",alpha=1,
#                 linewidth=3,linestyle="-.",
#                 label='Mål',zorder=99)
#     ax.scatter(df["startY"],df["startX"],facecolor="#cccccc",edgecolor='#71C1D6',s=60,
#         marker="h",alpha=.35,
#         linewidth=3,linestyle="-.",
#         zorder=99)

    ax.scatter(df["startY"], df["startX"],color="#D672CF",s=20,zorder=1)  
    ax.scatter(df["startY"], df["startX"],color="#D672CF",s=70,alpha=.3,zorder=1)
