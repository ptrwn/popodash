class SQL_stmt():
    
    create_table_user = """CREATE TABLE IF NOT EXISTS user (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    age integer
                                );"""


    create_table_item = """ CREATE TABLE IF NOT EXISTS item (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        abv real NOT NULL,                                      
                                        kind text NOT NULL,
                                        amount_l real NOT NULL,
                                        price real NOL NULL
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
    insert_item = """INSERT INTO item (name, abv, kind, amount_l, price) VALUES (?, ?, ?, ?, ?);"""

    insert_user_party = """INSERT INTO users_parties (user_id, party_id) VALUES (?, ?);"""
    insert_user_item = """INSERT INTO users_items (user_id, item_id) VALUES (?, ?);"""

    select_full_data = """select u.id, u.name, i.id, i.name, p.id, p.name 
                        from user u 
                        left join users_items ui on u.id = ui.user_id 
                        left join item i on i.id = ui.item_id 
                        left join users_parties up on u.id = up.user_id 
                        left join party p on up.party_id = p.id;"""

