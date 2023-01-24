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

from scipy.spatial import ConvexHull

from highlight_text import fig_text

from config import *


import main_ver03 as main03
import os
import pickle
import math
from math import pi
import scipy.stats
import matplotlib.patches as patches
from matplotlib.collections import LineCollection
from matplotlib.colors import to_rgba
from adjustText import adjust_text

def calPassComp(df,playerId):
    passDf = df[df["playerId"]==playerId]
    passAc = passDf[passDf["satisfiedEventsTypes"].apply(str).str.contains("PassAccurate",na=False)]
    passIc = passDf[passDf["satisfiedEventsTypes"].apply(str).str.contains("PassInaccurate",na=False)]
    try:
        passComp = round((len(passAc)/((len(passAc)+len(passIc))))*100,2)
    except:
        passComp = 0
    return passComp

def plotShotmap(pitch,ax,df,pId):
    df = df[df["playerId"]==pId]
    shotDf = df[df["satisfiedEventsTypes"].apply(str).str.contains('shotsTotal')]
    goal = df[df["satisfiedEventsTypes"].apply(str).str.contains('goal')]
    onTarget = df[df["satisfiedEventsTypes"].apply(str).str.contains('shotOnTarget')]
    offTarget = df[df["satisfiedEventsTypes"].apply(str).str.contains('shotOffTarget')]
    blocked = df[df["satisfiedEventsTypes"].apply(str).str.contains('shotBlocked')]
    cmap = mpl.colors.LinearSegmentedColormap.from_list('cmap', ["#131313","#f8f8f8","#ffffff"])
    for items in zip([onTarget,offTarget,blocked],["#ff5c8a","#4ea8de","#67b99a"]):
        for idx,row in items[0].iterrows():
            if row["y"] >= 45:
                if row["x"] >= 105:
                    scatter = pitch.scatter(row.x+4,row.y-3.5,color=pitchColor,marker="*",ax=ax,zorder=10,ec=items[1],lw=2,s=200)
                    Lines = pitch.lines(xstart=row.x,ystart=row.y,xend=row.x+4,yend=row.y-3.5,cmap=cmap,comet=True,lw=4,ax=ax,zorder=4)
                else:
                    scatter = pitch.scatter(row.x+10,row.y-3.5,color=pitchColor,marker="*",ax=ax,zorder=10,ec=items[1],lw=2,s=200)
                    Lines = pitch.lines(xstart=row.x,ystart=row.y,xend=row.x+10,yend=row.y-3.5,cmap=cmap,comet=True,lw=4,ax=ax,zorder=4)
            elif row["y"] <= 35:
                if row["x"] >= 105:
                    scatter = pitch.scatter(row.x+4,row.y+3.5,color=pitchColor,marker="*",ax=ax,zorder=10,ec=items[1],lw=2,s=200)
                    Lines = pitch.lines(xstart=row.x,ystart=row.y,xend=row.x+4,yend=row.y+3.5,cmap=cmap,comet=True,lw=4,ax=ax,zorder=4)
                else:
                    scatter = pitch.scatter(row.x+10,row.y+3.5,color=pitchColor,marker="*",ax=ax,zorder=10,ec=items[1],lw=2,s=200)
                    Lines = pitch.lines(xstart=row.x,ystart=row.y,xend=row.x+10,yend=row.y+3.5,cmap=cmap,comet=True,lw=4,ax=ax,zorder=4)
            else:
                if row["x"] >= 105:
                    scatter = pitch.scatter(row.x+4,row.y,color=pitchColor,marker="*",ax=ax,zorder=10,ec=items[1],lw=2,s=200)
                    Lines = pitch.lines(xstart=row.x,ystart=row.y,xend=row.x+4,yend=row.y,cmap=cmap,comet=True,lw=4,ax=ax,zorder=4)
                else:
                    scatter = pitch.scatter(row.x+10,row.y,color=pitchColor,marker="*",ax=ax,zorder=10,ec=items[1],lw=2,s=200)
                    Lines = pitch.lines(xstart=row.x,ystart=row.y,xend=row.x+10,yend=row.y,cmap=cmap,comet=True,lw=4,ax=ax,zorder=4)
                
    return [len(shotDf),len(goal),len(onTarget),len(offTarget),len(blocked)]


