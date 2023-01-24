#%%
import pandas as pd
import numpy as np
import ast
pd.options.mode.chained_assignment = None  # default='warn'

def load_data(season: str, gw: str, team=None, homeId=None) -> pd.DataFrame:
    
    if team is None:
        team = "barcelona"
    if int(season) >= 2122:
        df = pd.read_csv(f"/work/assets/whoscored/{team}/match/{season}/eventsData/new/{season}#{gw}.csv")   
    else:
        path = str(input("please input path  [????/{season}#{gw}.csv] "))
        df = pd.read_csv(path + f"/{season}#{gw}.csv")

    df["comp"] = gw
    
    if homeId is None:
        home_id = df['teamId'][0]
        away_id = df['teamId'][1]
    else:
        home_id = homeId
        away_id = df[df['teamId']!=homeId].loc[:,"teamId"].values[0]

    df_home = df[df['teamId'] == home_id]
    df_away = df[df['teamId'] == away_id]

    return df_home, df_away

def load_understat(gw,season=None,team=None):

    if season is None:
        season = "2122"
    if team is None:
        team = "Barcelona"

    df = pd.read_csv(f"/work/assets/understats/{season}/{team}/#{gw}.csv")
    
    
    home_team = df['team'].iloc[0]
    away_team = df['team'].iloc[-1]
    
    df_home = df[df['team'] == home_team].reset_index(drop=True)
    df_away = df[df['team'] == away_team].reset_index(drop=True)
    
    #extract goals and non goals
    #home
    df_home_goals = df_home[df_home['result'] == 'Goal']
    df_home_own_goals = df_home[df_home['result'] == 'OwnGoal']
    df_home_goals = pd.concat([df_home_goals, df_home_own_goals])
    df_home_non_goals = df_home[df_home['result'] != 'Goal']
    #away
    df_away_goals = df_away[df_away['result'] == 'Goal']
    df_away_own_goals = df_away[df_away['result'] == 'OwnGoal']
    df_away_goals = pd.concat([df_away_goals, df_away_own_goals])
    df_away_non_goals = df_away[df_away['result'] != 'Goal']
    
    return df_home_goals, df_home_non_goals, df_away_goals, df_away_non_goals


def get_average_locations(df_home, df_away):
    #find the first subsititution and filter the successful dataframe to be less than that minute
    home_subs = df_home[df_home['satisfiedEventsTypes'].str.contains('subOn', na=False)]
    home_subs = home_subs['minute'].reset_index(drop=True)
    num_home_subs = len(home_subs)
    df_home = df_home[df_home['minute'] < home_subs[0]]
    
    away_subs = df_away[df_away['satisfiedEventsTypes'].str.contains('subOn', na=False)]
    away_subs = away_subs['minute'].reset_index(drop=True)
    num_away_subs = len(home_subs)
    df_away = df_away[df_away['minute'] < away_subs[0]]
    

    home_avg_locations = df_home.groupby('playerId').agg({'x':['mean'],'y':['mean']})
    away_avg_locations = df_away.groupby('playerId').agg({'x':['mean'],'y':['mean']})
    
    return home_avg_locations, away_avg_locations


