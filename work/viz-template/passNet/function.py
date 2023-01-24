import main_ver03 as main03
import os
import pickle
import pandas as pd
import numpy as np
import seaborn as sns
import math
from math import pi
import scipy.stats
import matplotlib as mpl
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.projections import get_projection_class
from mplsoccer import Pitch, add_image, VerticalPitch, FontManager
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from config import *
import matplotlib.patheffects as path_effects
from adjustText import adjust_text

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
                            arrowprops=dict(arrowstyle="-|>,head_width=.6,head_length=.8", linestyle="-.", color=line_color(norm(epv)), 
                                            shrinkA=shrink_val, shrinkB=shrink_val, 
                                            linewidth=width*1.2, alpha=1))

            elif passerNum > receiverNum:
                ax.annotate('', 
                            xy=(end_y - arrow_shift, end_x), 
                            xytext=(y - arrow_shift, x),
                            zorder=1,
                            arrowprops=dict(arrowstyle="-|>,head_width=.6,head_length=.8", linestyle="-.", color=line_color(norm(epv)),
                                            shrinkA=shrink_val, shrinkB=shrink_val, 
                                            linewidth=width*1.2, alpha=1))

    elif abs( (end_y) - (y) ) <= abs( end_x - x ):

            if receiverNum > passerNum:
                ax.annotate("", 
                            xy=(end_y, end_x + arrow_shift), 
                            xytext=(y, x + arrow_shift),
                            arrowprops=dict(arrowstyle="-|>,head_width=.6,head_length=.8", linestyle="-.", color=line_color(norm(epv)),
                                            shrinkA=shrink_val, shrinkB=shrink_val, 
                                            linewidth=width*1.2, alpha=1))

            elif passerNum > receiverNum:

                ax.annotate("", 
                            xy=(end_y, end_x - arrow_shift), 
                            xytext=(y, x - arrow_shift),
                            arrowprops=dict(arrowstyle="-|>,head_width=.6,head_length=.8", linestyle="-.", color=line_color(norm(epv)),
                                            shrinkA=shrink_val, shrinkB=shrink_val, 
                                            linewidth=width*1.2, alpha=1))
    
def pass_line_template_shrink(ax, idx, x, y, end_x, end_y, passerNum, receiverNum, line_color, epv, norm, passes_between, dist_delta=2):
    dist = math.hypot(end_x - x, end_y - y)
    angle = math.atan2(end_y-y, end_x-x)
    upd_x = x + (dist - dist_delta) * math.cos(angle)
    upd_y = y + (dist - dist_delta) * math.sin(angle)
    width = passes_between['width'][idx]*.15
    pass_line_template(ax, x, y, upd_x, upd_y, passerNum, receiverNum, line_color=line_color, width=width, epv=epv, norm=norm)

texts = []
def plot_passnet(ax,average_locs_and_count,passes_between,color,lineColor):
    ax.scatter(
        average_locs_and_count[y],
        average_locs_and_count[x],
        s=average_locs_and_count['marker_size']**2*.01, 
        marker="h",
        alpha=1,
        facecolor="#171733",  #color,
        edgecolor='#E3B409',
        linewidth=3,
        linestyle="--",
        label='Mål',
    )
    ax.scatter(
        average_locs_and_count[y],
        average_locs_and_count[x],
        s=average_locs_and_count['marker_size']**2*.015, 
        marker="h",
        alpha=.25,
        facecolor=color,
        edgecolor='#E3B409',
        linewidth=3,
        linestyle="--",
    )

    for index, row in average_locs_and_count.iterrows():
        if len(row['passRecipientName'].split(" "))>=3:
            try:
                first = row['passRecipientName'].split(" ")[0].title()
                second = row['passRecipientName'].split(" ")[1].title()
                third = row['passRecipientName'].split(" ")[2].title()
                name = first[0] + "." + second[0] + "." + third
            except IndexError:
                name = row['passRecipientName'].split(" ")[0].title()
        else:
            try:
                first = row['passRecipientName'].split(" ")[0].title()
                second = row['passRecipientName'].split(" ")[1].title()
                name = first[0] + "." + second
            except IndexError:
                name = row['passRecipientName'].split(" ")[0].title()
        
        
        annotater = ax.annotate(
                    row["playerKitNumber"],
                    xy=(row[y], row[x]),
                    c="#f8f8f8",
                    va='center',
                    ha='center',
                    size=22,
                    alpha=1,
                    weight=888,
                    fontproperties=monoBFont.prop,
                    zorder=99) 
