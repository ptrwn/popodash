from dash import dcc, html
import dash_bootstrap_components as dbc

from datetime import datetime

from callbacks import times, du, dp

layout =  dbc.Container(fluid=False, children=[

    dbc.Row(id='top-name', children=[
        html.Div([
            html.H1("popodash"),
            html.Hr(),
        ]),

    ]),
    dbc.Row(id='mid-controls', children=[
        dbc.Label("Parties"),
        dcc.Dropdown(
            options=dp,
            value=[x['value'] for x in dp],
            multi=True,
            placeholder='select the parties',
            clearable=False,
            id='parties-dropdown'),
        dbc.Label("Users"),
        dcc.Dropdown(
            options=du,
            value=[x['value'] for x in du],
            multi=True,
            placeholder='select the users',
            clearable=False,
            id='users-dropdown'),
        dbc.Label("Dates range"),
        dcc.RangeSlider(
            min=list(times.keys())[0],
            max=list(times.keys())[-1],
            value=(list(times.keys())[0], list(times.keys())[-1]),
            step=None, # is needed to prohibit selection between the marks
            marks={t : 
                    {"label": str(d.split(' ')[0]), 
                     "style": {"transform": "rotate(45deg)",
                                'font_family': 'Arial',
                                'font_size': '3px',
                                'text_align': 'center'
                               }} for t, d  in times.items()},
            id='dates-range'),
    ]),
    dbc.Row(id='bottom-charts', children=[    
        dbc.Col(id='generic-view-col', width=7, children=[dbc.Card([dcc.Graph(id='scatter-parties'),]),]),
        # dbc.Col(id='details-view-col', width=5, children=[dbc.Card([dcc.Graph(id='users-at-party'),]),] ),
    ]),
])
