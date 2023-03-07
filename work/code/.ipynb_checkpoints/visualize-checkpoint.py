import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import to_rgba
from mplsoccer.pitch import Pitch
from selenium import webdriver

import main

teams, match_links = main.getMatchLinks(main_url='https://www.whoscored.com/',
                                        comp_url='https://www.whoscored.com/Regions/206/Tournaments/4/Seasons/7889/Spain-LaLiga')

team_links = main.getTeamLinks('Barcelona', match_links)

team_data = main.getTeamData(team_links)


for data in team_data:

    matches_df = main.createMatchesDF(data)

    events_df = main.createEventsDF(data)

    matchId = data['matchId']

    team = 'Barcelona'
    teamId = 65

    if matches_df['venueName'].bool == 'Camp Nou':
        venue = 'home'
    else:
        venue = 'away'

    team_players_dict = {}
    for player in matches_df[venue][matchId]['players']:
        team_players_dict[player['playerId']] = player['name']

    match_events_df = events_df[events_df['matchId']
                                == matchId].reset_index(drop=True)

    passes_df = match_events_df.loc[[
        row['displayName'] == 'Pass' for row in list(match_events_df['type'])
    ]].reset_index(drop=True)

    passes_df = passes_df[passes_df['teamId'] ==
                          teamId].reset_index().drop('index', axis=1)

    passes_df = passes_df.loc[[
        row['displayName'] == 'Successful' for row in list(
            passes_df['outcomeType']
        )
    ]].reset_index(drop=True)

    playerIds = []
    for i in passes_df['playerId']:
        playerIds.append(int(i))

    passes_df['playerId'] = playerIds

    passes_df.insert(
        27,
        column='playerName',
        value=[
            team_players_dict[i] for i in list(passes_df['playerId'])
        ]
    )

    passes_df.insert(
        28,
        column='passRecipientId',
        value=passes_df['playerId'].shift(-1)
    )

    passes_df.insert(
        29,
        column='passRecipientName',
        value=passes_df['playerName'].shift(-1)
    )

    passes_df.dropna(subset=['passRecipientName'], inplace=True)

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
    match_player_df['playerName'] = player_names
    match_player_df['playerPos'] = player_pos
    match_player_df['playerKitNumber'] = player_kit_number

    passes_df = passes_df.merge(
        match_player_df,
        on=['playerId', 'playerName'],
        how='left',
        validate='m:1'
    )
    passes_df = passes_df.merge(
        match_player_df.rename({
            'playerId': 'passRecipientId', 'playerName': 'passRecipientName'
        }, axis='columns'),
        on=['passRecipientId', 'passRecipientName'],
        how='left',
        validate='m:1',
        suffixes=['', '_Receipt']
    )

    passes_df = passes_df[passes_df['playerPos'] != 'Sub']
    passes_formation = passes_df[[
        'id', 'playerKitNumber', 'playerKitNumber_Receipt']].copy()

    location_formation = passes_df[['playerKitNumber', 'x', 'y']]

    average_locs_and_count = location_formation.groupby('playerKitNumber').agg(
        {'x': ['mean', 'median'], 'y': ['mean', 'median', 'count']}
    )
    # average_locs_and_count = location_formation.groupby(
    #         'playerKitNumber').agg({'x': ['mean'], 'y': ['mean', 'count']})

    average_locs_and_count.columns = [
        'x_mean', 'x_median', 'y_mean', 'y_median', 'count']

    passes_formation['kitNo_max'] = passes_formation[[
        'playerKitNumber', 'playerKitNumber_Receipt'
    ]].max(axis='columns')

    passes_formation['kitNo_min'] = passes_formation[[
        'playerKitNumber', 'playerKitNumber_Receipt'
    ]].min(axis='columns')

    passes_between = passes_formation.groupby(
        ['kitNo_max', 'kitNo_min']
    )['id'].count().reset_index()

    passes_between.rename({'id': 'pass_count'}, axis='columns', inplace=True)

    passes_between = passes_between.merge(
        average_locs_and_count,
        left_on='kitNo_min',
        right_index=True)

    passes_between = passes_between.merge(
        average_locs_and_count,
        left_on='kitNo_max',
        right_index=True,
        suffixes=['', '_end']
    )

    max_lw = 10
    max_marker_size = 1000
    max_line_width = max_lw
    passes_between['width'] = passes_between['pass_count'] / \
        passes_between['pass_count'].max() * max_line_width

    average_locs_and_count['marker_size'] = (
        average_locs_and_count['count'] /
        average_locs_and_count['count'].max() *
        max_marker_size)

    min_transparency = 0.3
    color = np.array(to_rgba('white'))
    color = np.tile(color, (len(passes_between), 1))
    c_transparency = passes_between['pass_count'] / \
        passes_between['pass_count'].max()
    c_transparency = (c_transparency * (1 - min_transparency)
                      ) + min_transparency
    color[:, 3] = c_transparency
