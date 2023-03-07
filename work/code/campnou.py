import math
import statistics

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import poisson

import chart_studio
import dash
import dash_core_components as dcc
import dash_html_components as html
import japanize_matplotlib
import plotly.graph_objs as go
import plotly.offline as pyo
from plotly import subplots

df = pd.read_csv('assets/liga1920.csv')

liga1920home = df[df['HomeTeam'] == 'Barcelona']
liga1920home = liga1920home[['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']]
liga1920home = liga1920home.rename(
    columns={
        'FTHG': 'HomeGoals',
        'FTAG': 'againstG(H)'})

liga1920away = df[df['AwayTeam'] == 'Barcelona']
liga1920away = liga1920away[['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']]
liga1920away = liga1920away.rename(
    columns={
        'FTHG': 'againstG(A)',
        'FTAG': 'AwayGoals'})
liga1920home.reset_index(drop=True, inplace=True)
liga1920away.reset_index(drop=True, inplace=True)

liga1920 = pd.concat([liga1920home, liga1920away], axis=1)
liga1920_goal = liga1920[['HomeTeam', 'AwayTeam', 'HomeGoals', 'AwayGoals']]
liga1920_goal.mean()

poisson_pred = np.column_stack(
    [[poisson.pmf(i, liga1920_goal.mean()[j]) for i in range(9)] for j in range(2)])


fig, ax = plt.subplots(figsize=(8, 4))
# plot histogram of actual goals
plt.hist(liga1920[['HomeGoals', 'AwayGoals']].values, range(9), alpha=0.7, label=[
         'home', 'away'], density=True, color=["#fc0362", "#03e3fc"])

pois1, = plt.plot([i - 0.5 for i in range(1, 10)], poisson_pred[:, 0],
                  linestyle='-', marker='o', label="Home", color='#fc0341')
pois2, = plt.plot([i - 0.5 for i in range(1, 10)], poisson_pred[:, 1],
                  linestyle='-', marker='o', label="Away", color='#0331fc')
# matplotlib.rcParams['font.family'] = 'IPAPGothic'
leg = plt.legend(loc='upper right', fontsize=12, ncol=2)
leg.set_title(
    "データ分析                 実際の数字",
    prop={
        'size': '10',
        'weight': 'normal'})

plt.xticks([i - 0.5 for i in range(1, 10)], [i for i in range(9)])
plt.xlabel("1試合あたりのゴール数", size=12)
plt.ylabel("その得点が（あったorあるだろう）試合の割合", size=12)
plt.title("Barcelona19/20's number of Goals per Match",
          size=16, fontweight='bold', fontname="fantasy")
plt.ylim([-0.004, 0.5])
plt.tight_layout()
plt.show()
