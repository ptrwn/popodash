import sqlite3
import pandas as pd
import numpy as np
from sqlite3 import Error

from config import Config
from pathlib import Path
from sql_statements import SQL_stmt

from random import randint, choice
from constants import users, locations_to_kinds, NUMBER_OF_GUESTS



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


loc = list(locations_to_kinds.keys())

def main():

    df_p = pd.read_csv('parties_dates.csv', parse_dates=['start', 'end'])
    places = list(locations_to_kinds.keys())
    picked_places = np.random.choice(places, size=df_p.shape[0], replace=True)
    df_p['location'] = picked_places

    df_i = pd.read_csv('drinks.csv')

    conn = create_connection()

    with conn:
        df_p.to_sql('party', con=conn, if_exists='replace')
        create_table(conn, SQL_stmt.create_table_user)
        create_table(conn, SQL_stmt.create_table_item)
        create_table(conn, SQL_stmt.create_table_users_parties)
        create_table(conn, SQL_stmt.create_table_users_items)

        parties = df_p.party.tolist()

        for party_id, party in enumerate(parties):

            num_guests = randint(1, NUMBER_OF_GUESTS)
            party_location =  df_p.loc[df_p.party == party]['location'].item()
            locations_drinks_kinds = list(locations_to_kinds[party_location])
            df_loc_items = df_i.loc[df_i['kind'].isin(locations_drinks_kinds)]

            #TODO: Add processing for exclusive_in
            df_loc_items = df_loc_items.loc[:, df_loc_items.columns != "exclusive_in"]

            for _ in range(num_guests):
                # TODO add user age
                user_id = insert(conn, SQL_stmt.insert_user, (choice(users), ))
                u_p_id = insert(conn, SQL_stmt.insert_user_party, (user_id, party_id))
                num_items = randint(1, max(2, df_loc_items.shape[0]))

                for _ in range(num_items):
                    item = df_loc_items.sample(1).to_dict('tight')['data'][0]
                    item = tuple(item)
                    item_id = insert(conn, SQL_stmt.insert_item, item)
                    u_i_id = insert(conn, SQL_stmt.insert_user_item, (user_id, item_id))



if __name__ == '__main__':
    main()