def plotPassMap(df,playerId,ax,time=None):
    pdf = df[df['playerId']==playerId]    
    if time is not None:
        pdf = pdf[pdf["minute"]<time]
        
    x = pdf['x']
    y = pdf['y']
    endX = pdf['endX']
    endY = pdf['endY']

    cmap = mpl.colors.LinearSegmentedColormap.from_list('cmap', ["#13B9D6","#e76f51","#D61327"])
    color = cmap(pdf["xT"]/pdf["xT"].max())
    sumXt = pdf["xT"].sum()
    
#     ax.scatter(y,x,color="#dc2f02",s=30)  
#     ax.scatter(y,x,color="#ffba08",s=80,alpha=.3)   

    ax.scatter(y,x,color=color,s=70,zorder=1)  
    ax.scatter(y,x,color=color,s=180,alpha=.3,zorder=1)  
    
    for index, row in pdf.iterrows():
        if row["dist"] > 36.57:
            if 'passAccurate' in row["satisfiedEventsTypes"]:
                ax.annotate("",
                       xy=(row['endY'], row['endX']),xytext=(row["y"],row["x"]),
                       arrowprops={'arrowstyle':"-|>,head_width=.4,head_length=.55",
                                   'fc':'#76c893',
                                   'ec':'#76c893',
                                    "connectionstyle":"angle3, angleA = 0, angleB = 95"
                                    #"connectionstyle":"arc, angleA = 90, angleB = 0"
                                  })
 
            elif "PassInaccurate" in row["satisfiedEventsTypes"]:
                ax.annotate("",
                            xy=(row['endY'],row['endX']),
                            xytext=(row["y"],row["x"]),
                            arrowprops={'arrowstyle':"-|>,head_width=.4,head_length=.55",
                                        'fc':"#7400b8",
                                        'ec':"#7400b8",
                                        "connectionstyle":"angle3, angleA = 0, angleB = 95"})

        else:
            if 'passAccurate' in row["satisfiedEventsTypes"]:
                ax.annotate("",
                            xy=(row['endY'],row['endX']),
                            xytext=(row["y"],row["x"]),
                            arrowprops={'arrowstyle':"-|>,head_width=.4,head_length=.55",
                                        'fc':'#76c893',
                                        'ec':'#76c893'},
                            zorder=1)
                            
            elif "PassInaccurate" in row["satisfiedEventsTypes"]:
                ax.annotate("",
                            xy=(row['endY'],row['endX']),
                            xytext=(row["y"],row["x"]),
                            arrowprops={'arrowstyle':"-|>,head_width=.4,head_length=.55",
                                        'fc':"#7400b8",
                                        'ec':"#7400b8"},
                            zorder=1)
                
    return sumXt

def plotVerticalAndKeyPassMap(df,playerId,ax,time=None):
    pdf = df[df['playerId']==playerId]    
    if time is not None:
        pdf = pdf[pdf["minute"]<time]

    pdf['dist1']=np.sqrt((120-pdf.x)**2 + (40-pdf.y)**2)
    pdf['dist2']=np.sqrt((120-pdf.endX)**2 + (40-pdf.endY)**2)
    pdf['distdiff'] = pdf['dist1']-pdf['dist2']
    keyCount = len(pdf[pdf["satisfiedEventsTypes"].apply(str).str.contains("passKey",na=False)])
    verticalCount = 0
    for index, row in pdf.iterrows():
        
        if 'passKey' in row["satisfiedEventsTypes"]:
            ax.scatter(row["y"],row["x"],color="#F5E76B",s=20,zorder=1)  
            ax.scatter(row["y"],row["x"],color="#F5E76B",s=70,alpha=.3,zorder=1) 
            ax.annotate("",
                        xy=(row['endY'],row['endX']),
                        xytext=(row["y"],row["x"]),
                        arrowprops={'arrowstyle':"-|>,head_width=.35,head_length=.5",
                                    'fc':'#F5E76B','ec':'#F5E76B'},
                        zorder=1)
            
        elif ((row["x"]<60)&(row["endX"]<60)&(row["distdiff"]>=30)) | \
           ((row["x"]<60)&(row["endX"]>60)&(row["distdiff"]>=15)) | \
           ((row["x"]>60)&(row["endX"]>60)&(row["distdiff"]>=7)):  #30 15 10
