import sqlite3
from sqlite3 import Error

from config import Config
from pathlib import Path
from sql_statements import SQL_stmt

from random import randint, choice
from constants import parties, users, types_to_items, locations

def create_connection():
    """ create a database connection to a SQLite database """
    conn = None
    db_file =  Path().absolute() / Config.DB_FILE
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
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


class Item():
    def __init__(self, amount_ml, price):
        self.group = choice(list(types_to_items.keys()))
        drink_from_group = choice(list(types_to_items[self.group])) 
        self.name = drink_from_group[0]
        self.abv = drink_from_group[1]
        self.amount_ml = amount_ml
        self.price = price

        


class User():
    def __init__(self, name):
        self.name = name
        self.age = randint(25, 50)


class Party():

    def __init__(self, name, start=None, end=None, location=None):
        self.name = name
        self.start = start
        self.end = end
        self.location = location
    




def main():

    conn = create_connection()

    with conn:
        create_table(conn, SQL_stmt.create_table_user)
        create_table(conn, SQL_stmt.create_table_party)
        create_table(conn, SQL_stmt.create_table_item)
        create_table(conn, SQL_stmt.create_table_users_parties)
        create_table(conn, SQL_stmt.create_table_users_items)

    with conn:

        for party in parties:
            party_id = insert(conn, SQL_stmt.insert_party, (party,))
            
            num_guests = randint(1, 5)
            for _ in range(num_guests):
                user_id = insert(conn, SQL_stmt.insert_user, (choice(users), ))
                u_p_id = insert(conn, SQL_stmt.insert_user_party, (user_id, party_id))
                num_items = randint(1, len(items))
                for _ in range(num_items):
                    item_id = insert(conn, SQL_stmt.insert_item, (choice(items),))
                    u_i_id = insert(conn, SQL_stmt.insert_user_item, (user_id, item_id))


if __name__ == '__main__':
    main()