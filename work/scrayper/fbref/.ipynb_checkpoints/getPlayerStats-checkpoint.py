import csv
import getopt
import math
import re
import statistics
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup, Comment
from scipy import stats


def get_gk_data(url=None, player_name=None):
    
    if url is None:
        url = f'https://fbref.com/en/players/1e26e376/Sergio-Romero'
    
    if player_name is None:
        player_name = str(input('please input player name!!!!'))
    
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    table = soup.select('table')
    tbody_list = []
    for _table in table:
        tbody_list.append(_table.tbody)

    seasons = tbody_list[0](attrs={'data-stat':'season'})
    season_list = []
    for season in seasons:
        season_list.append(season.text)

    games =  tbody_list[0](attrs={'data-stat':'games_gk'})
    game_list = []
    for game in games:
        game_list.append(game.text)

    starts = tbody_list[0](attrs={'data-stat':'games_starts_gk'})
    start_list = []
    for start in starts:
        start_list.append(start.text)

    minutes = tbody_list[0](attrs={'data-stat':'minutes_gk'})
    minute_list = []
    for minute in minutes:
        minute_list.append(minute.text)

    againsts = tbody_list[0](attrs={'data-stat':'goals_against_gk'})
    against_list = []
    for against in againsts:
        against_list.append(against.text)

    against90s = tbody_list[0](attrs={'data-stat':'goals_against_per90_gk'})
    against90_list = []
    for against90 in against90s:
        against90_list.append(against90.text)

    shots_on_tgts = tbody_list[0](attrs={'data-stat':'shots_on_target_against'})
    shots_on_tgt_list = []
    for shots_on_tgt in shots_on_tgts:
        shots_on_tgt_list.append(shots_on_tgt.text)

    saves = tbody_list[0](attrs={'data-stat':'saves'})
    save_list = []
    for save in saves:
        save_list.append(save.text)

    save_pcts = tbody_list[0](attrs={'data-stat':'save_pct'})
    save_pct_list = []
    for save_pct in save_pcts:
        save_pct_list.append(save_pct.text)

    clean_sheets = tbody_list[0](attrs={'data-stat':'clean_sheets'})
    clean_sheet_list = []
    for clean_sheet in clean_sheets:
        clean_sheet_list.append(clean_sheet.text)

    clean_sheets_pcts = tbody_list[0](attrs={'data-stat':'clean_sheets_pct'})
    clean_sheet_pct_list = []
    for clean_sheet_pct in clean_sheets_pcts:
        clean_sheet_pct_list.append(clean_sheet_pct.text)


    psxg = tbody_list[1](attrs={'data-stat': 'psxg_gk'})
    psxg_list = []
    for _psxg in psxg:
        psxg_list.append(_psxg)
    psxg_list


    psnp = tbody_list[1](attrs={'data-stat': 'psnpxg_per_shot_on_target_against'})
    psnp_list = []
    for _psnp in psnp:
        psnp_list.append(_psnp)
    psnp_list


    net = tbody_list[1](attrs={'data-stat': 'psxg_net_gk'})
    net_list = []
    for _net in net:
        net_list.append(_net)
    net_list


    psxg90 = tbody_list[1](attrs={'data-stat': 'psxg_net_per90_gk'})
    psxg90_list = []
    for _psxg90 in psxg90:
        psxg90_list.append(_psxg90)
    psxg90_list


    launch = tbody_list[1](attrs={'data-stat': 'passes_pct_launched_gk'})
    launch_list = []
    for _launch in launch:
        launch_list.append(_launch)
    launch_list


    plaunch = tbody_list[1](attrs={'data-stat': 'pct_passes_launched_gk'})
    plaunch_list = []
    for _plaunch in plaunch:
        plaunch_list.append(_plaunch)
    plaunch_list


    lave = tbody_list[1](attrs={'data-stat': 'passes_length_avg_gk'})
    lave_list = []
    for _lave in lave:
        lave_list.append(_lave)
    lave_list


    gkave = tbody_list[1](attrs={'data-stat': 'goal_kick_length_avg'})
    gkave_list = []
    for _gkave in gkave:
        gkave_list.append(_gkave)
    gkave_list


    plave = tbody_list[1](attrs={'data-stat': 'passes_length_avg_gk'})
    plave_list = []
    for _plave in plave:
        plave_list.append(_plave)
    plave_list


    cross = tbody_list[1](attrs={'data-stat': 'crosses_gk'})
    cross_list = []
    for _cross in cross:
        cross_list.append(_cross)
    cross_list


    cstop = tbody_list[1](attrs={'data-stat': 'crosses_stopped_pct_gk'})
    cstop_list = []
    for _cstop in cstop:
        cstop_list.append(_cstop)
    cstop_list


    outside = tbody_list[1](
        attrs={'data-stat': 'def_actions_outside_pen_area_per90_gk'})
    outside_list = []
    for _outside in outside:
        outside_list.append(_outside)
    outside_list


    dist = tbody_list[1](attrs={'data-stat': 'avg_distance_def_actions_gk'})
    dist_list = []
    for _dist in dist:
        dist_list.append(_dist)
    dist_list
    
    with open(f'/work/assets/fbref/position/gk/{player_name}.csv', 'w') as csv_file:
        
        fieldnames = [
            'Season','Game','Start','Minute','Against', 'Against90', 
            'Sot', 'Saves', 'Save %', 'Clean-sheet', 'Clean-sheet %', 
            'Psxg', 'Psnp', 'Net','Psxg90', 'Launch', 'Plaunch', 
            'Lave', 'Gkave', 'Plave', 'Cross', 'Cstop', 'Outside', 'Dist']
        
        writer = csv.DictWriter(csv_file,fieldnames=fieldnames)

        writer.writeheader()

        for (season,game, start, minute,against,against90, sot, \
             save, saveper,clean_sheet,clean_sheetper, psxg, psnp, \
             net, psxg90, launch, plaunch,lave, gkave, plave, cross, \
             cstop, outside, dist) in zip(season_list, game_list, start_list, minute_list, 
                                          against_list, against90_list, shots_on_tgt_list, 
                                          save_list, save_pct_list,clean_sheet_list, 
                                          clean_sheet_pct_list, psxg_list, psnp_list,net_list, 
                                          psxg90_list, launch_list, plaunch_list, lave_list, 
                                          gkave_list, plave_list, cross_list, cstop_list, 
                                          outside_list, dist_list):
            writer.writerow({
                'Season': season,
                'Game': game, 
                'Start':start, 
                'Minute': minute, 
                'Against': against, 
                'Against90':against90, 
                'Sot':sot,  
                'Saves':save, 
                'Save %':saveper, 
                'Clean-sheet':clean_sheet, 
                'Clean-sheet %':clean_sheetper,
                'Psxg':psxg,
                'Psnp':psnp,
                'Net':net,
                'Psxg90':psxg90,
                'Launch':launch,
                'Plaunch':plaunch,
                'Lave':lave,
                'Gkave':gkave,
                'Plave':plave,
                'Cross':cross,
                'Cstop':cstop,
                'Outside':outside,
                'Dist':dist
            })   