#             if 'passAccurate' in row["satisfiedEventsTypes"]: 
                ax.scatter(row["y"],row["x"],color="#F5706C",s=20,zorder=1)  
                ax.scatter(row["y"],row["x"],color="#F5706C",s=70,alpha=.3,zorder=1) 
                ax.annotate("",
                            xy=(row['endY'],row['endX']),
                            xytext=(row["y"],row["x"]),
                            arrowprops={'arrowstyle':"-|>,head_width=.35,head_length=.5",
                                        'fc':'#F5706C','ec':'#F5706C'},
                            zorder=1)
                verticalCount+=1
                
        elif ('passAccurate' in row["satisfiedEventsTypes"]) | ("passInaccurate" in row["satisfiedEventsTypes"]):
                ax.scatter(row["y"],row["x"],color="#555555",s=20,zorder=.5)  
#                 ax.scatter(row["y"],row["x"],color="#777777",s=70,alpha=.3,zorder=.5) 
                ax.annotate("",
                            xy=(row['endY'],row['endX']),
                            xytext=(row["y"],row["x"]),
                            arrowprops={'arrowstyle':"-|>,head_width=.3,head_length=.45",
                                        'fc':'#555555',
                                        'ec':'#555555'},
                            zorder=.5)
    return (keyCount,verticalCount)
    

def plotScatterMap(df,playerId,ax,time=None):
    df = df[df["satisfiedEventsTypes"].apply(str).str.contains("touch",na=False)]
    pdf = df[df['playerId']==playerId]    
    if time is not None:
        pdf = pdf[pdf["minute"]<time]
        
    x = pdf['x']
    y = pdf['y']
    endX = pdf['endX']
    endY = pdf['endY']
    meanX = pdf["x"].median()
    meanY = pdf["y"].median()
    
    ax.scatter(y,x,color="#555555",s=20,marker="h",zorder=1)  
    ax.scatter(y,x,color="#555555",s=100,marker="h",alpha=.7,zorder=1) 
#     ax.scatter(meanY,meanX,color=awayColor,s=200,marker="h",zorder=1)
#     ax.scatter(meanY,meanX,color=home,s=450,marker="h",alpha=.3,zorder=1)
    ax.scatter(meanY,meanX,facecolor="#cccccc",edgecolor='gold',s=300*4, 
        marker="h",alpha=.35,
        linewidth=3,linestyle="--",
        zorder=99)
    ax.scatter(meanY,meanX,facecolor="#ffffff",edgecolor='gold',s=335*2, 
        marker="h",alpha=1,
        linewidth=3,linestyle="--",
        label='Mål',zorder=99)
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

