from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

import sqlite3
from sql_statements import SQL_stmt

conn = sqlite3.connect('popo.db') 
          
sql_query = pd.read_sql_query (SQL_stmt.select_full_data, conn)
df = pd.DataFrame(sql_query)
df.set_axis(['user_id', 'user_name', 'item_id', 'item_name', 'item_abv', 'item_kind', 'item_amount', 'item_price', 'party_id', 'party_name', 'party_location'], axis=1, inplace=True)

parties = df.party_name.unique().tolist()

# BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"
# app = Dash(external_stylesheets=[BS])


app = Dash(external_stylesheets=[dbc.themes.COSMO])

top_card = dbc.Card(
    [
        dbc.CardImg(src="/static/images/placeholder286x180.png", top=True),
        dbc.CardBody(
            html.P("This card has an image at the top", className="card-text")
        ),
    ],
    style={"width": "18rem"},
)

bottom_card = dbc.Card(
    [
        dbc.CardBody(html.P("This has a bottom image", className="card-text")),
        dbc.CardImg(src="/static/images/placeholder286x180.png", bottom=True),
    ],
    style={"width": "18rem"},
)



app.layout =  dbc.Container(fluid=False, children=[

    dbc.Row([
        html.Div([
            html.H1("popodash"),
            html.Hr(),
        ]),

    ]),
    dbc.Row([
        html.Div([
            dbc.Label("Party"),
            dcc.Dropdown(
                df.party_name.unique().tolist(),
                'select the party',
                id='party-dropdown'
            ),
        ]),

    ]),
    dbc.Row([
    
    html.Div([
    dbc.Card([
    
        

    dcc.Graph(id='users-at-party'),

    html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("75% width card", className="card-title"),
                    html.P(
                        [
                            "This card uses the ",
                            html.Code("w-75"),
                            " class to set the width to 75%",
                        ],
                        className="card-text",
                    ),
                ]
            ),
            className="w-75 mb-3",
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("50% width card", className="card-title"),
                    html.P(
                        [
                            "This card uses the ",
                            html.Code("w-50"),
                            " class to set the width to 50%",
                        ],
                        className="card-text",
                    ),
                ]
            ),
            className="w-50",
        ),
    ]
)
    

]),    
]),
    








    ]),


    


])


@app.callback(
    Output('users-at-party', 'figure'),
    Input('party-dropdown', 'value'))
def update_figure(selected_party):
    df_party = df.loc[df.party_name == selected_party]
    df_chart = df_party[['user_name', 'item_name']]
    df_chart = df_chart.groupby(['user_name', 'item_name']).size().reset_index().rename(columns={0: 'count'})

    fig = px.bar(df_chart, x="user_name", y="count", color="item_name", barmode="group")

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

