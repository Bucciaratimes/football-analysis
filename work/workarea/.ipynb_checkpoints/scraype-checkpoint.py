import csv
import getopt
import json
import re
import sys
import time
import urllib

import pandas as pd
import requests
from bs4 import BeautifulSoup, Comment
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from tqdm import trange


class FbrefScrayper(object):

    def __init__(self, base_url='https://fbref.com/en/'):
        self.base_url = base_url
        
    def build_df(self, df):

        columns = []
        for col1, col2 in df.columns.to_flat_index():
            column = f'{col2}_{col1}'
            columns.append(column)

        df.columns = columns

        if '90s_' in df.columns:
            df['90s_'] = df['90s_'].fillna(0)
        df.columns = df.columns.str.replace('Unnamed: [0-9]+_level_0', '')
        if 'Player_' in df.columns:
            try:
                df = df[df['Player_'] != 'Player']
                df = df.drop_duplicates(
                            subset=['Player_'],
                            keep=False).reset_index(drop=True)
            except:
                pass
    
        for column in df.columns:
            if column[-1] == '_':
                df.rename(
                    columns={
                        f'{column}': f'{column[:-1]}'},
                    inplace=True)
        try:
            df = df.drop(columns='Matches')
        except:
            pass

        return df
        
    def get_team_data(self, url=None, number=0):
        """
        number->0: Standard Stats
                1: Score & Fixtures
                2: GoalKeeping
                3: Advanced Goalkeeping
                4: Shooting
                5: Passing
                6: Pass Types
                7: Goal and Shot Creation
                8: Defensive Actions
                9: Possession
                10: Playing Time
                11: Miscellaneous Stats
                12: Regular Season 
        """
        if url is None:
            url = 'squads/206d90db/Barcelona-Stats'
        html = requests.get(self.base_url + url)
        soup = BeautifulSoup(html.content, 'html.parser')
        table = soup.find_all('table')
        df = pd.read_html(table[number].prettify(), flavor='bs4')[0]
        return self.build_df(df) 
    
    def get_match_data(self, url=None, number=0):
        """
        number->0: Member Home
                1: Member Away
                2: Match Stats
                3: Summary Home
                4: Passing Home
                5: Pass Types Home
                6: Defensive Actions Home
                7: Possession Home
                8: Miscellaneous Stats Home
                9: Goalkeeper Stats Home
                10: Summary Away
                11: Passing Away
                12: Pass Types Away
                13: Defensive Actions Away 
                14: Possessiong Away
                15: Miscellaneous Stats Away
                16: Goalkeeper Stats Away
                17: Shots Data
        """
        if url is None:
            url = 'https://fbref.com/en/matches/086be9c6/Valladolid-Barcelona-December-22-2020-La-Liga'

        html = requests.get(url)
        comment = re.compile('<!--|-->')
        soup = BeautifulSoup(comment.sub("", html.text), 'lxml')
        table = soup.find_all("table")
        df = pd.read_html(table[number].prettify(), flavor='bs4')[0]
        if (number == 0)or(number == 1):
            return df
        return self.build_df(df)

    def get_player_season_data(self, url='None'):
        """
        number->0: Scouting Report 
                1: Scouting Report 
                2: Similar Players
                3: Similar Players
                4: Standard Stat
                5: Shooting
                6: Passing
                7: Pass Types
                8: Goal and Shot Creation
                9: Defensive Actions
                10: Possession
                11: Playing Time
                12: Miscellaneous Stats
        """

        if url is None:
            url = self.base_url + 'players/d70ce98e/Lionel-Messi'

        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'html.parser')
        table = soup.find_all('table')
        df = pd.read_html(table[number].prettify(), flavor='bs4')[0]
        return self.build_df(df)

    def get_player_match_data(self, url=None,category='summary'):
        """
        category->summary
                  passing
                  passing_types
                  gca
                  defense
                  possession
                  misc
        """
        if url is None:
            url = self.base_url + f'players/d70ce98e/matchlogs/2020-2021/{category}/Lionel-Messi-Match-Logs'

        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'html.parser')
        table = soup.find_all('table')
        df = pd.read_html(table[0].prettify(), flavor='bs4')[0]
        return self.build_df(df)





# def getLeagueLinks(main_url):

#     options = webdriver.ChromeOptions()
#     driver = webdriver.Remote(
#         command_executor='172.31.0.3:4444/wd/hub',
#         options=options
#     )
#     driver.get(main_url)
