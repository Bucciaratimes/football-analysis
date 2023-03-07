import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import to_rgba
from mplsoccer.pitch import Pitch
from selenium import webdriver

import main
import visualizer

match_urls = [
    "https://www.whoscored.com/Matches/1491975/Live/Spain-LaLiga-2020-2021-Barcelona-Villarreal",
    "https://www.whoscored.com/Matches/1491984/Live/Spain-LaLiga-2020-2021-Celta-Vigo-Barcelona",
    "https://www.whoscored.com/Matches/1491995/Live/Spain-LaLiga-2020-2021-Barcelona-Sevilla",
    "https://www.whoscored.com/Matches/1492021/Live/Spain-LaLiga-2020-2021-Getafe-Barcelona",
    "https://www.whoscored.com/Matches/1492033/Live/Spain-LaLiga-2020-2021-Barcelona-Real-Madrid",
    "https://www.whoscored.com/Matches/1492047/Live/Spain-LaLiga-2020-2021-Deportivo-Alaves-Barcelona",
    "https://www.whoscored.com/Matches/1492327/Live/Spain-LaLiga-2020-2021-Barcelona-Real-Betis",
    "https://www.whoscored.com/Matches/1492008/Live/Spain-LaLiga-2020-2021-Atletico-Madrid-Barcelona",
    "https://www.whoscored.com/Matches/1492024/Live/Spain-LaLiga-2020-2021-Barcelona-Osasuna",
    "https://www.whoscored.com/Matches/1492054/Live/Spain-LaLiga-2020-2021-Cadiz-Barcelona",
    "https://www.whoscored.com/Matches/1492065/Live/Spain-LaLiga-2020-2021-Barcelona-Levante",
    "https://www.whoscored.com/Matches/1492121/Live/Spain-LaLiga-2020-2021-Barcelona-Real-Sociedad",
    "https://www.whoscored.com/Matches/1492089/Live/Spain-LaLiga-2020-2021-Barcelona-Valencia",
    "https://www.whoscored.com/Matches/1492060/Live/Spain-LaLiga-2020-2021-Real-Valladolid-Barcelona",
    "https://www.whoscored.com/Matches/1492070/Live/Spain-LaLiga-2020-2021-Barcelona-Eibar",
    'https://www.whoscored.com/Matches/1492096/Live/Spain-LaLiga-2020-2021-SD-Huesca-Barcelona',
    'https://www.whoscored.com/Matches/1491963/Live/Spain-LaLiga-2020-2021-Athletic-Bilbao-Barcelona',
    'https://www.whoscored.com/Matches/1492112/Live/Spain-LaLiga-2020-2021-Granada-Barcelona'
]
opponents = [
    'Villarreal', 'Celta-Vigo', 'Sevilla', 'Getafe', 'Real-Madrid', 'Alaves', 'Betis', 'Atletico',
    'Osasuna', 'Cadiz', 'Levante', 'Real-Sociedad', 'Valencia', 'Valladolid', 'Eibar'
]

teamId = 65

options = webdriver.ChromeOptions()    
driver = webdriver.Remote(
    command_executor='ylenium_driver_1:4444/wd/hub',
    options=options,
)




match_data = main.getMatchData(driver, match_urls[1])

matches_df = main.createMatchesDF(match_data)

events_df = main.createEventsDF(match_data)

matchId = match_data['matchId']

# data = main.getMatchData(driver, url='https://www.whoscored.com/Matches/1491963/Live/Spain-LaLiga-2020-2021-Athletic-Bilbao-Barcelona')

match_data = main.getTeamData(match_urls)

df_total = pd.io.json.json_normalize(match_data)

venue_list = df_total['venueName']

df_opponent = df_total[['home.name', 'away.name']]
opponent_list = []
for idx, row in df_opponent.iterrows():
    if row['home.name']=='Barcelona':
        opponent_list.append(row['away.name'])
    else:
        opponent_list.append(row['home.name'])

for i, data in enumerate(df_total['events']):
    df_events = pd.io.json.json_normalize(data)
    df_events['venue'] = venue_list[i]
    df_events.to_csv(f'/work/assets/whoscored/barcelona/match/2021/2021#{i}.csv')

df = pd.DataFrame(match_data)

player_dict = pd.DataFrame(df['playerIdNameDictionary'])

player_dict.to_csv('/work/assets/whoscored/barcelona/match/2021/player/player_dict.csv')
