import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.offline as pyo
from plotly.subplots import make_subplots
import numpy as np
import math
import pandas as pd
import chart_studio
import chart_studio.plotly as py

pd.get_option("display.max_columns")
df = pd.read_csv('assets/league/team_age_architect2020.csv')
df.fillna(0, inplace=True)

teams = df['team'].unique()
team_name =[]
for team in teams:
    team = team.title()
    team_name.append(team)


fig = make_subplots(rows=8, cols=4, subplot_titles=team_name)


row = 1
col = 1
limit_time = 10

for team in teams:

    mp_total = 0
    df_by_t = df[df['team'] == team]
    df_by_mp = df_by_t['mplay']
    for mp in df_by_mp:
        mp_total += mp

    df_by_30 = df[(df['age'] >= 30) & (
        df['team'] == team) & (df['mplay'] > limit_time)]

    df_by_25 = df[(df['age'] >= 24) & (df['age'] < 30) &
                  (df['team'] == team) & (df['mplay'] > limit_time)]

    df_by_20 = df[(df['age'] >= 15) & (df['age'] < 24) &
                  (df['team'] == team) & (df['mplay'] > limit_time)]

    df_by_mp30 = df_by_30['mplay']
    # print(df_by_mp30)
    # print('#############################')

    df_by_mp25 = df_by_25['mplay']
    # print(df_by_mp25)
    # print('#############################')

    df_by_mp20 = df_by_20['mplay']
    # print(df_by_mp20)
    # print('#############################')

    total30 = 0
    total25 = 0
    total20 = 0

    for minute in df_by_mp30:
        total30 += minute
        per30 = math.floor(100 * (total30 / mp_total))


    for minute in df_by_mp25:
        total25 += minute
        per25 = math.floor(100 * (total25 / mp_total))

    for minute in df_by_mp20:
        total20 += minute
        per20 = math.floor(100 * (total20 / mp_total))

    x_age = ['17~23', '24~29', '30~']
    y_data = [per20, per25, per30]

    team_dict = {}
    team_dict[team] = y_data

    team = go.Bar(
        x=x_age,
        y=y_data,
        name=team.title(),
        text=y_data,
        textposition='auto'
    )

    fig.append_trace(team, row, col)
    col += 1

    if col == 5:
        col = 1
        row += 1
        if row == 9:
            break


fig['layout'].update(
    height=2000,
    title='',
    # textAlign='center',
    #   xaxis={'title': '年齢層'},
    #   yaxis={
    #         'title': '総出場時間に対する割合',
    #         'range': [0,100]
    #          },
    #     xaxis_type="linear", yaxis_type="log",
    # margin={
    #     'l': 50, 'r': 50, 't': 50, 'b': 50,
    #         'autoexpand': False
    # },
    font={"family": "Monospace", "size": 12},
    paper_bgcolor="black",
    plot_bgcolor="#333333",
    template="plotly_dark"
)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H2(
        children='「Squad Age Balance 20/21 ~11/01」',
        style={
            'textAlign': 'center',
            'font-family': 'monospace',
            'color': '#ffffff',
            'padding-top': 20
        }
    ),
    html.H5(
        children='by Bucciarati',
        style={
            'textAlign': 'center',
            'font-family': 'monospace',
            'color': '#eeeeee'
        }
    ),
    html.Div([
        dcc.Graph(
            id='age_balance',
            figure=fig,
            style={
                # "display": "inline-block",
                # "margin-left": "auto",
                # "margin-right": "auto",
            }
        )
    ])
], style={
    'margin': 'auto', 'width': "70%",
    'background-color': '#000000'
    }
)

if __name__ == '__main__':
    # app.run_server(debug=True)
    app.run_server(host='0.0.0.0', port=8001, debug=True)
