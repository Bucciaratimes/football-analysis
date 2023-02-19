import glob
import json
import os
import pickle
import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
import numpy as np
from lxml import html
import sys

def get_player_data(player_ids):
    
    """
    understats.comから選手のデータ取得する。
    
    Parameters
    ----------
    player_ids : int
        対象の選手ID。
    """
    
    for player_id in player_ids:
        
        url =f'https://understat.com/player/{player_id}'
        html = requests.get(url)
        soup = BeautifulSoup(html.content,'lxml')

        scripts = soup.find_all('script')
        strings = scripts[3].string
        indexStart = strings.index("('")+2
        indexEnd = strings.index("')")
        json_data = strings[indexStart:indexEnd]
        json_data = json_data.encode('utf8').decode('unicode_escape')

        data = json.loads(json_data)
        # data

        player = []
        playerId = []
        situation = []
        shotType = []
        player_assisted =[]
        lastAction = []
        x = []
        y = []
        xg = []
        result = []
        season = []
        matchId = []
        if len(data) == 0:
            break
        for i in range(len(data)):
            for key in data[i]:
                if key=='player':
                    player.append(data[i][key])
                if key=='player_id':
                    playerId.append(data[i][key])
                if key=='situation':
                    situation.append(data[i][key])
                if key=='shotType':
                    shotType.append(data[i][key])
                if key=='X':
                    x.append(data[i][key])
                if key=='Y':
                    y.append(data[i][key])
                if key=='xG':
                    xg.append(data[i][key])
                if key=='result':
                    result.append(data[i][key])
                if key=='season':
                    season.append(data[i][key])
                if key=='match_id':
                    matchId.append(data[i][key])

        columns = ['player', 'player_id', 'situation', 'shot_type', 'x', 'y', 'xG', 'result', 'season', 'match_id']
        df_understat = pd.DataFrame([player, playerId, situation, shotType, x, y, xg, result, season, matchId], index=columns)

        df_understat = df_understat.T
        df_understat = df_understat.apply(pd.to_numeric,errors='ignore')

        pitch_height = 120
        pitch_width = 80
        df_understat['x'] = df_understat['x'].apply(lambda x:x*pitch_height)
        df_understat['y'] = df_understat['y'].apply(lambda x:x*pitch_width)

        player = df_understat["player"][0]
        player = player.replace(" ", "_")
        print(player)
        df_understat.to_csv(f"/work/assets/understats/player_stats/{player}.csv")
        
def get_player_ids(team):
    
        url =f'https://understat.com/team/{team}/2022'
        html = requests.get(url)
        soup = BeautifulSoup(html.content,'lxml')
        scripts = soup.find_all('script')
        strings = scripts[3].string
        indexStart = strings.index("('")+2
        indexEnd = strings.index("')")
        json_data = strings[indexStart:indexEnd]
        json_data = json_data.encode('utf8').decode('unicode_escape')
        data = json.loads(json_data)
        player_ids = []
        for idx, _data in enumerate(data):
            if "id" in _data:
                player_ids.append(_data["id"])
                continue
        return player_ids
        
if __name__ == "__main__":
    
    player_ids = get_player_ids(sys.argv[1])
    print(player_ids)
    get_player_data(player_ids)