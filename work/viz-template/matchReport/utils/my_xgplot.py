import json
import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from highlight_text import ax_text, fig_text
from matplotlib.colors import LinearSegmentedColormap
from mplsoccer import FontManager, VerticalPitch, add_image
from PIL import Image

import utils.probability_functions as pf
from utils.cleaning import align_dfs, chance_quality, create_team_df
from utils.metadata import *

white_theme1 = "#ffffff"
white_theme2 = "#131313"

def main(ax=None,ax1=None,ax2=None,ax3=None,match=None):
    base_url = 'https://understat.com/match/'
    url = base_url+match

    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'lxml')
    scripts = soup.find_all('script')

    strings = scripts[1].string

    index_start = strings.index("('")+2
    index_end = strings.index("')")
    json_data = strings[index_start:index_end]
    json_data = json_data.encode('utf8').decode('unicode_escape')
    data = json.loads(json_data)

    x = []
    y = []
    minute = []
    xG = []
    result = []
    team = []
    player = []
    shotType = []
    assist = []
    data_away = data['a']
    data_home = data['h']

    for index in range(len(data_home)):
        for key in data_home[index]:
            if key == 'X':
                x.append(data_home[index][key])
            if key == 'Y':
                y.append(data_home[index][key])
            if key == 'minute':
                minute.append(data_home[index][key])
            if key == 'h_team':
                team.append(data_home[index][key])
            if key == 'xG':
                xG.append(data_home[index][key])
            if key == 'result':
                result.append(data_home[index][key])
            if key == 'player':
                player.append(data_home[index][key])
            if key == 'player_assisted':
                assist.append(data_home[index][key])
            if key == 'shotType':
                shotType.append(data_home[index][key])

    for index in range(len(data_away)):
        for key in data_away[index]:
            if key == 'X':
                x.append(data_away[index][key])
            elif key == 'Y':
                y.append(data_away[index][key])
            elif key == 'minute':
                minute.append(data_away[index][key])
            elif key == 'a_team':
                team.append(data_away[index][key])
            elif key == 'xG':
                xG.append(data_away[index][key])
            elif key == 'result':
                result.append(data_away[index][key])
            elif key == 'player':
                player.append(data_away[index][key])
            elif key == 'player_assisted':
                assist.append(data_away[index][key])
            elif key == 'shotType':
                shotType.append(data_away[index][key])


    col_names = [ 'minute', 'team','player', 'x', 'y', 'xG', 'result', 'shotType','assist']
    df = pd.DataFrame([minute, team, player, x, y, xG ,result ,shotType, assist],index=col_names)
    df = df.T
    df = df.astype({'x':float, 'y':float, 'minute':int, 'xG':float,'player':str, 'shotType':str, 'assist':str,'team':str})

#     comp = str(input("please input match number.")) # ex #1
#     season = str(input("please input season."))
#     team = str(input("please input target team."))

#     path = f'/work/assets/understats/{season}/{team}/'
#     if not os.path.exists(path):
#         os.makedirs(path)
#     df.to_csv(path+comp+'.csv')

#     df = pd.read_csv(path+comp+'.csv')
    
    
    df_home, df_away = create_team_df(df)
    home_team, away_team = df_home['team'][0], df_away['team'][0]
    df_home_final, df_home_final1, df_away_final, df_away_final1 = align_dfs(df, df_home, df_away)
    home_min_final = list(df_home_final['minute'].unique())
    away_min_final = list(df_away_final['minute'].unique())
    home_cum_xG_final = np.array(df_home_final1)
    away_cum_xG_final = np.array(df_away_final1)
    home_total_xG = '{:.2f}'.format(round(home_cum_xG_final[-1], 2))
    away_total_xG = '{:.2f}'.format(round(away_cum_xG_final[-1], 2))

    # Get probability of all scorelines from 0-0 to 9-9
    home_goal_probs, away_goal_probs, scoreline_probs = pf.score_probability(float(home_total_xG),
                                                                             float(away_total_xG),
                                                                             num_goals=10)

    # Prepare data for plotting
    #create xs and ys for bar plots 
    home_xs, home_ys = zip(*home_goal_probs)
    away_xs, away_ys = zip(*away_goal_probs)

    #get number of goals for each team
    home_goals = len(df_home[df_home['result'] == 'Goal'])
    away_goals = len(df_away[df_away['result'] == 'Goal'])

    # Calculate win, loss and draw probabilities
    home_prob, away_prob, draw_prob = pf.win_loss_draw_probs(scoreline_probs)

    home_prob = int(round(home_prob*100, 0))
    draw_prob = int(round(draw_prob*100, 0))
    away_prob = int(round(away_prob*100, 0))

    #concat to list
    home_away_draw_probs = pd.DataFrame({'outcomes': ['home', 'away', 'draw'], 'probs': [home_prob, away_prob, draw_prob]})

    if ax is not None:
        print("0000000")
        plot_xg(ax,df_home,df_away,df_home_final,df_away_final,home_min_final,away_min_final,home_cum_xG_final,away_cum_xG_final)
    elif ax1 is not None:
        print("0000001")
        plot_probar(ax1,ax2,home_xs,away_xs,home_ys,away_ys,home_goals,away_goals)
    elif ax3 is not None:
        print("0000002")
        plot_probar2(ax3,home_away_draw_probs,home_prob,away_prob,draw_prob)
                    
    


