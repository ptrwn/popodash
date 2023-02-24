class SQL_stmt():
    
    create_table_user = """CREATE TABLE IF NOT EXISTS user (
                                    id INTEGER PRIMARY KEY,
                                    name text NOT NULL
                                );"""
    
    create_table_location = """CREATE TABLE IF NOT EXISTS location (
                                id INTEGER PRIMARY KEY,
                                name text NOT NULL
                            );"""


    create_table_item = """ CREATE TABLE IF NOT EXISTS item (
                                        id INTEGER PRIMARY KEY,
                                        name text NOT NULL,
                                        abv real NOT NULL,                                      
                                        kind text NOT NULL
                                    ); """
    

    create_table_party = """ CREATE TABLE IF NOT EXISTS party (
                                    id INTEGER PRIMARY KEY,
                                    name text NOT NULL,
                                    start_dt text, 
                                    end_dt text
                                ); """


    create_table_party_user_itemloc = """ CREATE TABLE IF NOT EXISTS party_user_itemloc (
                                        id INTEGER PRIMARY KEY,
                                        party_id INTEGER NOT NULL,
                                        user_id INTEGER NOT NULL,
                                        itemloc_id INTEGER NOT NULL,
                                        order_dt text,
                                        FOREIGN KEY(party_id) REFERENCES party(id),
                                        FOREIGN KEY(user_id) REFERENCES user(id),
                                        FOREIGN KEY(itemloc_id) REFERENCES item_location(id)
                                    ); """
    

    create_table_item_location = """ CREATE TABLE IF NOT EXISTS item_location (
                                        id INTEGER PRIMARY KEY,
                                        item_id INTEGER NOT NULL,
                                        location_id INTEGER NOT NULL,
                                        volume real NOT NULL,
                                        price real NOT NULL,
                                        FOREIGN KEY(item_id) REFERENCES item(id),
                                        FOREIGN KEY(location_id) REFERENCES location(id)
                                    ); """
    
    insert_item_location = """INSERT INTO item_location (item_id, location_id, volume, price) VALUES (?, ?, ?, ?);"""

    insert_party_user_itemloc = """INSERT INTO party_user_itemloc (party_id, user_id, itemloc_id, order_dt) VALUES (?, ?, ?, ?);"""



    # insert_user = """INSERT INTO user (name) VALUES (?);"""
    # insert_party = """INSERT INTO party (name) VALUES (?);"""
    # insert_item = """INSERT INTO item (name, abv, kind, amount_l, price) VALUES (?, ?, ?, ?, ?);"""

    # insert_user_party = """INSERT INTO users_parties (user_id, party_id) VALUES (?, ?);"""
    # insert_user_item = """INSERT INTO users_items (user_id, item_id) VALUES (?, ?);"""

    # select_full_data = """select u.id, u.name, i.id, i.name, i.abv, i.kind, i.amount_l, i.price, p.id, p.name, p.location, p.start, p.end 
    #                     from user u 
    #                     left join users_items ui on u.id = ui.user_id 
    #                     left join item i on i.id = ui.item_id 
    #                     left join users_parties up on u.id = up.user_id 
    #                     left join party p on up.party_id = p.id;"""



# sqlite> select l.name, i.drink from location l left join item_location il on l.id =
#  il.location_id left join item i on i.id = il.item_id;
# name|drink
# joyce|
# amster|
# ambar|buzbac white
# ambar|buzbac red
# touchdown|
# moretenders|bullshitter
# clever|ohota krepkoe
# galaktion|kindzmarauli
# galaktion|khvanchkara
# galaktion|chacha
# sqlite>


# sqlite> select l.name, i.drink from location l inner join item_location il on l.id
# = il.location_id inner join item i on i.id = il.item_id;
# name|drink
# clever|ohota krepkoe
# galaktion|kindzmarauli
# ambar|buzbac white
# ambar|buzbac red
# galaktion|khvanchkara
# galaktion|chacha
# moretenders|bullshitter

# sqlite> select l.name, i.drink, il.volume, il. price from location l inner join item_location il on l.id = il.location_id inner join item i on i.id = il.item_id;  