from dash import Input, Output
import plotly.express as px
import pandas as pd

import sqlite3
from db.sql_statements import SQL_stmt

from app import app

conn = sqlite3.connect('popo.db') 
sql_query = pd.read_sql_query (SQL_stmt.select_full_data, conn) 


def get_lgh_per_party(df, party):

    df_p = df.loc[df.party_name == party]
    u_count = len(df_p.user_name.unique().tolist())
    df_p['lg'] = df_p.item_abv * df_p.item_amount
    party_duration = df_p.party_end - df_p.party_start
    td = party_duration.tolist()[0]
    hours = td.seconds / 3600
    lgh = sum(df_p.lg) / (hours * u_count)
    return lgh


def get_df(sql_query):
    df = pd.DataFrame(sql_query)
    df.set_axis(['user_id', 'user_name', 'item_id', 'item_name', 'item_abv', 'item_kind', 'item_amount', 'item_price', 'party_id', 'party_name', 'party_location', 'party_start', 'party_end'], axis=1, inplace=True)
    df['party_start'] = pd.to_datetime(df['party_start'])
    df['party_end'] = pd.to_datetime(df['party_end'])
    return df


df = get_df(sql_query)
parties = df.party_name.unique().tolist()


@app.callback(
    Output('users-at-party', 'figure'),
    Input('party-dropdown', 'value'))
def update_figure_barchart(selected_party):
    df_party = df.loc[df.party_name == selected_party]
    df_chart = df_party[['user_name', 'item_name']]
    df_chart = df_chart.groupby(['user_name', 'item_name']).size().reset_index().rename(columns={0: 'count'})

    fig = px.bar(df_chart, x="user_name", y="count", color="item_name", barmode="group")

    fig.update_layout(transition_duration=500)

    return fig


@app.callback(
    Output('scatter-parties', 'figure'),
    Input('average-dropdown', 'value'))
def updated_figure_scatter(average):

    modes = [df.loc[df.party_name == party, 'item_price'].mode()[0] for party in parties]
    medians = [df.loc[df.party_name == party, 'item_price'].median() for party in parties]
    means = [df.loc[df.party_name == party, 'item_price'].mean() for party in parties]
    lghs = [get_lgh_per_party(df, party) for party in parties]
    num_users = [len(df.loc[df.party_name == party, 'user_name'].unique().tolist()) for party in parties]
    mode_drink = [df.loc[df.party_name == party, 'item_kind'].mode()[0] for party in parties]
    name = [df.loc[df.party_name == party, 'party_name'].tolist()[0] for party in parties]


    summary_df = pd.DataFrame({
        'price_mode': modes,
        'price_median': medians,
        'price_mean': means, 
        'productivity': lghs, 
        'num_users': num_users,
        'most_frequent_drink': mode_drink,
        'name': name
    })



    fig = px.scatter(summary_df, x="productivity", y=average,
                 size="num_users", color="most_frequent_drink", hover_name="name",
                 log_x=False, size_max=60)
    

    fig.update_layout(transition_duration=500)

    return fig




# @app.callback(
#     Output('indicator-graphic', 'figure'),
#     Input('xaxis-column', 'value'),
#     Input('yaxis-column', 'value'),
#     Input('xaxis-type', 'value'),
#     Input('yaxis-type', 'value'),
#     Input('year--slider', 'value'))
# def update_graph(xaxis_column_name, yaxis_column_name,
#                  xaxis_type, yaxis_type,
#                  year_value):
#     dff = df[df['Year'] == year_value]

#     fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
#                      y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
#                      hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])

#     fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

#     fig.update_xaxes(title=xaxis_column_name,
#                      type='linear' if xaxis_type == 'Linear' else 'log')

#     fig.update_yaxes(title=yaxis_column_name,
#                      type='linear' if yaxis_type == 'Linear' else 'log')

#     return fig