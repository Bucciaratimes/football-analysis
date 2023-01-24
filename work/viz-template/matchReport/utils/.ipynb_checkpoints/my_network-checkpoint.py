import pandas as pd
import numpy as np
import seaborn as sns
from PIL import Image
from math import pi
import scipy.stats
from selenium import webdriver
import warnings
import os

import matplotlib as mpl
from matplotlib.colors import to_rgba
import matplotlib.pyplot as plt
from matplotlib.markers import MarkerStyle
import matplotlib.image as mpimg
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
from matplotlib.projections import get_projection_class
from matplotlib.projections import get_projection_class
import matplotlib.cm as cm


from mplsoccer import Pitch, add_image, VerticalPitch
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from utils.metadata import *

import main as setDf
from imageio import imread
from skimage.transform import resize
import math

from matplotlib import colors
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.image as image


playerNameColor = "#1A1F21"

textColor = "gray"
discribeColor = "#6D6065"
lineColor = '#3D3337'

homeColor = "crimson"
awayColor = '#0033ff'

arrow_shift = 1.5 ##Units by which the arrow moves from its original position
shrink_val = 1 ##Units by which the arrow is shortened from the end_points

    
x = 'x_median'
end_x = 'x_median_end'
y = 'y_median'
end_y = 'y_median_end'

def pass_line_template(ax, x, y, end_x, end_y, passerNum, receiverNum, line_color, width):

    if abs( (end_y) - (y) ) > abs( end_x - x ):

            if receiverNum > passerNum:

                ax.annotate('', 
                            xy=(end_y+arrow_shift, end_x), 
                            xytext=(y+arrow_shift, x), 
                            zorder=1,
                            arrowprops=dict(arrowstyle="-|>,head_width=.6,head_length=.8", linestyle="--", color="#4A5EB8", 
                                            shrinkA=shrink_val, shrinkB=shrink_val, 
                                            linewidth=width, alpha=.88))

            elif passerNum > receiverNum:

                ax.annotate('', 
                            xy=(end_y - arrow_shift, end_x), 
                            xytext=(y - arrow_shift, x),
                            zorder=1,
                            arrowprops=dict(arrowstyle="-|>,head_width=.6,head_length=.8", linestyle="--", color="#B94B5F", 
                                            shrinkA=shrink_val, shrinkB=shrink_val, 
                                            linewidth=width, alpha=.88))

    elif abs( (end_y) - (y) ) <= abs( end_x - x ):

            if receiverNum > passerNum:
                ax.annotate("", 
                            xy=(end_y, end_x + arrow_shift), 
                            xytext=(y, x + arrow_shift),
                            arrowprops=dict(arrowstyle="-|>,head_width=.6,head_length=.8", linestyle="--", color="#4A5EB8",
                                            shrinkA=shrink_val, shrinkB=shrink_val, 
                                            linewidth=width, alpha=.88))

            elif passerNum > receiverNum:

                ax.annotate("", 
                            xy=(end_y, end_x - arrow_shift), 
                            xytext=(y, x - arrow_shift),
                            arrowprops=dict(arrowstyle="-|>,head_width=.6,head_length=.8", linestyle="--", color="#B94B5F",
                                            shrinkA=shrink_val, shrinkB=shrink_val, 
                                            linewidth=width, alpha=.88))
    
def pass_line_template_shrink(ax, idx, x, y, end_x, end_y, passerNum, receiverNum, line_color, width, dist_delta=1.2):
    dist = math.hypot(end_x - x, end_y - y)
    angle = math.atan2(end_y-y, end_x-x)
    upd_x = x + (dist - dist_delta) * math.cos(angle)
    upd_y = y + (dist - dist_delta) * math.sin(angle)
#     width = passes_between['width'][idx]*.4
    pass_line_template(ax, x, y, upd_x, upd_y, passerNum, receiverNum, line_color=line_color, width=width)


def plot_passnet(average_locs_and_count, passes_between, axes, color):
    axes.scatter(
        average_locs_and_count[y],
        average_locs_and_count[x],
        s=average_locs_and_count['marker_size']*1.3, 
        marker="h",
        alpha=1,
        facecolor=color,
        edgecolor='#E3B409',
        linewidth=3,
        linestyle="--",
        label='Mål',
    )
    axes.scatter(
        average_locs_and_count[y],
        average_locs_and_count[x],
        s=average_locs_and_count['marker_size']*2, 
        marker="h",
        alpha=.3,
        facecolor=color,
        edgecolor='#E3B409',
        linewidth=3,
        linestyle="--",
    )

    for index, row in average_locs_and_count.iterrows():
        axes.annotate(row['passRecipientName'],
                       xy=(row[y]-5, row[x]),
                       c=playerNameColor,
                       va='baseline',
                       ha='center',
                       size=11,
                       alpha=1,
                       weight=550,
                       fontname='serif',
                       zorder=99,
                     )
    for idx, row in passes_between.iterrows():
        
        pass_line_template_shrink(
             axes,idx,
             row[x],row[y],
             row[end_x],row[end_y],
             row["playerKitNumber"],
             row["playerKitNumber_Receipt"],
             lineColor,
             width=row['width']*.4)

    