def get_pass_network_data(df_home: pd.DataFrame, df_away: pd.DataFrame):
    """
    Returns:
        home_avg_locations: Average position locations (x,y coordinates)
        home_pass_between: Number of passes between players
        away_avg_locations: Average position locations (x,y coordinates)
        away_pass_between: Number of passes between players
    """
    # Find passer and recipient
    df_home['passer'] = df_home['playerId']
    df_home['recipient'] = df_home['playerId'].shift(-1)
    df_away['passer'] = df_away['playerId']
    df_away['recipient'] = df_away['playerId'].shift(-1)
    
    # Filter for player accurate passes (accuratePass = passAccurate) (can change to progressive passes etc.)
    df_home_successful_pass = df_home[df_home['satisfiedEventsTypes'].str.contains('passAccurate', na=False)]
    df_away_successful_pass = df_away[df_away['satisfiedEventsTypes'].str.contains('passAccurate', na=False)]
    
    #find the first subsititution and filter the successful dataframe to be less than that minute
    home_subs = df_home[df_home['satisfiedEventsTypes'].str.contains('subOn', na=False)]
    home_subs = home_subs['minute'].reset_index(drop=True)
    num_home_subs = len(home_subs)
    if num_home_subs > 0:
        df_home_successful_pass = df_home_successful_pass[df_home_successful_pass['minute'] < home_subs[0]]
    else:
        df_home_successful_pass = df_home_successful_pass
    num_home_passes = len(df_home_successful_pass)
    
    away_subs = df_away[df_away['satisfiedEventsTypes'].str.contains('subOn', na=False)]
    away_subs = away_subs['minute'].reset_index(drop=True)
    num_away_subs = len(away_subs)
    if num_away_subs > 0:
        df_away_successful_pass = df_away_successful_pass[df_away_successful_pass['minute'] < away_subs[0]]
    else:
        df_away_successful_pass = df_away_successful_pass
    num_away_passes = len(df_away_successful_pass)
    
    #find the average locations and counts of the passes
    home_avg_locations = df_home_successful_pass.groupby('passer').agg({'x':['mean'],'y':['mean','count']})
    home_avg_locations.columns = ['x','y','count']

    away_avg_locations = df_away_successful_pass.groupby('passer').agg({'x':['mean'],'y':['mean','count']})
    away_avg_locations.columns = ['x','y','count']

    #find the number of passes between each player
    home_pass_between = df_home_successful_pass.groupby(['passer','recipient']).id.count().reset_index()
    home_pass_between.rename({'id':'pass_count'}, axis='columns', inplace=True)
    #merge the average location dataframe. We need to merge on the passer first then the recipient
    home_pass_between = home_pass_between.merge(home_avg_locations, left_on='passer', right_index=True)
    home_pass_between = home_pass_between.merge(home_avg_locations, left_on='recipient', right_index=True, suffixes=['', '_end'])
    
    #find the number of passes between each player
    away_pass_between = df_away_successful_pass.groupby(['passer','recipient']).id.count().reset_index()
    away_pass_between.rename({'id':'pass_count'}, axis='columns', inplace=True)
    #merge the average location dataframe. We need to merge on the passer first then the recipient
    away_pass_between = away_pass_between.merge(away_avg_locations, left_on='passer', right_index=True)
    away_pass_between = away_pass_between.merge(away_avg_locations, left_on='recipient', right_index=True, suffixes=['', '_end'])

    return home_avg_locations, home_pass_between, away_avg_locations, away_pass_between

#home_avg_locations, home_pass_between, away_avg_locations, away_pass_between = passNetworkData('2021', 'gw23')

