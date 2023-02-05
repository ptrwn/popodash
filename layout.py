from dash import dcc, html
import dash_bootstrap_components as dbc

from callbacks import parties


layout =  dbc.Container(fluid=False, children=[

    dbc.Row(id='top-name', children=[
        html.Div([
            html.H1("popodash"),
            html.Hr(),
        ]),

    ]),
    dbc.Row(id='mid-controls', children=[
        dbc.Label("Party"),
        dcc.Dropdown(
            parties,            
            'select the party',
            id='party-dropdown'),
        dbc.Label("Price metric"),
        dcc.Dropdown(
            options=[
                {'label': 'Mean', 'value': 'price_mean'},
                {'label': 'Mode', 'value': 'price_mode'},
                {'label': 'Median', 'value': 'price_median'},
            ],
            value='price_mean',
            id='average-dropdown'
        )

        
    ]),
    dbc.Row(id='bottom-charts', children=[    
        dbc.Col(id='generic-view-col', width=7, children=[dbc.Card([dcc.Graph(id='scatter-parties'),]),]),
        dbc.Col(id='details-view-col', width=5, children=[dbc.Card([dcc.Graph(id='users-at-party'),]),] ),
    ]),
])
