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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
SEASONS = [
    '08~09',
    '09~10',
    '10~11',
    '11~12',
    '12~13',
    '13~14',
    '14~15',
    '15~16',
    '16~17',
    '17~18',
    '18~19',
    '19~20']


def get_cleansheet_percentage():

    df = pd.read_csv('assets/liga1920.csv')

    liga1920 = df[df['HomeTeam'] == 'Barcelona']
    home1920 = liga1920[liga1920['FTAG'] == 0]

    liga1920 = df[df['AwayTeam'] == 'Barcelona']
    away1920 = liga1920[liga1920['FTHG'] == 0]


    df = pd.read_csv('assets/liga1819.csv')

    liga1819 = df[df['HomeTeam'] == 'Barcelona']
    home1819 = liga1819[liga1819['FTAG'] == 0]

    liga1819 = df[df['AwayTeam'] == 'Barcelona']
    away1819 = liga1819[liga1819['FTHG'] == 0]


    df = pd.read_csv('assets/liga1718.csv')

    liga1718 = df[df['HomeTeam'] == 'Barcelona']
    home1718 = liga1718[liga1718['FTAG'] == 0]

    liga1718 = df[df['AwayTeam'] == 'Barcelona']
    away1718 = liga1718[liga1718['FTHG'] == 0]


    df = pd.read_csv('assets/liga1617.csv')

    liga1617 = df[df['HomeTeam'] == 'Barcelona']
    home1617 = liga1617[liga1617['FTAG'] == 0]

    liga1617 = df[df['AwayTeam'] == 'Barcelona']
    away1617 = liga1617[liga1617['FTHG'] == 0]


    df = pd.read_csv('assets/liga1516.csv')

    liga1516 = df[df['HomeTeam'] == 'Barcelona']
    home1516 = liga1516[liga1516['FTAG'] == 0]

    liga1516 = df[df['AwayTeam'] == 'Barcelona']
    away1516 = liga1516[liga1516['FTHG'] == 0]


    df = pd.read_csv('assets/liga1415.csv')

    liga1415 = df[df['HomeTeam'] == 'Barcelona']
    home1415 = liga1415[liga1415['FTAG'] == 0]

    liga1415 = df[df['AwayTeam'] == 'Barcelona']
    away1415 = liga1415[liga1415['FTHG'] == 0]


    df = pd.read_csv('assets/liga1314.csv')

    liga1314 = df[df['HomeTeam'] == 'Barcelona']
    home1314 = liga1314[liga1314['FTAG'] == 0]

    liga1314 = df[df['AwayTeam'] == 'Barcelona']
    away1314 = liga1314[liga1314['FTHG'] == 0]


    df = pd.read_csv('assets/liga1213.csv')

    liga1213 = df[df['HomeTeam'] == 'Barcelona']
    home1213 = liga1213[liga1213['FTAG'] == 0]

    liga1213 = df[df['AwayTeam'] == 'Barcelona']
    away1213 = liga1213[liga1213['FTHG'] == 0]


    df = pd.read_csv('assets/liga1112.csv')

    liga1112 = df[df['HomeTeam'] == 'Barcelona']
    home1112 = liga1112[liga1112['FTAG'] == 0]

    liga1112 = df[df['AwayTeam'] == 'Barcelona']
    away1112 = liga1112[liga1112['FTHG'] == 0]


    df = pd.read_csv('assets/liga1011.csv')

    liga1011 = df[df['HomeTeam'] == 'Barcelona']
    home1011 = liga1011[liga1011['FTAG'] == 0]

    liga1011 = df[df['AwayTeam'] == 'Barcelona']
    away1011 = liga1011[liga1011['FTHG'] == 0]


    df = pd.read_csv('assets/liga0910.csv')

    liga0910 = df[df['HomeTeam'] == 'Barcelona']
    home0910 = liga0910[liga0910['FTAG'] == 0]

    liga0910 = df[df['AwayTeam'] == 'Barcelona']
    away0910 = liga0910[liga0910['FTHG'] == 0]


    df = pd.read_csv('assets/liga0809.csv')

    liga0809 = df[df['HomeTeam'] == 'Barcelona']
    home0809 = liga0809[liga0809['FTAG'] == 0]

    liga0809 = df[df['AwayTeam'] == 'Barcelona']
    away0809 = liga0809[liga0809['FTHG'] == 0]


    season19 = pd.concat([home1920, away1920])
    season18 = pd.concat([home1819, away1819])
    season17 = pd.concat([home1718, away1718])
    season16 = pd.concat([home1617, away1617])
    season15 = pd.concat([home1516, away1516])
    season14 = pd.concat([home1415, away1415])
    season13 = pd.concat([home1314, away1314])
    season12 = pd.concat([home1213, away1213])
    season11 = pd.concat([home1112, away1112])
    season10 = pd.concat([home1011, away1011])
    season09 = pd.concat([home0910, away0910])
    season08 = pd.concat([home0809, away0809])

    cleansheet_list = [
        len(season08),
        len(season09),
        len(season10),
        len(season11),
        len(season12),
        len(season13),
        len(season14),
        len(season15),
        len(season16),
        len(season17),
        len(season18),
        len(season19),
    ]
    # print(cleansheet_list)

    per_cleansheet_list = []
    for cleansheet in cleansheet_list:
        per_cleansheet = round((cleansheet / 38 * 100), 2)
        per_cleansheet_list.append(per_cleansheet)
    

    pep = per_cleansheet_list[:4]
    tito = per_cleansheet_list[4]
    tata = per_cleansheet_list[5]
    enrique = per_cleansheet_list[6:9]
    valverde = per_cleansheet_list[9:11]
    quique = per_cleansheet_list[11]

    pep_mean = statistics.mean(pep)
    enrique_mean = statistics.mean(enrique)
    valverde_mean = statistics.mean(valverde)

    VALUES = per_cleansheet_list

    return VALUES
    
