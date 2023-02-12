import sqlite3
import pandas as pd
import numpy as np
from sqlite3 import Error

from config import Config
from pathlib import Path
from sql_statements import SQL_stmt

from random import randint, choice
from constants import users, locations_to_kinds, NUMBER_OF_GUESTS

from functools import partial



def create_connection():
    conn = None
    db_file =  Path().absolute() / Config.DB_FILE
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def insert(conn, statement, params):
    cur = conn.cursor()
    cur.execute(statement, params)
    conn.commit()
    return cur.lastrowid


def df_to_sql(conn, df, table_name):
    df.to_sql(table_name, con=conn, if_exists='replace', index_label='id')


def main():

    df_p = pd.read_csv('parties_dates.csv', parse_dates=['start_dt', 'end_dt'])
    df_u = pd.DataFrame({'name': users})
    df_i = pd.read_csv('drinks.csv', usecols=['drink', 'abv', 'kind'])
    df_l = pd.DataFrame({'name': list(locations_to_kinds.keys())})

    conn = create_connection()

    with conn:

        withconn = partial(df_to_sql, conn)
        for df, table_name in zip((df_p, df_u, df_i, df_l), ('party', 'user', 'item', 'location')):
            withconn(df, table_name)


        # df_p.to_sql('party', con=conn, if_exists='replace')
        # create_table(conn, SQL_stmt.create_table_user)
        # create_table(conn, SQL_stmt.create_table_item)
        # create_table(conn, SQL_stmt.create_table_users_parties)
        # create_table(conn, SQL_stmt.create_table_users_items)

        # parties = df_p.name.tolist()

        # for party_id, party in enumerate(parties, start=1):

        #     num_guests = randint(1, NUMBER_OF_GUESTS)
        #     party_location =  df_p.loc[df_p.name == party]['location'].item()
        #     locations_drinks_kinds = list(locations_to_kinds[party_location])
        #     df_loc_items = df_i.loc[df_i['kind'].isin(locations_drinks_kinds)]

        #     #TODO: Add processing for exclusive_in
        #     df_loc_items = df_loc_items.loc[:, df_loc_items.columns != "exclusive_in"]

        #     for _ in range(num_guests):
        #         # TODO add user age
        #         user_id = insert(conn, SQL_stmt.insert_user, (choice(users), ))
        #         u_p_id = insert(conn, SQL_stmt.insert_user_party, (user_id, party_id))
        #         num_items = randint(1, max(2, df_loc_items.shape[0]))

        #         for _ in range(num_items):
        #             item = df_loc_items.sample(1).to_dict('tight')['data'][0]
        #             item = tuple(item)
        #             item_id = insert(conn, SQL_stmt.insert_item, item)
        #             u_i_id = insert(conn, SQL_stmt.insert_user_item, (user_id, item_id))



if __name__ == '__main__':
    main()