def get_bar_plot_data(df_home: pd.DataFrame, df_away: pd.DataFrame, gw: str, team=None, season=None) -> list:
    
    if team is None:
        team = "barcelona"
    if season is None:
        season = "2122"

    df = pd.read_csv(f"/work/assets/understats/{season}/{team}/#{gw}.csv")
    
    home_team = df['team'].iloc[0]
    away_team = df['team'].iloc[-1]
    
    df_home_understat = df[df['team'] == home_team].reset_index(drop=True)
    df_away_understat = df[df['team'] == away_team].reset_index(drop=True)

    home_xg = round(df_home_understat['xG'].sum(), 2)
    away_xg = round(df_away_understat['xG'].sum(), 2)
    total_xg = home_xg + away_xg
    
    # Passes
    df_home_passes = df_home[(df_home['satisfiedEventsTypes'].apply(str).str.contains('passAccurate', na=False)) | (df_home['eventId'].apply(str).str.contains('passInaccurate', na=False))]
    
    df_away_passes = df_away[(df_away['satisfiedEventsTypes'].apply(str).str.contains('passAccurate', na=False)) | (df_away['eventId'].apply(str).str.contains('passInaccurate', na=False))]
    
    home_passes_deep = len(df_home_passes[df_home_passes['x'] < 50])
    away_passes_deep = len(df_away_passes[df_away_passes['x'] < 50])
    
    # PPDA 3 7 8 12 49 56 74  
    df_home_def_actions = df_home[(df_home['satisfiedEventsTypes'].apply(str).str.contains('tackleLost')) | (df_home['satisfiedEventsTypes'].apply(str).str.contains('tackleWon'))
                                  |(df_home['satisfiedEventsTypes'].apply(str).str.contains('interceptionAll'))| (df_home['satisfiedEventsTypes'].apply(str).str.contains('outfielderBlock'))
                                  |(df_home['satisfiedEventsTypes'].apply(str).str.contains('interceptionWon')) | (df_home['satisfiedEventsTypes'].apply(str).str.contains('outfielderBlockedPass'))
                                  |(df_home['satisfiedEventsTypes'].apply(str).str.contains('clearanceTotal'))]
    
    df_away_def_actions = df_away[(df_away['satisfiedEventsTypes'].apply(str).str.contains('tackleLost')) | (df_away['eventId'].apply(str).str.contains('tackleWon'))
                                  |(df_away['satisfiedEventsTypes'].apply(str).str.contains('interceptionAll'))| (df_away['satisfiedEventsTypes'].apply(str).str.contains('outfielderBlock'))
                                  |(df_away['satisfiedEventsTypes'].apply(str).str.contains('interceptionWon')) | (df_away['satisfiedEventsTypes'].apply(str).str.contains('outfielderBlockedPass'))
                                  |(df_away['satisfiedEventsTypes'].apply(str).str.contains('clearanceTotal'))]


    home_def_actions = len(df_home_def_actions[df_home_def_actions['x'] > 50])
    away_def_actions = len(df_away_def_actions[df_away_def_actions['x'] > 50])
    
    #calculate PPDA
    home_ppda = round(away_passes_deep / home_def_actions, 1)
    away_ppda = round(home_passes_deep / away_def_actions, 1)
    total_ppda = home_ppda + away_ppda
    
    # Passes
    num_home_passes = len(df_home_passes)
    num_away_passes = len(df_away_passes)
    
    # Shots
    df_home_shots = df_home[df_home['isShot'] == True]
    df_away_shots = df_away[df_away['isShot'] == True]
    
    # Goals
    df_home_goals = df_home[df_home["isGoal"] == True]
    df_away_goals = df_away[df_away['isGoal'] == True]
    
    num_home_shots = len(df_home_shots)
    num_away_shots = len(df_away_shots)
    
    num_home_goals = len(df_home_goals)
    num_away_goals = len(df_away_goals)
    
    num_home_shots_target = len(df_home[df_home['satisfiedEventsTypes'].apply(str).str.contains('shotOnTarget', na=False, regex=True)])
    num_away_shots_target = len(df_away[df_away['satisfiedEventsTypes'].apply(str).str.contains('shotOnTarget', na=False, regex=True)])
    
    # Get totals
    total_goals = num_home_goals + num_away_goals
    total_shots = num_home_shots + num_away_shots
    total_target = num_home_shots_target + num_away_shots_target
    total_passes = num_home_passes + num_away_passes
    
    # Calculate percentages
    per_home_goals = num_home_goals / total_goals
    per_away_goals = num_away_goals / total_goals
    per_home_shots = num_home_shots / total_shots
    per_away_shots = num_away_shots / total_shots
    per_home_target = num_home_shots_target / total_target
    per_away_target = num_away_shots_target / total_target
    per_home_passes = num_home_passes / total_passes
    per_away_passes = num_away_passes / total_passes
    per_home_xg = home_xg / total_xg
    per_away_xg = away_xg / total_xg
    per_home_ppda = home_ppda / total_ppda
    per_away_ppda = away_ppda / total_ppda
    
    home_num_stats = [home_ppda, num_home_passes, num_home_shots_target, num_home_shots, home_xg, num_home_goals]
    away_num_stats = [away_ppda, num_away_passes, num_away_shots_target, num_away_shots, away_xg, num_away_goals]
    
    home_percentages = [per_home_ppda, per_home_passes, per_home_target, per_home_shots, per_home_xg, per_home_goals]
    away_percentages = [per_away_ppda, per_away_passes, per_away_target, per_away_shots, per_away_xg, per_away_goals]
    
    home_stats = zip(home_num_stats, home_percentages)
    away_stats = zip(away_num_stats, away_percentages)
    
    return home_stats, away_stats

def data_for_percentiles(team=None,season=None,gw=None):

    if season is None:
        season = "2122"
    if team is None:
        team = "Barcelona"
    if gw is None:
        gw = "1"
    
    if season == "2122":
        df = pd.read_csv(f"/work/assets/whoscored/{team}/match/{season}/eventsData/new/{season}#{gw}.csv")
    else:    
        df = pd.read_csv(f"/work/assets/whoscored/{team}/match/{season}/{season}#{gw}.csv")
        
    df["comp"] = gw

    def_third = 33.3
    att_third = 66.6
    
    df_def_actions = df[(df['satisfiedEventsTypes'].apply(str).str.contains('tackleLost')) | (df['satisfiedEventsTypes'].apply(str).str.contains('tackleWon'))
                       | (df['satisfiedEventsTypes'].apply(str).str.contains('interceptionWon')) | (df['satisfiedEventsTypes'].apply(str).str.contains('interceptionAll'))
                       | (df['satisfiedEventsTypes'].apply(str).str.contains('foulCommitted')) | (df['satisfiedEventsTypes'].apply(str).str.contains('outfielderBlock'))
                       | (df['satisfiedEventsTypes'].apply(str).str.contains('shotBlocked')) | (df['satisfiedEventsTypes'].apply(str).str.contains('passCrossBlockedDefensive'))
                       | (df['satisfiedEventsTypes'].apply(str).str.contains('outfielderBlockedPass')) | (df['satisfiedEventsTypes'].apply(str).str.contains('interceptionIntheBox'))]

    # Regular passes
    df_passes = df[df['satisfiedEventsTypes'].apply(str).str.contains('passAccurate', na=False)]
    
    # Wing play
    wing_passes = df_passes[(df_passes['x'] > 75)
                                | (df_passes['x'] < 25)].groupby('comp').size()
    
    # Deep circulation
    deep_passes = df_passes[df_passes['x'] < 25].groupby('comp').size()
    
    # Long balls
    df_passes['dist'] = np.sqrt((df_passes.x-df_passes.endX)**2 + (df_passes.y-df_passes.endY)**2)
    long_balls = df_passes[df_passes['dist'] > 40].groupby('comp').size()
    
    # Crosses
    crosses = df[(df['satisfiedEventsTypes'].apply(str).str.contains('passCrossAccurate'))
                 | (df['satisfiedEventsTypes'].apply(str).str.contains('passCrossInaccurate'))].groupby('comp').size()
    
    # Danger Zones entries
    danger_zone = df_passes[(df_passes['endX'] > 90)
                                       & (df_passes['x'] < 90)
                                       & (df_passes['endY'].between(25, 75))].groupby('comp').size()
    
    # High press
    high_press = df_def_actions[df_def_actions['x'] > att_third].groupby('comp').size()
    
    # Low block
    low_block = df_def_actions[df_def_actions['x'] < def_third].groupby('comp').size()
    
    # Counters
    short_passes = df_passes[df_passes['dist'] < 15].groupby('comp').size()
    
    # Concatenate dataframes