def plot_xg(ax,df_home,df_away,df_home_final,df_away_final,home_min_final,away_min_final,home_cum_xG_final,away_cum_xG_final):
    



    #plot the step graphs
    ax.plot(home_min_final, home_cum_xG_final, drawstyle='steps-post',
            color=home_color, linewidth=5)

    ax.plot(away_min_final, away_cum_xG_final, drawstyle='steps-post',
            color=away_color, linewidth=5)

    for i in range(len(df_home)):
        if df_home['result'][i] == 'Goal':
            ax.scatter(df_home['minute'][i], df_home['cum_xG'][i], 
                        s=300, zorder=10, facecolor=home_color, label='Mål')
            ax.scatter(df_home['minute'][i], df_home['cum_xG'][i], 
                s=650, zorder=9, facecolor=home_color, alpha=0.3)
    for i in range(len(df_away)):
        if df_away['result'][i] == 'OwnGoal':
            ax.scatter(df_away['minute'][i], df_home['cum_xG'][i], 
                        s=300, zorder=10, facecolor=home_color, label='Mål')
            ax.scatter(df_away['minute'][i], df_home['cum_xG'][i], 
                        s=650, zorder=9, facecolor=home_color, alpha=0.3)

    #plot away goals
    for i in range(len(df_away)):
        if df_away['result'][i] == 'Goal':
            ax.scatter(df_away['minute'][i], df_away['cum_xG'][i], 
                        s=300, zorder=10, facecolor=away_color, label='Mål')
            ax.scatter(df_away['minute'][i], df_away['cum_xG'][i], 
                        s=650, zorder=9, facecolor=away_color, alpha=0.3)
    for i in range(len(df_home)):
        if df_home['result'][i] == 'OwnGoal':
            ax.scatter(df_home['minute'][i], df_away['cum_xG'][i], 
                        s=300, zorder=10, facecolor=away_color, label='Mål')
            ax.scatter(df_home['minute'][i], df_away['cum_xG'][i], 
                        s=650, zorder=9, facecolor=away_color, alpha=0.3)
            
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
        
    # Set x and y labels
    ax.set_xlabel('Minutes', color="#131313", fontsize=8)
    ax.set_ylabel('xG', color="#131313", fontsize=8)
    ax.set_xticks([0, 15, 30, 45, 60, 75, 90])
    add_ax_title(ax, 'xG-Flow')



def plot_probar(ax1,ax2,home_xs,away_xs,home_ys,away_ys,home_goals,away_goals):

    # ax1.set_facecolor(white_theme1)
    # ax2.set_facecolor(white_theme1)
    
    ax1.tick_params(axis='x', colors="#131313", labelsize=8)
    ax1.set_xticks(home_xs)
    ax1.tick_params(axis='y', colors="#131313", labelsize=7)

    # Set grid, ticks and frame
    #ax1.grid(axis='y', color='w', linestyle='--', zorder=1, alpha=0.5)
    ax1.tick_params(axis='both', which='both', left=False, bottom=False)
#     ax1.set_frame_on(False)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)


    # Set labels and text
#     ax1.set_xlabel('Score',
#                    color="#131313", fontweight='bold', size=14)
#     ax1.set_ylabel('Probability',
#                    color="#131313", fontweight='bold', size=14)

    # Annotate probabilities on the bars
    for i, value in enumerate(home_ys):
            if value >= 1:
                    ax1.text(i, value+0.5, f'{int(value)}%',
                             color="#131313", ha="center", fontweight='bold', fontsize=12, zorder=15)
                 
    # ------- ax1 -------- #
    ax1.bar(home_xs, home_ys,
            facecolor=white_theme1, edgecolor=home_color, zorder=10, alpha=1)
    for i in home_xs:
        if i == home_goals:
            ax1.bar(i, home_ys[i],
            color=home_color, zorder=10, alpha=1)


    # ------- ax2 ---------- #
    ax2.bar(away_xs, away_ys,
            facecolor=white_theme1, edgecolor=away_color, zorder=10, alpha=1)
    for i in away_xs:
        if i == away_goals:
            ax2.bar(i, away_ys[i],
            color=away_color, zorder=10, alpha=1)
            
    ax2.tick_params(axis='both', which='both', left=False, bottom=False)
#     ax2.set_frame_on(False)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)



def plot_probar2(ax,home_away_draw_probs,home_prob,away_prob,draw_prob):

    #set up our base layer
    ax.tick_params(axis='x', bottom=False, labelsize=12, colors=white_theme1)
    ax.tick_params(axis='y', left=False, labelsize=12, colors=white_theme1)
    
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    
    # Plot bars
    home = ax.barh(0.5, home_away_draw_probs['probs'][0], edgecolor=home_color,
                   fill=True, facecolor=home_color,align="center",
                   linewidth=3, height=0.8)
    draw = ax.barh(0.5, home_away_draw_probs['probs'][2],
                   left=home_away_draw_probs['probs'][0], edgecolor=text_color, align="center",
                   facecolor=text_color, fill=True, linewidth=3, height=0.8)
    away = ax.barh(0.5, home_away_draw_probs['probs'][1],
                   left=home_away_draw_probs['probs'][0]+home_away_draw_probs['probs'][2], edgecolor=away_color, align="center",
                   facecolor=away_color, fill=True, linewidth=3, height=0.8)

    # Set texts
    # Home
    ax.text(x=home_prob/2, y=0.5, s=f'{home_prob}%',
            color='w', ha='center', size=32, fontweight='bold')
    # Draw
    ax.text(x=home_prob+draw_prob/2, y=0.5, s=f'Draw:{draw_prob}%',
            color='w', ha='center', size=32, fontweight='bold')
    # Away
    ax.text(x=home_prob+draw_prob+away_prob/2, y=0.5, s=f'{away_prob}%',
            color='w', ha='center', size=32, fontweight='bold')
