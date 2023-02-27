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


# TODO: DRY violation -- put them into a func,
# maybe some class with service funcs? 

df_u = df[['user_name', 'user_id']].drop_duplicates()
df_u = df_u.rename(columns={'user_id': 'value', 'user_name': 'label'})
du = df_u.to_dict('records')

df_p = df[['party_name', 'party_id']].drop_duplicates()
df_p = df_p.rename(columns={'party_id': 'value', 'party_name': 'label'})
dp = df_p.to_dict('records')

dates = df.start_dt.sort_values().unique()
dates = df.start_dt.sort_values().dt.strftime('%Y-%m-%d %H:%M:%S')
dates = dates.unique().tolist()

# int is required here to mitigate the bug that shows labels 
# only if the keys are int or float
# https://community.plotly.com/t/range-slider-labels-not-showing/6605/2
# TODO: reuse start_utime column instead of calculating unix ts twice
times = {int(time.mktime(datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S').timetuple())): s for s in dates}


@app.callback(
    Output('scatter-parties', 'figure'),
    Input('parties-dropdown', 'value'),
    Input('users-dropdown', 'value'),
    Input('dates-range', 'value') 
    )
def updated_figure_scatter(parties, users, dates):

    
    print(parties)
    print(users)
    print(dates)

    fil_users_parties = df['user_id'].isin(users) & df['party_id'].isin(parties)
    fil_dates_range = (dates[0] <= df['start_utime']) & (df['start_utime'] <= dates[1])
    parties_filtered = df.loc[fil_users_parties & fil_dates_range]['party_id'].unique().tolist()
    fil_parties = df['party_id'].isin(parties_filtered)
    df_chart = df.loc[fil_parties]
    df_chart = df_chart.groupby(['party_id', 'party_name','start_utime', 'start_dt'])['price'].sum().reset_index()
    df_chart = df_chart.sort_values(by=['start_utime'])


    #  size="num_users", color="most_frequent_drink", hover_name="name",
    fig = px.scatter(df_chart, x="start_dt", y='price', hover_name="party_name", log_x=False, size_max=10)
    

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


# @app.callback(
#     Output('users-at-party', 'figure'),
#     Input('party-dropdown', 'value'))
# def update_figure_barchart(selected_party):
#     df_party = df.loc[df.party_name == selected_party]
#     df_chart = df_party[['user_name', 'item_name']]
#     df_chart = df_chart.groupby(['user_name', 'item_name']).size().reset_index().rename(columns={0: 'count'})

#     fig = px.bar(df_chart, x="user_name", y="count", color="item_name", barmode="group")

#     fig.update_layout(transition_duration=500)

#     return fig


# def get_lgh_per_party(df, party):

#     df_p = df.loc[df.party_name == party]
#     u_count = len(df_p.user_name.unique().tolist())
#     df_p['lg'] = df_p.item_abv * df_p.item_amount
#     party_duration = df_p.party_end - df_p.party_start
#     td = party_duration.tolist()[0]
#     hours = td.seconds / 3600
#     lgh = sum(df_p.lg) / (hours * u_count)
#     return lgh