#     df_all = pd.concat([wing_passes, deep_passes, long_balls, short_passes,
#                         danger_zone, low_block, high_press], axis=1).fillna(0).div(2)
#     df_all.columns = ['wing_passes', 'deep_passes', 'long_balls', 'short_passes',
#                         'danger_zone', 'low_block', 'high_press']

    df_all = pd.concat([wing_passes, deep_passes, long_balls, short_passes,
                        crosses, danger_zone, low_block, high_press], axis=1).fillna(0).div(2)
    df_all.columns = ['wing_passes', 'deep_passes', 'long_balls', 'short_passes',
                        'crosses', 'danger_zone', 'low_block', 'high_press']
    
    return df_all

def get_radar_data(df_home: pd.DataFrame, df_away: pd.DataFrame):
    
    # Regular passes
    df_home_passes = df_home[df_home['satisfiedEventsTypes'].apply(str).str.contains('passAccurate', na=False)]
    df_away_passes = df_away[df_away['satisfiedEventsTypes'].apply(str).str.contains('passAccurate', na=False)]   
    
    df_home_passes['dist'] = np.sqrt((df_home_passes.x-df_home_passes.endX)**2 + (df_home_passes.y-df_home_passes.endY)**2)
    df_away_passes['dist'] = np.sqrt((df_away_passes.x-df_away_passes.endX)**2 + (df_away_passes.y-df_away_passes.endY)**2)
    
    def_third = 33.3
    att_third = 66.6
    
    df_home_def_actions = df_home[(df_home['satisfiedEventsTypes'].apply(str).str.contains('tackleLost')) | (df_home['satisfiedEventsTypes'].apply(str).str.contains('tackleWon'))
                                  |(df_home['satisfiedEventsTypes'].apply(str).str.contains('interceptionAll'))| (df_home['satisfiedEventsTypes'].apply(str).str.contains('outfielderBlock'))
                                  |(df_home['satisfiedEventsTypes'].apply(str).str.contains('interceptionWon')) | (df_home['satisfiedEventsTypes'].apply(str).str.contains('outfielderBlockedPass'))
                                  |(df_home['satisfiedEventsTypes'].apply(str).str.contains('clearanceTotal'))]
    df_away_def_actions = df_away[(df_away['satisfiedEventsTypes'].apply(str).str.contains('tackleLost')) | (df_away['eventId'].apply(str).str.contains('tackleWon'))
                                  |(df_away['satisfiedEventsTypes'].apply(str).str.contains('interceptionAll'))| (df_away['satisfiedEventsTypes'].apply(str).str.contains('outfielderBlock'))
                                  |(df_away['satisfiedEventsTypes'].apply(str).str.contains('interceptionWon')) | (df_away['satisfiedEventsTypes'].apply(str).str.contains('outfielderBlockedPass'))
                                  |(df_away['satisfiedEventsTypes'].apply(str).str.contains('clearanceTotal'))]
    
    # Wing play
    home_wing_passes = len(df_home_passes[(df_home_passes['x'] > 75)
                                          | (df_home_passes['x'] < 25)])
    away_wing_passes = len(df_away_passes[(df_away_passes['x'] > 75)
                                          | (df_away_passes['x'] < 25)])
    
    # Deep circulation
    home_deep_passes = len(df_home_passes[df_home_passes['x'] < 25])
    away_deep_passes = len(df_away_passes[df_away_passes['x'] < 25])

    # Long balls
    home_long_balls = len(df_home_passes[df_home_passes['dist'] > 40])
    away_long_balls = len(df_away_passes[df_away_passes['dist'] > 40])
    
     # Crosses 
    home_crosses = len(df_home[(df_home['satisfiedEventsTypes'].apply(str).str.contains('passCrossAccurate'))
                 | (df_home['satisfiedEventsTypes'].apply(str).str.contains('passCrossInaccurate'))])
    away_crosses = len(df_away[(df_away['satisfiedEventsTypes'].apply(str).str.contains('passCrossAccurate'))
                 | (df_away['satisfiedEventsTypes'].apply(str).str.contains('passCrossInaccurate'))])
      
    # Danger Zone entries
    home_danger_zone = len(df_home_passes[(df_home_passes['endX'] > 90)
                                       & (df_home_passes['x'] < 90)
                                       & (df_home_passes['endY'].between(25, 75))])
    away_danger_zone = len(df_away_passes[(df_away_passes['endX'] > 90)
                                       & (df_away_passes['x'] < 90)
                                       & (df_away_passes['endY'].between(25, 75))])

    # High press
    home_high_press = len(df_home_def_actions[df_home_def_actions['x'] > att_third])
    away_high_press = len(df_away_def_actions[df_away_def_actions['x'] > att_third])
    
    # Low block
    home_low_block = len(df_home_def_actions[df_home_def_actions['x'] < def_third])
    away_low_block = len(df_away_def_actions[df_away_def_actions['x'] < def_third])
    
    # Counters
    home_short_passes = len(df_home_passes[df_home_passes['dist'] < 15])
    away_short_passes = len(df_away_passes[df_away_passes['dist'] < 15])

   # Concatenate dataframes
