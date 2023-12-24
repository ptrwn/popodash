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

    select_whole_data = """select u.name as user_name, u.id as user_id, 
                                i.name as item_name, i.id as item_id, i.abv, i.kind, 
                                p.name as party_name, p.id as party_id, p.start_dt, p.end_dt, 
                                l.id as location_id, l.name as location_name,
                                il.volume, il.price, puil.order_dt 
                            from user_ u 
                            inner join party_user_itemloc puil on u.id = puil.user_id 
                            left join item_location il on il.id = puil.itemloc_id  
                            left join party p on p.id = puil.party_id  
                            left join location l on l.id = il.location_id
                            left join item i on i.id = il.item_id;"""


    select_whole_data_inners = '''select u.name as user_name, u.id as user_id, 
                                i.name as item_name, i.id as item_id, i.abv, i.kind, 
                                p.name as party_name, p.id as party_id, p.start_dt, p.end_dt, 
                                l.id as location_id, l.name as location_name,
                                il.volume, il.price, puil.order_dt 
                    from user_ u 
                    inner join party_user_itemloc puil on u.id = puil.user_id 
                    inner join item_location il on il.id = puil.itemloc_id  
                    inner join party p on p.id = puil.party_id  
                    inner join location l on l.id = il.location_id
                    inner join item i on i.id = il.item_id;
    '''