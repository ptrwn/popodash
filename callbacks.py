from dash import Input, Output
import plotly.express as px
import pandas as pd
import datetime, time

import sqlite3
from db.sql_statements import SQL_stmt

from app import app

conn = sqlite3.connect('popo.db') 
df = pd.read_sql(SQL_stmt.select_whole_data, conn, parse_dates=['start_dt',	'end_dt'])
df['start_utime'] = df['start_dt'].apply(lambda x: int(time.mktime(x.timetuple())))
pp = df.party_id.unique().tolist()
uu = df.user_id.unique().tolist()


@app.callback(
    Output('scatter-parties', 'figure'),
    Output('parties-dropdown', 'options'),
    Output('parties-dropdown', 'value'),
    Output('users-dropdown', 'options'),
    Output('users-dropdown', 'value'),
    Input('parties-dropdown', 'value'),
    Input('users-dropdown', 'value'),
    # Input('dates-range', 'value') 
    )
def update_figure_scatter(parties, users):

    fil_users_parties = df['user_id'].isin(users) & df['party_id'].isin(parties)
    # fil_dates_range = (dates[0] <= df['start_utime']) & (df['start_utime'] <= dates[1])
    # parties_filtered = df.loc[fil_users_parties & fil_dates_range]['party_id'].unique().tolist()

    df_chart = df.loc[fil_users_parties]

    # TODO: DRY violation -- put them into a func,
    # maybe some class with service funcs? 

    df_u = df_chart[['user_name', 'user_id']].drop_duplicates()
    df_u = df_u.rename(columns={'user_id': 'value', 'user_name': 'label'})
    du = df_u.to_dict('records')

    df_p = df_chart[['party_name', 'party_id']].drop_duplicates()
    df_p = df_p.rename(columns={'party_id': 'value', 'party_name': 'label'})
    dp = df_p.to_dict('records')


    # dates = df.start_dt.sort_values().unique()
    # dates = df.start_dt.sort_values().dt.strftime('%Y-%m-%d %H:%M:%S')
    # dates = dates.unique().tolist()

    # int is required here to mitigate the bug that shows labels 
    # only if the keys are int or float
    # https://community.plotly.com/t/range-slider-labels-not-showing/6605/2
    # TODO: reuse start_utime column instead of calculating unix ts twice
    # times = {int(time.mktime(datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S').timetuple())): s for s in dates}


    df_chart = df_chart.groupby(['party_id', 'party_name','start_utime', 'start_dt'])['price'].sum().reset_index()
    df_chart = df_chart.sort_values(by=['start_utime'])


    #  size="num_users", color="most_frequent_drink", hover_name="name",
    fig = px.scatter(df_chart, x="start_dt", y='price', hover_name="party_name", log_x=False, size_max=10)
    fig.update_layout(transition_duration=500)


    return fig, dp, [x['value'] for x in dp], du, [x['value'] for x in du]