#     home_all = [home_wing_passes, home_deep_passes, home_long_balls, home_short_passes,
#                 home_danger_zone, home_low_block, home_high_press]
#     away_all = [away_wing_passes, away_deep_passes, away_long_balls, away_short_passes,
#                 away_danger_zone, away_low_block, away_high_press]

    home_all = [home_wing_passes, home_deep_passes, home_long_balls, home_short_passes,
                home_crosses, home_danger_zone, home_low_block, home_high_press]
    away_all = [away_wing_passes, away_deep_passes, away_long_balls, away_short_passes,
                   away_crosses, away_danger_zone, away_low_block, away_high_press]
    
    # Get percentiles
    df_all = data_for_percentiles()
    
    df_all.loc['home'] = home_all
    df_all.loc['away'] = away_all
    
    df_percentile = df_all.rank(pct=True, axis='index')
    
    home_pvals = [df_percentile[df_percentile.index == 'home'][qty].item()*100 for qty in df_all.columns]
    away_pvals = [df_percentile[df_percentile.index == 'away'][qty].item()*100 for qty in df_all.columns]
    
    return home_pvals, away_pvals


def get_possession_data(df_home: pd.DataFrame, df_away: pd.DataFrame):
    # Get passes
    df_home_passes = df_home[(df_home['satisfiedEventsTypes'].apply(str).str.contains('passAccurate', na=False)) | (df_home['satisfiedEventsTypes'].str.contains('passInaccurate', na=False))]
    df_away_passes = df_away[(df_away['satisfiedEventsTypes'].apply(str).str.contains('passAccurate', na=False)) | (df_away['satisfiedEventsTypes'].str.contains('passInaccurate', na=False))]
                             
    
    # Minutes
    df_minutes = pd.DataFrame({'minute': range(df_home['minute'].min(), df_home['minute'].max()+1, 1)})

    # Create counter of passes
    df_home_passes['counter'] = np.arange(1, len(df_home_passes)+1)
    df_away_passes['counter'] = np.arange(1, len(df_away_passes)+1)

    df_home_possession = df_minutes.merge(df_home_passes, how='left', on='minute')[['minute', 'counter']].ffill().fillna(0)
    df_away_possession = df_minutes.merge(df_away_passes, how='left', on='minute')[['minute', 'counter']].ffill().fillna(0)
    
    # Group by minutes and sum counter
    df_home_possession_final = pd.DataFrame(df_home_possession.groupby('minute').count()).reset_index()
    df_away_possession_final = pd.DataFrame(df_away_possession.groupby('minute').count()).reset_index()
    
    # Create rolling average
    df_home_possession_final['rolling'] = df_home_possession_final['counter'].rolling(window=15, min_periods=1).mean()
    df_away_possession_final['rolling'] = df_away_possession_final['counter'].rolling(window=15, min_periods=1).mean()
    
    # Calculate percentages of possession
    df_home_possession_final['rolling_percentage'] = ((df_home_possession_final['rolling'] / (df_home_possession_final['rolling']
                                                                                            + df_away_possession_final['rolling'])) * 100)
    df_away_possession_final['rolling_percentage'] = ((df_away_possession_final['rolling'] / (df_away_possession_final['rolling']
                                                                                            + df_home_possession_final['rolling'])) * 100)

    df_home_rolling = df_home_possession_final.groupby('minute')['rolling_percentage'].sum()
    df_away_rolling = df_away_possession_final.groupby('minute')['rolling_percentage'].sum()
    
    return df_home_possession_final, df_away_possession_final

