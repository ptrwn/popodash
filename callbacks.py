from dash import Input, Output, ctx
import plotly.express as px
import pandas as pd
import datetime, time

from db.sql_statements import SQL_stmt
from sqlalchemy import create_engine
from sqlalchemy.sql import text

from app import app

try:
    engine = create_engine("postgresql+psycopg2://popodash:123qwe@localhost/popodash")
except Exception as e:
    #TODO: replace with logger
    print('Could not access postgres database', repr(e))

with engine.connect() as conn:
    df = pd.read_sql(text(SQL_stmt.select_whole_data), conn, parse_dates=['start_dt',	'end_dt'])


# TODO: the df must not be global
# either move to a func
# or mabe a frontend state? 
df['start_utime'] = df['start_dt'].apply(lambda x: int(time.mktime(x.timetuple())))
pp = df.party_id.unique().tolist()
uu = df.user_id.unique().tolist()

dates = df.start_dt.sort_values().dt.strftime('%Y-%m-%d %H:%M:%S')
dates = dates.unique().tolist()

# int is required here to mitigate the bug that shows labels 
# only if the keys are int or float
# https://community.plotly.com/t/range-slider-labels-not-showing/6605/2
# TODO: reuse start_utime column instead of calculating unix ts twice
times = {int(time.mktime(datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S').timetuple())): s for s in dates}


@app.callback(
    Output('scatter-parties', 'figure'),
    Output('users-at-party', 'figure'),
    Output('parties-dropdown', 'options'),
    Output('parties-dropdown', 'value'),
    Output('users-dropdown', 'options'),
    Output('users-dropdown', 'value'),
    Output('dates-range', 'value'),
    Input('parties-dropdown', 'value'),
    Input('users-dropdown', 'value'),
    Input('dates-range', 'value'),
    )
def update_figure_scatter(parties, users, dates):

    caller = ctx.triggered_id

    users_fil = df['user_id'].isin(users)
    parties_fil = df['party_id'].isin(parties)
    dates_fil = (dates[0] <= df['start_utime']) & (df['start_utime'] <= dates[1])

    caller_to_filters = {
        'users-dropdown': users_fil,
        'parties-dropdown': parties_fil,
        'dates-range': dates_fil, 
        None: users_fil & parties_fil & dates_fil
    }

    df_fil = df.loc[caller_to_filters.get(caller)]

    # TODO: DRY violation -- put them into a func,
    # maybe some class with service funcs? 
    df_u = df_fil[['user_name', 'user_id']].drop_duplicates()
    df_u = df_u.rename(columns={'user_id': 'value', 'user_name': 'label'})
    du = df_u.to_dict('records')

    df_p = df_fil[['party_name', 'party_id']].drop_duplicates()
    df_p = df_p.rename(columns={'party_id': 'value', 'party_name': 'label'})
    dp = df_p.to_dict('records')

    uu = df[['user_name', 'user_id']].drop_duplicates().rename(columns={'user_id': 'value', 'user_name': 'label'})
    uu = uu.to_dict('records')

    pp = df[['party_name', 'party_id']].drop_duplicates().rename(columns={'party_id': 'value', 'party_name': 'label'})
    pp = pp.to_dict('records')

    dates = df_fil.start_dt.sort_values().dt.strftime('%Y-%m-%d %H:%M:%S')
    dates = dates.unique().tolist()

    # int is required here to mitigate the bug that shows labels 
    # only if the keys are int or float
    # https://community.plotly.com/t/range-slider-labels-not-showing/6605/2
    # TODO: reuse start_utime column instead of calculating unix ts twice
    times = {int(time.mktime(datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S').timetuple())): s for s in dates}

    df_chart = df_fil.groupby(['party_id', 'party_name','start_utime', 'start_dt'])['price'].sum().reset_index()
    df_chart = df_chart.sort_values(by=['start_utime'])

    fig = px.scatter(df_chart, x="start_dt", y='price', hover_name="party_name", log_x=False, size_max=10)
    fig.update_layout(transition_duration=500)
    
    df_ch2 = df_fil.groupby(['user_name', 'item_name', 'kind', 'location_name', 'party_name']).value_counts().reset_index().rename(columns={0: 'count'})

    figus = px.parallel_categories(df_ch2, dimensions=['user_name', 'item_name', 'kind', 'location_name', 'party_name'],
    color="count", 
    # color_continuous_scale=px.colors.sequential.Inferno,
    #labels={'sex':'Payer sex', 'smoker':'Smokers at the table', 'day':'Day of week'}
    )
    # figus.update(layout_showlegend=False)
    figus.update_coloraxes(showscale=False)

    return fig, figus, pp, [x['value'] for x in dp], uu, [x['value'] for x in du], [list(times.keys())[0], list(times.keys())[-1]]