#         annotater = ax.annotate(
#                     name,
#                     xy=(row[y], row[x]),
#                     c=playerNameColor,
#                     va='baseline',
#                     ha='center',
#                     size=17,
#                     alpha=1,
#                     weight=888,
#                     fontproperties=monoBFont.prop,
#                     zorder=99)
#         texts.append(annotater)
        


#     [text.set_path_effects([mpl.patheffects.withStroke(
#         linewidth=3, foreground="black"
#     )]) for text in texts]

#     adjust_text(
#         texts, autoalign='xy',
#         only_move={'points':'xy', 'text':'xy'}, 
#         force_objects=(0.5, 1.5), force_text=(0.5, 1.5), 
#         force_points=(0.5, 1.5)
#     )   
        
    norm = plt.Normalize(passes_between["EPV"].min(), passes_between["EPV"].max())
    
    #points = np.array([passes_between[x],passes_between[y]]).T.reshape(-1, 1, 2)
    #segments = np.concatenate([points[:-1], points[1:]], axis=1)
    #lc = LineCollection(segments, cmap='viridis', norm=norm)

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
        
def main(axes,teamId,teamName,season,gw,cmap1,cmap2,isTable=False):
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
    opponentName = homeName if awayName == teamName else awayName

    venues = {'home':homeId,'away':awayId}
    idx = 0
    for venue,teamId in venues.items():
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
        print(type(match_player_df["playerId"][0]))
        print(type(passes_df["playerId"][0]))

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
        passes_between[y] = 80-(passes_between[y]*.8)
        passes_between[end_y] = 80-(passes_between[end_y]*.8)

        average_locs_and_count[x] = average_locs_and_count[x]*1.2
        average_locs_and_count[y] = 80-(average_locs_and_count[y]*.8)

        #cmap1 = mpl.colors.LinearSegmentedColormap.from_list('cmap1', ["#FF8C00","#FF6000","#FF3400","#FF0800","#FF0023"])
        #cmap2 = mpl.colors.LinearSegmentedColormap.from_list("cmap2", ["#00CEFF","#00A3FF","#0077FF","#004BFF","#003CFF"])
        column_labels=["Passer", "Receiver", "Pass-Count"]
        if idx == 0:   
            plot_passnet(axes[0],average_locs_and_count,passes_between,homeColor,lineColor=cmap1)
            axes[0].set_title(f"{homeName}", color="#f8f8f8", fontsize=18, path_effects=path_eff, fontproperties=monoBFont.prop)

        
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

            idx += 1
        elif idx == 1:
    #         axes[idx].text(x=17, y=110, s=f'{awayName}-Network (Avg.Age {awayAge})',fontsize=22,color=textColor,fontname="serif")
            plot_passnet(axes[1],average_locs_and_count,passes_between,awayColor,lineColor=cmap2)
            axes[1].set_title(f"{awayName}", color="#f8f8f8", fontsize=18, path_effects=path_eff, fontproperties=monoBFont.prop)
            if isTable:
                passes_between = changeNumberToName(passes_between,passes_df)
                values = passes_between[["playerKitNumber", "playerKitNumber_Receipt", "pass_count"]].sort_values("pass_count",ascending=False).iloc[:4,:].values
                axes[3].axis('tight')
                axes[3].axis('off')
                tbl = axes[3].table(cellText=values,colLabels=column_labels,loc="center",bbox=[0, 0, 1, 1])
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
                
    return passes_between,average_locs_and_count