def calculate_possession(df_home_possession, df_away_possession):
    home_possession = round((df_home_possession['counter'].sum() / (df_away_possession['counter'].sum()
                                                                  + df_home_possession['counter'].sum())) * 100, 1)
    away_possession = round((df_away_possession['counter'].sum() / (df_away_possession['counter'].sum()
                                                                  + df_home_possession['counter'].sum())) * 100, 1)
    return home_possession, away_possession

def get_added_time(df):
    
    # Added time (+45)
    df_45 = df[df['period']=="FirstHalf"]
    added_time45 = df_45['minute'].max() - 45
    
    # Added time (+90)
    added_time90 = df['minute'].max() - 90

    return [added_time45, added_time90]

def get_defensive_actions(df_home, df_away):
    def_third = 33.3
    att_third = 66.6

    df_home_def_actions = df_home[(df_home['satisfiedEventsTypes'].apply(str).str.contains('tackleLost')) | (df_home['satisfiedEventsTypes'].apply(str).str.contains('tackleWon'))
                                  |(df_home['satisfiedEventsTypes'].apply(str).str.contains('interceptionAll'))| (df_home['satisfiedEventsTypes'].apply(str).str.contains('outfielderBlock'))
                                  |(df_home['satisfiedEventsTypes'].apply(str).str.contains('interceptionWon')) | (df_home['satisfiedEventsTypes'].apply(str).str.contains('outfielderBlockedPass'))
                                  |(df_home['satisfiedEventsTypes'].apply(str).str.contains('clearanceTotal'))]
    df_away_def_actions = df_away[(df_away['satisfiedEventsTypes'].apply(str).str.contains('tackleLost')) | (df_away['eventId'].apply(str).str.contains('tackleWon'))
                                  |(df_away['satisfiedEventsTypes'].apply(str).str.contains('interceptionAll'))| (df_away['satisfiedEventsTypes'].apply(str).str.contains('outfielderBlock'))
                                  |(df_away['satisfiedEventsTypes'].apply(str).str.contains('interceptionWon')) | (df_away['satisfiedEventsTypes'].apply(str).str.contains('outfielderBlockedPass'))
                                  |(df_away['satisfiedEventsTypes'].apply(str).str.contains('clearanceTotal'))]

#     df_home_def_actions = df_home[(df_home['satisfiedEventsTypes'].apply(str).str.contains('141')) | (df_home['satisfiedEventsTypes'].apply(str).str.contains('142'))
#                                   |(df_home['satisfiedEventsTypes'].apply(str).str.contains('100'))| (df_home['satisfiedEventsTypes'].apply(str).str.contains('57'))
#                                   |(df_home['satisfiedEventsTypes'].apply(str).str.contains('55')) | (df_home['satisfiedEventsTypes'].apply(str).str.contains('59'))
#                                   |(df_home['satisfiedEventsTypes'].apply(str).str.contains('94'))]
#     df_away_def_actions = df_away[(df_away['satisfiedEventsTypes'].apply(str).str.contains('141')) | (df_away['eventId'].apply(str).str.contains('142'))
#                                   |(df_away['satisfiedEventsTypes'].apply(str).str.contains('100'))| (df_away['satisfiedEventsTypes'].apply(str).str.contains('57'))
#                                   |(df_away['satisfiedEventsTypes'].apply(str).str.contains('55')) | (df_away['satisfiedEventsTypes'].apply(str).str.contains('59'))
#                                   |(df_away['satisfiedEventsTypes'].apply(str).str.contains('94'))]

    
    #calculate percentages of defensive actions in different zones
    num_home_def_actions = len(df_home_def_actions)
    home_def_third_actions_percentage = (len(df_home_def_actions[df_home_def_actions['x'] < def_third]) / num_home_def_actions) * 100
    home_mid_third_actions_percentage = (len(df_home_def_actions[df_home_def_actions['x'].between(def_third, att_third)]) / num_home_def_actions) * 100
    home_att_third_actions_percentage = (len(df_home_def_actions[df_home_def_actions['x'] > att_third]) / num_home_def_actions) * 100
    #concat to list
    def_home_actions_list = list([home_def_third_actions_percentage, home_mid_third_actions_percentage, home_att_third_actions_percentage])
    home_labels = list([f'{int(home_def_third_actions_percentage)}%', f'{int(home_mid_third_actions_percentage)}%', f'{int(home_att_third_actions_percentage)}%'])

    #calculate percentages of defensive actions in different zones
    num_away_def_actions = len(df_away_def_actions)
    away_def_third_actions_percentage = (len(df_away_def_actions[df_away_def_actions['x'] < def_third]) / num_away_def_actions) * 100
    away_mid_third_actions_percentage = (len(df_away_def_actions[df_away_def_actions['x'].between(def_third, att_third)]) / num_away_def_actions) * 100
    away_att_third_actions_percentage = (len(df_away_def_actions[df_away_def_actions['x'] > att_third]) / num_away_def_actions) * 100
    #concat to list
    def_away_actions_list = list([away_def_third_actions_percentage, away_mid_third_actions_percentage, away_att_third_actions_percentage])
    away_labels = list([f'{int(away_def_third_actions_percentage)}%', f'{int(away_mid_third_actions_percentage)}%', f'{int(away_att_third_actions_percentage)}%'])

    return df_home_def_actions, home_labels, df_away_def_actions, away_labels


