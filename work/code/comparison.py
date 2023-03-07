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

# playtime = [1862, 498, 256]
# for time in playtime:
#     time = time 


goal = [0, 1, 0]
assist = [2, 2, 0]
pass_comp = [91.00, 86.4, 81.4]
xa = [1.6, 1.6, 0.7]
xgplus90 = [6.9, 11.8, 0.6]
keypass = [10, 17, 6]
finalthird = [31, 170, 7]
through = [2, 3, 1]
press = [70, 318, 27]
chancecreate90 = [3.53, 2.44, 3.16]
tackle = [10, 20, 7]
switch = [10,318, 2]
sucdribble = [87.5, 73.1, 33.3]
attemptdribble = [16, 67, 3]
# ELEMENTS = [
#     goal,
#     assist,
#     pass_comp,
#     xa,
#     xgplus90,
#     keypass,
#     finalthird,
#     through,
#     press,
#     chancecreate90,
#     tackle,
#     switch,
#     sucdribble,
#     attemptdribble
# ]


def compare_player(url='assets/barca_ptype.csv', PLUS_NUM, keys=*keys):

    df = pd.read_csv(url)

    col = df.columns
    ELEMENTS = []

    for c in col:
        d = {c: df[c].tolist()}
        ELEMENTS.append(d)

    keys = keys

    keys = [element.keys() for element in elements]
    
    player = [element.get(key[0]) for element in elements]
    

    COUNT = len(element)
    MEAN = np.mean(element)
    STD = np.std(element)
    score_list = []
    for x in range(COUNT):
        score = (element[x] - MEAN) / STD + PLUS_NUM
        list.append(score.round(2))

        


    



    lader_list = [
                    [42.93, 64.14, 42.93],
                    [57.07, 57.07, 35.86],
                    [62.07, 50.34, 37.59],
                    [57.07, 57.07, 35.86],
                    #   [51.02, 61.71, 37.28],
                    [47.8, 63.2, 39.0],
                    [44.67, 64.01, 41.32],
                    [50.0, 62.25, 37.75],
                    [44.67, 64.01, 41.32],
                    [45.8, 63.79, 40.4],
                    [59.98, 53.69, 36.33]
                ]


    lader = pd.DataFrame(lader_list)



    title = Eleme

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=lader[0],
    theta=title,
    fill='toself',
    name='Riqui Puig',
    line_color='gold'
))
fig.add_trace(go.Scatterpolar(
    r=lader[1],
    theta=title,
    fill='toself',
    name='Andres Iniesta',
    line_color='deeppink'
))
fig.add_trace(go.Scatterpolar(
    r=lader[2],
    theta=title,
    fill='toself',
    name='Pedri',
    line_color='aqua'
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=False,
            range=[0, 100]
        )),
    showlegend=True,
)


fig['layout'].update(
    # height=2000,
    title='Riqui ( 19/20 ) vs  Iniesta ( 17/18 ) vs  Pedri ( 20/21 )',
    font={"family": "Monospace", "size": 14},
    template="plotly_dark",
    polar=dict(
        # bgcolor=''
    ),
)

fig.show()
