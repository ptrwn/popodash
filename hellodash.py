from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

import sqlite3
from sql_statements import SQL_stmt

conn = sqlite3.connect('popo.db') 
          
sql_query = pd.read_sql_query (SQL_stmt.select_full_data, conn)
df = pd.DataFrame(sql_query)
df.set_axis(['user_id', 'user_name', 'item_id', 'item_name', 'party_id', 'party_name'], axis=1, inplace=True)

parties = df.party_name.unique().tolist()

app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        df.party_name.unique().tolist(),
        'select the party',
        id='party-dropdown'
    ),
    dcc.Graph(id='users-at-party'),
    
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
