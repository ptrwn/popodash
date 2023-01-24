import sqlite3
from sqlite3 import Error

from config import Config
from pathlib import Path
from sql_statements import SQL_stmt


def create_connection():
    """ create a database connection to a SQLite database """
    conn = None
    db_file =  Path().absolute() / Config.DB_FILE
    try:
        conn = sqlite3.connect(db_file)
        # conn = sqlite3.connect(':memory:')
    except Error as e:
        print(e)
    # finally:
    #     if conn:
    #         conn.close()

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



def main():

    conn = create_connection()

    with conn:
        create_table(conn, SQL_stmt.create_table_user)
        create_table(conn, SQL_stmt.create_table_party)
        create_table(conn, SQL_stmt.create_table_item)
        create_table(conn, SQL_stmt.create_table_users_parties)
        create_table(conn, SQL_stmt.create_table_users_items)


    with conn:

        user_id = insert(conn, SQL_stmt.insert_user, ('Bob',))
        print(user_id)

        party_id = insert(conn, SQL_stmt.insert_party, ('NewYear',))
        print(party_id)

        item_id = insert(conn, SQL_stmt.insert_item, ('Guinness',))
        print(item_id)

        u_p_id = insert(conn, SQL_stmt.insert_user_party, (user_id, party_id))
        print(u_p_id)

        u_i_id = insert(conn, SQL_stmt.insert_user_item, (user_id, item_id))
        print(u_i_id)

    


    


if __name__ == '__main__':
    main()