# print(len(SEASONS), len(VALUES))



def set_color(x):
    if x == SEASONS[0]:
        return 'gold'
    elif x == SEASONS[1]:
        return 'gold'
    elif x == SEASONS[2]:
        return 'gold'
    elif x == SEASONS[3]:
        return 'gold'
    elif x == SEASONS[4]:
        return 'cyan'
    elif x == SEASONS[5]:
        return 'red'
    elif x == SEASONS[6]:
        return 'darkviolet'
    elif x == SEASONS[7]:
        return 'darkviolet'
    elif x == SEASONS[8]:
        return 'darkviolet'
    elif x == SEASONS[9]:
        return 'blue'
    elif x == SEASONS[10]:
        return 'blue'
    else:
        return 'green'










app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.H2(children=''),
    dcc.Graph(
        id='bucciara_graph',
        figure={
            'data': [
                go.Bar(
                    x=SEASONS,
                    y=get_cleansheet_percentage(),
                    text=get_cleansheet_percentage(),
                    textposition='auto',
                    marker_color=list(map(set_color, SEASONS)),
                ),
                go.Scatter(
                    x=SEASONS,
                    y=get_cleansheet_percentage(),
                    mode='lines+markers',
                    text=get_cleansheet_percentage(),
                    # textposition='auto',
                    line=dict(
                        color=('rgb(255,244,255)'),
                        width=1,
                    )
                ),
            ], 
            'layout': go.Layout(
                title="Barcelona's Percentage of clean-sheets for the last several years                                                                                                          @Bucciarati",
                # height=500,
                # width=1000,
                # margin={'autoexpand': True},
                font={"family": "Monospace", "size": 14},
                template='plotly_dark',
                yaxis=dict(
                    range=(0, 100)
                )
            )
        }
    )
],
)


if __name__ == '__main__':

    app.run_server(debug=True)