def passSonerMap(df,playerId,ax):
    pdf = df[df['playerId']==playerId]
    cmap = mpl.colors.LinearSegmentedColormap.from_list('cmap', ["#13B9D6","#D61327"])
    colors = cmap(pdf['count']/pdf['count'].max())
    multiplier = 2*np.pi/24
    bars = ax.bar(pdf['angle_bin']*multiplier, 
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

def plotHeatMap(df,playerId,ax):
    df = df[df["satisfiedEventsTypes"].apply(str).str.contains("touch",na=False)]
    if playerId is not None:
        pdf = df[df['playerId']==playerId]
    pdf = df
    cmap = mpl.colors.LinearSegmentedColormap.from_list('cmap', ["#13B9D6","#D61327"])
    
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

def plotConvexfull(df,playerId,ax,color):
    df = df[df["satisfiedEventsTypes"].apply(str).str.contains("touch",na=False)]
    pdf = df[df['playerId']==playerId]
    maxX,maxY = pdf[["x","y"]].mean() + pdf[['x','y']].std()
    minX,minY = pdf[["x","y"]].mean() - pdf[['x','y']].std()
    covX = []
    covY = []
    for index, row in pdf.iterrows():
        if row["x"] < maxX and row["y"] < maxY:
            if row["x"] > minX and row["y"] > minY:
                covX.append(row["x"])
                covY.append(row["y"])
        else:
            continue

    covDf = pd.DataFrame(columns=["x","y"])
    covDf["x"] = covX
    covDf["y"] = covY
    
    points = covDf[['x','y']].values
    if len(points) > 2:
        hull = ConvexHull(covDf[['x','y']])
        for simplex in hull.simplices:
#             ax.scatter(points[:,1],points[:,0],color="blue")
            ax.plot(points[simplex,1],points[simplex,0],linestyle='-.',color="#F5E76B",linewidth=1)
#             ax.plot(points[hull.vertices,1],points[hull.vertices,0],linestyle='-.',color="white",linewidth=.3)
            ax.fill(points[hull.vertices,1],points[hull.vertices,0],fc=color,ec='white',linewidth=6,hatch="///"*3,alpha=.01)
    else:
        pass
#         pos.scatter(points[:,1],points[:,0],color='blue',s=8)
#     pos.set_title(name,color=whiteTheme["textColor"],fontweight='bold',fontsize=12)
    
def plotBinStatHeatmap(pitch,ax,df,playerId,font,cmap,alpha):
    pdf = df[df['playerId']==playerId]
    
    # bin_statistic = pitch.bin_statistic_positional(df["x"], df["y"], statistic='count',
    #                                               positional='full', normalize=True)

    # pitch.heatmap_positional(bin_statistic, ax=ax['pitch'][idx],
    #                         cmap=cmap, edgecolors='#495E62',alpha=1, linewidth=.05)

    # labels = pitch.label_heatmap(bin_statistic, color=text_color, fontsize=18,
    #                             ax=ax['pitch'][idx], ha='center', va='center',
    #                             str_format='{:.0%}',fontproperties=font.prop)

    stats = pitch.bin_statistic(pdf["x"], pdf["y"], 
                                statistic='count', 
                                normalize=True)
    
    pitch.heatmap(stats, edgecolors='black',cmap=cmap,ax=ax,alpha=alpha)
    
    path_eff = [path_effects.Stroke(linewidth=2, foreground='black'),path_effects.Normal()]
    
    text = pitch.label_heatmap(stats,
                               color='white',
                               ax=ax,
                               fontsize=15, 
                               ha='center',
                               va='center',
                               alpha=1,
                               path_effects=path_eff,
                               str_format='{:.0%}')
    
def plotHeatMap2(df,ax,pitch,playerId=None):
    if playerId is not None:
        df = df[df["playerId"]==playerId]
    cmapA = LinearSegmentedColormap.from_list("my_cmap", ["#131313","#442D2D", "#852626", "#CB1C1C", "#FF0000"], N=100)
    stats = pitch.bin_statistic(df["x"], df["y"], bins=(12,8))
    pitch.heatmap(stats, edgecolors='none', cmap=cmapA, alpha=.5, ax=ax)
    
def plotHexbin(pitch,df,playerId,ax,time=None):
    pdf = df[df['playerId']==playerId]
    x = pdf["endX"]
    y = pdf["endY"]
    cmap = colors.ListedColormap(["#222222", "#2A2224", "#3A2027", "#421F28", "#54202B", "#65202E", "#782231",
                              "#892433", "#9B2838", "#AC2B3A", "#BE2F3E", "#CF3341", "#E13746"])
    pitch.hexbin(x, y, edgecolors='white', gridsize=(20, 9), cmap=cmap, ax=ax, bins="log")
    
def plotDefensiveLine(df,ax,defs,mids,teamId=65,time=None,color=None):
    if teamId is not None:
        df = df[df["teamId"]!=teamId]
    elif time is not None:
        if isinstance(time,tuple):
            if len(time)==2:
                if time[0] < time[1]:
                    early = time[0]
                    later = time[1]
                else:
                    early = time[1]
                    later = time[0]
                    
                df = df[(df["minute"]>=early)&(df["minute"]<=later)]               
            else:
                raise Exception
        else:        
            df = df[df["minute"]<=time]
        
    df = df[df["satisfiedEventsTypes"].apply(str).str.contains("touch",na=False)]        
    dfD = df[(df["playerId"]==defs[0][0])|(df["playerId"]==defs[1][0])|(df["playerId"]==defs[2][0])|(df["playerId"]==defs[3][0])]
    dfM = df[(df["playerId"]==mids[0][0])|(df["playerId"]==mids[1][0])|(df["playerId"]==mids[2][0])|(df["playerId"]==mids[3][0])|(df["playerId"]==mids[4][0])]
    
    dAveX = dfD["x"].median()
    dAveY = dfD["y"].mean()
    mAveX = dfM["x"].median()
    mAveY = dfM["y"].mean()
    ax.plot((0,80),(120-dAveY,120-dAveY),"#14FFFF",linestyle = "-.",linewidth=1.2)
    ax.plot((0,80),(120-mAveY,120-mAveY),"#14FFFF",linestyle = "-.",linewidth=1.2)
    
    
def plotDefensiveAct(df,playerId,ax):
    df = df[(df['satisfiedEventsTypes'].apply(str).str.contains('tackleLost')) | (df['satisfiedEventsTypes'].apply(str).str.contains('tackleWon'))
                      |(df['satisfiedEventsTypes'].apply(str).str.contains('interceptionAll'))| (df['satisfiedEventsTypes'].apply(str).str.contains('outfielderBlock'))
                      |(df['satisfiedEventsTypes'].apply(str).str.contains('interceptionWon')) | (df['satisfiedEventsTypes'].apply(str).str.contains('outfielderBlockedPass'))
                      |(df['satisfiedEventsTypes'].apply(str).str.contains('clearanceTotal'))]
    pdf = df[(df["playerId"]==playerId)]
    ax.plot(pdf["y"],pdf["x"],"o")
    
def carryPlot(df,ax,playerId,teamId=None,carryDist=(9,120)):
    df = df[df["teamId"]==teamId]
    df = df[["playerId","x","y","endX","endY"]]
    df['startX'] = df['endX'].shift(+1)
    df['startY'] = df['endY'].shift(+1)
    df['carry1']=np.sqrt((120-df.startX)**2 + (40-df.startY)**2)
    df['carry2']=np.sqrt((120-df.x)**2 + (40-df.y)**2)
    df['carrydist'] = df['carry1']-df['carry2']
    df = df.query(f"(carrydist>={carryDist[0]} and carrydist<={carryDist[1]}) and playerId=={playerId}").dropna()
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
    ax.plot((df["startY"],df["y"]),(df['startX'],df['x']),"#7280D6",linestyle="-.",linewidth=3.2,zorder=.5)
#     ax.scatter(df["startY"],df["startX"],color="white",zorder=3,ec="#7280D6",lw=3,s=40)
#     ax.scatter(df["startY"],df["startX"],facecolor="#ffffff",edgecolor='#71C1D6',s=15, 
#                 marker="h",alpha=1,
#                 linewidth=3,linestyle="-.",
#                 label='Mål',zorder=99)
#     ax.scatter(df["startY"],df["startX"],facecolor="#cccccc",edgecolor='#71C1D6',s=60, 
#         marker="h",alpha=.35,
#         linewidth=3,linestyle="-.",
#         zorder=99)
    
    ax.scatter(df["startY"],df["startX"],color="#D672CF",s=20,zorder=1)  
    ax.scatter(df["startY"],df["startX"],color="#D672CF",s=70,alpha=.3,zorder=1) 
    return len(df)



path_eff = [path_effects.Stroke(linewidth=2, foreground='black'),
            path_effects.Normal()]

def changeNumberToName(passes_between,passes_df):
    passerNames = []
    receiverNames = []
    keyNumValName = {}
    for i in range(len(passes_df)):
        try:
            keyNumValName[passes_df.loc[i,"playerKitNumber"]] = passes_df.loc[i,"playerName"]
        except:
            pass
    for idx,row in passes_between[["playerKitNumber", "playerKitNumber_Receipt"]].iterrows():
        try:
            passer = keyNumValName[row["playerKitNumber"]]
            receiver = keyNumValName[row["playerKitNumber_Receipt"]]
            passerNames.append(passer)
            receiverNames.append(receiver)
        except:
            pass
    try:
        passes_between["playerKitNumber"] = passerNames
        passes_between["playerKitNumber_Receipt"] = receiverNames
    except:
        pass
    
    return passes_between

def pass_line_template(ax, x, y, end_x, end_y, passerNum, receiverNum, line_color, width, epv, norm):

    # annotationをヨコにシフトするかタテにシフトするか
    if abs( (end_y) - (y) ) > abs( end_x - x ):
            # パスを出した時と受けた時で場合分け
            if receiverNum > passerNum:
                ax.annotate('', 
                            xy=(end_y+arrow_shift, end_x), 
                            xytext=(y+arrow_shift, x), 
                            zorder=1,
                            arrowprops=dict(arrowstyle="-|>,head_width=.3,head_length=.5", linestyle="-.", color=line_color(norm(epv)), 
                                            shrinkA=shrink_val, shrinkB=shrink_val, 
                                            linewidth=width, alpha=1))

            elif passerNum > receiverNum:
                ax.annotate('', 
                            xy=(end_y - arrow_shift, end_x), 
                            xytext=(y - arrow_shift, x),
                            zorder=1,
                            arrowprops=dict(arrowstyle="-|>,head_width=.3,head_length=.5", linestyle="-.", color=line_color(norm(epv)),
                                            shrinkA=shrink_val, shrinkB=shrink_val, 
                                            linewidth=width, alpha=1))

    elif abs( (end_y) - (y) ) <= abs( end_x - x ):

            if receiverNum > passerNum:
                ax.annotate("", 
                            xy=(end_y, end_x + arrow_shift), 
                            xytext=(y, x + arrow_shift),
                            arrowprops=dict(arrowstyle="-|>,head_width=.3,head_length=.5", linestyle="-.", color=line_color(norm(epv)),
                                            shrinkA=shrink_val, shrinkB=shrink_val, 
                                            linewidth=width, alpha=1))

            elif passerNum > receiverNum:

                ax.annotate("", 
                            xy=(end_y, end_x - arrow_shift), 
                            xytext=(y, x - arrow_shift),
                            arrowprops=dict(arrowstyle="-|>,head_width=.3,head_length=.5", linestyle="-.", color=line_color(norm(epv)),
                                            shrinkA=shrink_val, shrinkB=shrink_val, 
                                            linewidth=width, alpha=1))
    
def pass_line_template_shrink(ax, idx, x, y, end_x, end_y, passerNum, receiverNum, line_color, epv, norm, passes_between, dist_delta=2):
    dist = math.hypot(end_x - x, end_y - y)
    angle = math.atan2(end_y-y, end_x-x)
    upd_x = x + (dist - dist_delta) * math.cos(angle)
    upd_y = y + (dist - dist_delta) * math.sin(angle)
    width = passes_between['width'][idx]*.1
    pass_line_template(ax, x, y, upd_x, upd_y, passerNum, receiverNum, line_color=line_color, width=width, epv=epv, norm=norm)

texts = []
def plot_passnet(ax,average_locs_and_count,passes_between,color,lineColor,kitNum):
    for idx,row in average_locs_and_count.iterrows():
        if (row["playerKitNumber"]==kitNum):
            ax.scatter(
                row[y],
                row[x],
                s=row['marker_size']*2, 
                marker="h",
                alpha=1,
                facecolor="#131313",
                edgecolor=color,
                linewidth=0,
#                 linestyle="-",
                label='Mål',
                zorder=90)
            ax.scatter(
                row[y],
                row[x],
                s=row['marker_size']*2, 
                marker="h",
                alpha=.5,
                facecolor=color,
                edgecolor=color,
                linewidth=1,
#                 linestyle="-",
                label='Mål',
                zorder=90)
        else:
            ax.scatter(
                row[y],
                row[x],
                s=row['marker_size']*1.5, 
                marker="h",
                alpha=1,
                facecolor="#131313",
                edgecolor='#f8f8f8',
                linewidth=1,
#                 linestyle="--",
                label='Mål',
                zorder=90)

    for index, row in average_locs_and_count.iterrows():
        if len(row['passRecipientName'].split(" "))>=3:
            try:
                first = row['passRecipientName'].split(" ")[0].title()
                second = row['passRecipientName'].split(" ")[1].title()
                third = row['passRecipientName'].split(" ")[2].title()
                name = first[0] + "." + second[0] + "." + third[0]
            except IndexError:
                name = row['passRecipientName'].split(" ")[0].title()
        else:
            try:
                first = row['passRecipientName'].split(" ")[0].title()
                second = row['passRecipientName'].split(" ")[1].title()
                name = first[0] + "." + second[0]
            except IndexError:
                name = row['passRecipientName'].split(" ")[0].title()

        annotater = ax.annotate(row["playerKitNumber"],
#             name,
                    xy=(row[y], row[x]),
                    c="#f8f8f8",
                    va='center',
                    ha='center',
                    size=12,
                    alpha=1,
                    weight=888,
                    fontproperties=monoBFont.prop,
                    zorder=99) 
        
    norm = plt.Normalize(passes_between["EPV"].min(), passes_between["EPV"].max())

    for idx, row in passes_between.iterrows():
        pass_line_template_shrink(
             ax,idx,
             row[x],row[y],
             row[end_x],row[end_y],
             row["playerKitNumber"],
             row["playerKitNumber_Receipt"],
             lineColor,
             row["EPV"],
             norm,
             passes_between
        ) 
        
def main(axes,teamId,teamName,season,gw,cmap1,kitNum,isTable=False):
    ## Read
    with open(file=f"/work/assets/whoscored/{teamName}/match/{season}/matchData/#{gw}.json", mode="rb") as file:
        match_data = pickle.load(file)

    matchId = match_data['matchId']
    homeId = match_data['home']['teamId']
    homeFormation = match_data['home']['formations'][0]['formationName']

    awayId = match_data['away']['teamId']
    awayFormation = match_data['away']['formations'][0]['formationName']

    matches_df = main03.createMatchesDF(match_data)

    homeName = matches_df['home'][matchId]['name']
    homeScore = matches_df['home'][matchId]['scores']['fulltime']
    homeAge = matches_df['home'][matchId]['averageAge']

    awayName = matches_df['away'][matchId]['name']
    awayScore = matches_df['away'][matchId]['scores']['fulltime']
    awayAge = matches_df['away'][matchId]['averageAge']

    events_df = main03.createEventsDF(match_data)
    events_df = main03.addEpvToDataFrame(events_df)
    events_df = events_df.dropna(subset=["endX"])
    events_df["playerId"] = events_df["playerId"].astype(int)
    
    opponentId = homeId if awayId == teamId else awayId
    opponentName = homeName if awayName == "Barcelona" else awayName
    
#     axes.set_title(f"vs {opponentName}", color="#f8f8f8", fontsize=14, path_effects=path_eff, fontproperties=monoBFont.prop)

    venues = {'home':homeId,'away':awayId}
    for venue,venueId in venues.items():
        if venueId != teamId:
            continue
        elif venueId != teamId:
            continue
        team_players_dict = {}
        for player in matches_df[venue][matchId]['players']:
            team_players_dict[player['playerId']] = player['name']

        match_events_df = events_df.reset_index(drop=True)
        passes_df = match_events_df[match_events_df["type"]=="Pass"].reset_index(drop=True)

        passes_df = passes_df[passes_df['teamId']==teamId].reset_index().drop('index', axis=1)
        passes_df = passes_df[passes_df['outcomeType']=='Successful'].reset_index(drop=True)

        passes_df['playerName'] = [team_players_dict[i] for i in list(passes_df['playerId'])]
        passes_df['passRecipientId'] = passes_df['playerId'].shift(-1)
        passes_df['passRecipientName'] = passes_df['playerName'].shift(-1)
        passes_df.dropna(subset=['passRecipientName'],inplace=True)


        match_player_df = pd.DataFrame()
        player_names = []
        player_ids = []
        player_pos = []
        player_kit_number = []

        for player in matches_df[venue][matchId]['players']:
            player_names.append(player['name'])
            player_ids.append(player['playerId'])
            player_pos.append(player['position'])
            player_kit_number.append(player['shirtNo'])

        match_player_df['playerId'] = player_ids
        match_player_df['playerName']=player_names
        match_player_df['playerPos']=player_pos
        match_player_df['playerKitNumber']=player_kit_number
        
        passes_df = passes_df.merge(
            match_player_df,
            on=['playerId', 'playerName'],
            how='left',
            validate='m:1'
        )

        match_player_df.rename(columns={
              'playerId': 'passRecipientId', 'playerName': 'passRecipientName'  
            },inplace=True)

        passes_df = passes_df.merge(
            match_player_df,
            on=['passRecipientId', 'passRecipientName'],
            how='left',
            validate='m:1',
            suffixes=['', '_Receipt']
        )

        passes_df = passes_df[(passes_df['playerPos'] != 'Sub')]

        passes_formation = passes_df[[
                'id', 'playerKitNumber', 'playerKitNumber_Receipt']].copy()

        location_formation = passes_df[['playerKitNumber', 'x', 'y',"EPV"]].copy()

        average_locs_and_count = location_formation.groupby(by='playerKitNumber').agg(
            {'x':['mean','median'], 'y':['mean','median','count'], "EPV":["sum"]}
        )
        average_locs_and_count.columns = ['x_mean', 'x_median', 'y_mean', 'y_median', 'count', "EPV"]

        passes_between = passes_formation.groupby(
            by=["playerKitNumber","playerKitNumber_Receipt"])["id"].count().reset_index()

        passes_between.rename(columns={'id': 'pass_count'},inplace=True)

        passes_between = passes_between.merge(
            average_locs_and_count,
            left_on='playerKitNumber',
            right_index=True
        )
        passes_between = passes_between.merge(
            average_locs_and_count,
            left_on='playerKitNumber_Receipt',
            right_index=True,
            suffixes=['','_end']
        )

        passes_between['width'] = passes_between['pass_count'] / \
            passes_between['pass_count'].max() * MAXLINEWIDTH

        passes_between = passes_between.loc[(passes_between['pass_count']>4)]

        average_locs_and_count['marker_size'] = (
            average_locs_and_count['count'] / average_locs_and_count['count'].max() * MAXMARKERSIZE
        )

        color = np.array(to_rgba(COLORCODE))
        color = np.tile(color, (len(passes_between), 1))
        c_transparency = passes_between['pass_count'] / passes_between['pass_count'].max()
        c_transparency = (c_transparency * (1 - MINTRANSPARENCY)) + MINTRANSPARENCY
        color[:,3] = c_transparency
        passes_between['alpha'] = color.tolist()

        passes_between.reset_index(drop=True,inplace=True)

        average_locs_and_count['name'] = average_locs_and_count.index
        average_locs_and_count = average_locs_and_count.merge(match_player_df,on=['playerKitNumber'])

        passes_between[x] = passes_between[x]*1.2
        passes_between[end_x] = passes_between[end_x]*1.2
        passes_between[y] = (passes_between[y]*.8)
        passes_between[end_y] = (passes_between[end_y]*.8)

        average_locs_and_count[x] = average_locs_and_count[x]*1.2
        average_locs_and_count[y] = (average_locs_and_count[y]*.8)
        
        column_labels=["Passer", "Receiver", "Pass-Count"]
        plot_passnet(axes,average_locs_and_count,passes_between,homeColor,lineColor=cmap1,kitNum=kitNum)
        if isTable:
            passes_between = changeNumberToName(passes_between,passes_df)
            values = passes_between[["playerKitNumber", "playerKitNumber_Receipt", "pass_count"]].sort_values("pass_count",ascending=False).iloc[:4,:].values
            axes[2].axis('tight')
            axes[2].axis('off')
            tbl = axes[2].table(cellText=values,colLabels=column_labels,loc="center",bbox=[0, 0, 1, 1])
    #         tbl.set_fontsize(18)
            cells = tbl.get_celld()
            for cell in cells.values():
                cell.set(edgecolor=pitchLineColor,
                         facecolor="#131313",
                         height=10,
                         path_effects=path_eff)
                cell.set_text_props(color="white",fontsize=22,fontproperties=monoBFont.prop,fontweight="heavy")

            tbl[0, 0].set_facecolor('#363636')
            tbl[0, 1].set_facecolor("#363636")
            tbl[0, 2].set_facecolor("#363636")

#     return passes_between,average_locs_and_count