#     axes.text(x=30,y=92,s=f'{homeScore}',color='red', fontsize=200, alpha=.33)
#     axes.text(x=30,y=92,s=f'{awayScore}',color='blue', fontsize=200, alpha=.33)

#     axes.text(x=35,y=124,s=f'{homeFormation}',color='#111111', fontsize=28, fontname="cmb10")
#     axes.text(x=36,y=124,s=f'{awayFormation}',color='#111111', fontsize=28, fontname="cmb10")
    
#     axes.text(x=13, y=130, s=f'{homeName}-Network (Avg.Age {homeAge})',fontsize=22,color='#000000',fontname="cmb10")
#     axes.text(x=17, y=130, s=f'{awayName}-Network (Avg.Age {awayAge})',fontsize=22,color='#000000',fontname="cmb10")
    
    
def main(match_data, axHome, axAway):
    
    matchId = match_data['matchId']
    homeId = match_data['home']['teamId']
    homeFormation = match_data['home']['formations'][0]['formationName']

    awayId = match_data['away']['teamId']
    awayFormation = match_data['away']['formations'][0]['formationName']

    matches_df = setDf.createMatchesDF(match_data)

    homeName = matches_df['home'][matchId]['name']
    homeScore = matches_df['home'][matchId]['scores']['fulltime']
    homeAge = matches_df['home'][matchId]['averageAge']

    awayName = matches_df['away'][matchId]['name']
    awayScore = matches_df['away'][matchId]['scores']['fulltime']
    awayAge = matches_df['away'][matchId]['averageAge']
    
    events_df = setDf.createEventsDF(match_data)
    
    MAXLINEWIDTH = 10
    MAXMARKERSIZE = 1000
    COLORCODE = '#87CEEB'
    MINTRANSPARENCY = 0.3
    
    net_dict = {'home':homeId,'away':awayId}
    idx = 0
    for VENUE,teamId in net_dict.items():
        team_players_dict = {}
        for player in matches_df[VENUE][matchId]['players']:
            team_players_dict[player['playerId']] = player['name']


        match_events_df = events_df[events_df['matchId']==matchId].reset_index(drop=True)

        passes_df = match_events_df.loc[[
                row['displayName']=='Pass' for row in list(match_events_df['type'])
        ]].reset_index(drop=True)

        passes_df = passes_df[passes_df['teamId']==teamId].reset_index().drop('index', axis=1)
        passes_df = passes_df.loc[[
            row['displayName']=='Successful' for row in list(
                passes_df['outcomeType']
            )]].reset_index(drop=True)


        passes_df['playerName'] = [team_players_dict[i] for i in list(passes_df['playerId'])]
        passes_df['passRecipientId'] = passes_df['playerId'].shift(-1)
        passes_df['passRecipientName'] = passes_df['playerName'].shift(-1)
        passes_df.dropna(subset=['passRecipientName'],inplace=True)


        match_player_df = pd.DataFrame()
        player_names = []
        player_ids = []
        player_pos = []
        player_kit_number = []

        for player in matches_df[VENUE][matchId]['players']:
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

        location_formation = passes_df[['playerKitNumber', 'x', 'y']].copy()

        average_locs_and_count = location_formation.groupby(by='playerKitNumber').agg(
            {'x':['mean','median'], 'y':['mean','median','count']}
        )
        average_locs_and_count.columns = ['x_mean', 'x_median', 'y_mean', 'y_median', 'count']

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
        
        if idx == 0:   
            plot_passnet(average_locs_and_count, passes_between, axHome, home_color)
            idx += 1
        elif idx == 1:
            plot_passnet(average_locs_and_count, passes_between, axAway, away_color)

            
            
    axHome.text(x=24,y=82,s=f'{homeScore}',color=home_color, fontsize=200, alpha=.7)
    axAway.text(x=24,y=82,s=f'{awayScore}',color=away_color, fontsize=200, alpha=.7)

    axHome.text(x=11,y=124,s=f'{homeFormation} (Avg-Age {homeAge})',color='#111111', fontsize=28, fontname="serif")
    axAway.text(x=11,y=124,s=f'{awayFormation} (Avg-Age {awayAge})',color='#111111', fontsize=28, fontname="serif")
    
#     axHome.text(x=68, y=130, s=f'{homeName}-Network (Avg.Age {homeAge})',fontsize=22,color='#000000',fontname="cmb10")
#     axAway.text(x=68, y=130, s=f'{awayName}-Network (Avg.Age {awayAge})',fontsize=22,color='#000000',fontname="cmb10")

         
    return None

if __name__ =="__main__":
    main()