def get_key_passes(df_home, df_away):
    
    
    df_home_passes = df_home[df_home['satisfiedEventsTypes'].apply(str).str.contains('passKey', na=False)]
    df_away_passes = df_away[df_away['satisfiedEventsTypes'].apply(str).str.contains('passKey', na=False)]
                    
#     df_home_passes = df_home[(df_home['type.displayName']=="Pass")|(df_home['outcomeType']==1)]
#     df_away_passes = df_away[(df_away['type.displayName']=="Pass")|(df_away['outcomeType']==1)]
                             
                             
#     home_key_passes = df_home_passes[(df_home_passes.x < 83) & (df_home_passes.endX > 83) & (df_home_passes.endY.between(21, 79))]
#     away_key_passes = df_away_passes[(df_away_passes.x < 83) & (df_away_passes.endX > 83) & (df_away_passes.endY.between(21, 79))]

    home_key_passes = df_home_passes
    away_key_passes = df_away_passes
    return home_key_passes, away_key_passes


def get_heatmap_data(df_home, df_away):
    
    # Get passes
    df_home_passes = df_home[(df_home['satisfiedEventsTypes'].apply(str).str.contains('passAccurate', na=False)) | (df_home['satisfiedEventsTypes'].apply(str).str.contains('passInaccurate', na=False))]
    df_away_passes = df_away[(df_away['satisfiedEventsTypes'].apply(str).str.contains('passAccurate', na=False)) | (df_away['satisfiedEventsTypes'].apply(str).str.contains('passInaccurate', na=False))]

    df_home_shots = df_home[df_home['isShot'] == True]
    df_away_shots = df_away[df_away['isShot'] == True]
    
    df_home_actions = pd.concat([df_home_passes, df_home_shots])
    df_away_actions = pd.concat([df_away_passes, df_away_shots])

    return df_home_actions, df_away_actions

def get_juego(df):
    
    df['prevShot'] = df['isShot'].shift(-1)
    df = df[df['prevShot'] == True]
    
    return df

def get_bar_plot_CLdata(df_home: pd.DataFrame, df_away: pd.DataFrame, gw: str, team=None, season=None) -> list:
    
    df_home_passes = df_home[(df_home['satisfiedEventsTypes'].apply(str).str.contains('passAccurate', na=False)) | (df_home['eventId'].apply(str).str.contains('passInaccurate', na=False))]
    
    df_away_passes = df_away[(df_away['satisfiedEventsTypes'].apply(str).str.contains('passAccurate', na=False)) | (df_away['eventId'].apply(str).str.contains('passInaccurate', na=False))]
    
    home_passes_deep = len(df_home_passes[df_home_passes['x'] < 50])
    away_passes_deep = len(df_away_passes[df_away_passes['x'] < 50])
    

#     df_home_def_actions = df_home[(df_home['satisfiedEventsTypes'].apply(str).str.contains('141')) | (df_home['satisfiedEventsTypes'].apply(str).str.contains('142'))
#                                   |(df_home['satisfiedEventsTypes'].apply(str).str.contains('100'))| (df_home['satisfiedEventsTypes'].apply(str).str.contains('57'))
#                                   |(df_home['satisfiedEventsTypes'].apply(str).str.contains('55')) | (df_home['satisfiedEventsTypes'].apply(str).str.contains('59'))
#                                   |(df_home['satisfiedEventsTypes'].apply(str).str.contains('94'))]
    
