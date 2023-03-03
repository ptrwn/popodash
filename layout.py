from dash import dcc, html
import dash_bootstrap_components as dbc
from callbacks import uu, pp, times

layout =  dbc.Container(fluid=False, children=[

    dbc.Row(id='top-name', children=[
        html.Div([
            html.H1("popodash"),
            html.Hr(),
        ]),

    ]),
    dbc.Row(id='mid-controls', children=[
        dbc.Col(id='mid-left', children=[
            dbc.Label("Parties"),
            dcc.Dropdown(
                id='parties-dropdown',
                value=pp,
                multi=True,
                clearable=False),]),
        dbc.Col(id='mid-right', children=[
            dbc.Label("Users"),
            dcc.Dropdown(
                id='users-dropdown',
                value=uu,
                multi=True,
                clearable=False),]),]),
    dbc.Row(id='mid-time', className='p-4', children=[
        dbc.Label("Dates range"),
        dcc.RangeSlider(
            id='dates-range',
            min=list(times.keys())[0],
            max=list(times.keys())[-1],
            value=(list(times.keys())[0], list(times.keys())[-1]),
            step=None, # is here to prohibit selection between the marks
            marks={t : 
                    {"label": str(d.split(' ')[0]), 
                     "style": {"transform": "rotate(45deg)",
                                'font_family': 'Arial',
                                'font_size': '3px',
                                'text_align': 'center'
                               }} for t, d  in times.items()},),]),
    dbc.Row(id='bottom-charts', children=[    
        dbc.Col(id='generic-view-col', width=7, children=[dbc.Card([dcc.Graph(id='scatter-parties'),]),]),
        # dbc.Col(id='details-view-col', width=5, children=[dbc.Card([dcc.Graph(id='users-at-party'),]),] ),
    ]),
])
