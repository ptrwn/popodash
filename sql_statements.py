class SQL_stmt():
    
    create_table_user = """CREATE TABLE IF NOT EXISTS user (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL
                                );"""

    create_table_party = """ CREATE TABLE IF NOT EXISTS party (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL
                                    ); """


    create_table_item = """ CREATE TABLE IF NOT EXISTS item (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL
                                    ); """

    create_table_users_parties = """ CREATE TABLE IF NOT EXISTS users_parties (
                                        id integer PRIMARY KEY,
                                        user_id integer NOT NULL,
                                        party_id integer NOT NULL
                                    ); """
    

    create_table_users_items = """ CREATE TABLE IF NOT EXISTS users_items (
                                        id integer PRIMARY KEY,
                                        user_id integer NOT NULL,
                                        item_id integer NOT NULL
                                    ); """
    
    insert_user = """INSERT INTO user (name) VALUES (?);"""
    insert_party = """INSERT INTO party (name) VALUES (?);"""
    insert_item = """INSERT INTO item (name) VALUES (?);"""

    insert_user_party = """INSERT INTO users_parties (user_id, party_id) VALUES (?, ?);"""
    insert_user_item = """INSERT INTO users_items (user_id, item_id) VALUES (?, ?);"""