#     df_away_def_actions = df_away[(df_away['satisfiedEventsTypes'].apply(str).str.contains('141')) | (df_away['eventId'].apply(str).str.contains('142'))
#                                   |(df_away['satisfiedEventsTypes'].apply(str).str.contains('100'))| (df_away['satisfiedEventsTypes'].apply(str).str.contains('57'))
#                                   |(df_away['satisfiedEventsTypes'].apply(str).str.contains('55')) | (df_away['satisfiedEventsTypes'].apply(str).str.contains('59'))
#                                   |(df_away['satisfiedEventsTypes'].apply(str).str.contains('94'))]

    df_home_def_actions = df_home[(df_home['satisfiedEventsTypes'].apply(str).str.contains('tackleLost')) | (df_home['satisfiedEventsTypes'].apply(str).str.contains('tackleWon'))
                                  |(df_home['satisfiedEventsTypes'].apply(str).str.contains('interceptionAll'))| (df_home['satisfiedEventsTypes'].apply(str).str.contains('outfielderBlock'))
                                  |(df_home['satisfiedEventsTypes'].apply(str).str.contains('interceptionWon')) | (df_home['satisfiedEventsTypes'].apply(str).str.contains('outfielderBlockedPass'))
                                  |(df_home['satisfiedEventsTypes'].apply(str).str.contains('clearanceTotal'))]
    
    df_away_def_actions = df_away[(df_away['satisfiedEventsTypes'].apply(str).str.contains('tackleLost')) | (df_away['eventId'].apply(str).str.contains('tackleWon'))
                                  |(df_away['satisfiedEventsTypes'].apply(str).str.contains('interceptionAll'))| (df_away['satisfiedEventsTypes'].apply(str).str.contains('outfielderBlock'))
                                  |(df_away['satisfiedEventsTypes'].apply(str).str.contains('interceptionWon')) | (df_away['satisfiedEventsTypes'].apply(str).str.contains('outfielderBlockedPass'))
                                  |(df_away['satisfiedEventsTypes'].apply(str).str.contains('clearanceTotal'))]


    home_def_actions = len(df_home_def_actions[df_home_def_actions['x'] > 50])
    away_def_actions = len(df_away_def_actions[df_away_def_actions['x'] > 50])
    
    #calculate PPDA
    home_ppda = round(away_passes_deep / home_def_actions, 1)
    away_ppda = round(home_passes_deep / away_def_actions, 1)
    total_ppda = home_ppda + away_ppda
    
    # Passes
    num_home_passes = len(df_home_passes)
    num_away_passes = len(df_away_passes)
    
    # Shots
    df_home_shots = df_home[df_home['isShot'] == True]
    df_away_shots = df_away[df_away['isShot'] == True]
    
    # Goals
    df_home_goals = df_home[df_home["isGoal"] == True]
    df_away_goals = df_away[df_away['isGoal'] == True]
    
    num_home_shots = len(df_home_shots)
    num_away_shots = len(df_away_shots)
    
    num_home_goals = len(df_home_goals)
    num_away_goals = len(df_away_goals)
    
    num_home_shots_target = len(df_home[df_home['satisfiedEventsTypes'].apply(str).str.contains('shotOnTarget', na=False, regex=True)])
    num_away_shots_target = len(df_away[df_away['satisfiedEventsTypes'].apply(str).str.contains('shotOnTarget', na=False, regex=True)])
    
    # Get totals
    total_goals = num_home_goals + num_away_goals
    total_shots = num_home_shots + num_away_shots
    total_target = num_home_shots_target + num_away_shots_target
    total_passes = num_home_passes + num_away_passes
    
    # Calculate percentages
    try:
        per_home_goals = num_home_goals / total_goals
        per_away_goals = num_away_goals / total_goals
    except ZeroDivisionError:
        print("total is zero")
        per_home_goals = 0
        per_away_goals = 0
    per_home_shots = num_home_shots / total_shots
    per_away_shots = num_away_shots / total_shots
    per_home_target = num_home_shots_target / total_target
    per_away_target = num_away_shots_target / total_target
    per_home_passes = num_home_passes / total_passes
    per_away_passes = num_away_passes / total_passes
#     per_home_xg = home_xg / total_xg
#     per_away_xg = away_xg / total_xg
    per_home_ppda = home_ppda / total_ppda
    per_away_ppda = away_ppda / total_ppda
    
    home_num_stats = [home_ppda, num_home_passes, num_home_shots_target, num_home_shots, num_home_goals]
    away_num_stats = [away_ppda, num_away_passes, num_away_shots_target, num_away_shots, num_away_goals]
    
    home_percentages = [per_home_ppda, per_home_passes, per_home_target, per_home_shots, per_home_goals]
    away_percentages = [per_away_ppda, per_away_passes, per_away_target, per_away_shots, per_away_goals]
    
    home_stats = zip(home_num_stats, home_percentages)
    away_stats = zip(away_num_stats, away_percentages)
    
    return home_stats, away_stats


'''
df_home, df_away = load_data('2021', 'gw23')
df = get_pass_zones(df_home)
print(df.shape)
'''
#%%
# def main():
#     pass

# if __name__ == '__main__':
#     main()
