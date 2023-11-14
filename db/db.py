from sqlalchemy import create_engine

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean, DateTime, Float, Enum
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.postgresql import ENUM


import pandas as pd

from config import Config
from pathlib import Path
from sql_statements import SQL_stmt

from random import randint, choice, choices
from constants import users, locations_to_kinds, MAX_USERS_PER_PARTY, MAX_LOC_PER_PARTY, MAX_ITEMS_USER_PARTY
from functools import partial

from faker import Faker
fake = Faker()

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255), nullable=True, unique=True)
    tg_username = Column(String(255), nullable=True, unique=True)


class Party(Base):
    __tablename__ = "party"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    start_dt = Column(DateTime(), nullable=True, default=None)
    end_dt = Column(DateTime(), nullable=True, default=None)


class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    address = Column(String(255))




class Item(Base):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    abv = Column(Float)
    drink_kinds = ('beer', 'wine', 'spirit', 'cocktail')
    kind = Column(Enum(*drink_kinds, name='drink_kinds_enum', create_type=False))



def main():

    try:
        engine = create_engine("postgresql+psycopg2://popodash:123qwe@localhost/popodash")
    except Exception as e:
        #TODO: replace with logger
        print('Could not access postgres database', repr(e))

    Base.metadata.create_all(engine)

    

    Session = sessionmaker(bind=engine)
    sess = Session()


if __name__ == '__main__':
    main()





# def revert(d):
#     '''Reverts a dictionary to 
#         {value1: [key1, key2, ...],
#         value2: [key1, key3, ...]}'''

#     rev = {}
#     for k in [*d]:
#         for v in d[k]:
#             if v not in [*rev]:
#                 rev[v] = [k]
#             else:
#                 rev[v].append(k)
#     return rev


# def create_connection():
#     conn = None
#     db_file =  Path().absolute() / Config.DB_FILE
#     try:
#         conn = sqlite3.connect(db_file)
#     except Error as e:
#         print(e)
#     return conn


# def create_table(conn, create_table_sql):
#     try:
#         c = conn.cursor()
#         c.execute(create_table_sql)
#     except Error as e:
#         print(e)


# def insert(conn, statement, params):
#     cur = conn.cursor()
#     cur.execute(statement, params)
#     conn.commit()
#     return cur.lastrowid


# def df_to_sql(conn, df, table_name):
#     df.to_sql(table_name, con=conn, if_exists='replace', index_label='id')


# def insert_item_loc(conn, name, location, vol, price):
#     cur = conn.cursor()
#     cur.execute(f"select id from location where name = '{location}';")
#     loc_id = cur.fetchone()[0]
#     cur.execute(f"select id from item where name = '{name}';")
#     item_id = cur.fetchone()[0]
#     cur.execute(SQL_stmt.insert_item_location, (item_id, loc_id, vol, price))
#     conn.commit()


# def arger(loc_ids):
#     return ', '.join([str(_) for _ in loc_ids])


# def insert_party_user_item_loc(conn, party_id, user_id, itemloc_id, order_dt):
#     cur = conn.cursor()
#     cur.execute(SQL_stmt.insert_party_user_itemloc, (party_id, user_id, itemloc_id, order_dt))
#     conn.commit()


# def main():

#     df_p = pd.read_csv('data/parties_dates.csv', parse_dates=['start_dt', 'end_dt'])
#     df_u = pd.DataFrame({'name': users})
#     df_i = pd.read_csv('data/drinks.csv', usecols=['name', 'abv', 'kind'])
#     df_l = pd.DataFrame({'name': [*locations_to_kinds]})

#     # moving pd dataframe index from 0 to 1 to make sqlite index start from 1 too
#     for df in [df_p, df_u, df_i, df_l]:
#         df.index = df.index + 1

#     df = pd.read_csv('data/drinks_vol_price_excl.csv')
#     df_excl = df.loc[df.exclusive_in.notna()]

#     # TODO: add price fluctuations -- set coefficients for 'cheap'
#     # and 'expensive' places.
#     df_any = df.loc[~df.exclusive_in.notna()]
#     kinds_to_locations = revert(locations_to_kinds)
#     df_any['location'] = df_any.kind.apply(lambda x: choice(kinds_to_locations[x]))
#     df_any1 = pd.DataFrame.copy(df_any)
#     df_any1['location'] = df_any.kind.apply(lambda x: choice(kinds_to_locations[x]))
#     df_any = pd.concat([df_any, df_any1])
#     df_any = df_any.drop_duplicates()

#     conn = create_connection()

#     with conn:

#         withconn = partial(df_to_sql, conn)
#         for df, table_name in zip((df_p, df_u, df_i, df_l), ('party', 'user', 'item', 'location')):
#             withconn(df, table_name)

#         create_table(conn, SQL_stmt.create_table_party_user_itemloc)
#         create_table(conn, SQL_stmt.create_table_item_location)

#         itemloc_conn = partial(insert_item_loc, conn)
#         party_user_conn = partial(insert_party_user_item_loc, conn)
#         df_excl.apply(lambda x: itemloc_conn(x['name'], x['exclusive_in'], x['vol'], x['price']), axis=1)
#         df_any.apply(lambda x: itemloc_conn(x['name'], x['location'], x['vol'], x['price']), axis=1)

#         for party in df_p.itertuples():
#             # the fewer places, the more probable
#             how_many_locations = choices(list(range(1,MAX_LOC_PER_PARTY)), weights = list(range(MAX_LOC_PER_PARTY,1, -1)))[0]
#             # the more users, the more probable
#             how_many_users = choices(list(range(1, MAX_USERS_PER_PARTY)), weights = list(range(1, MAX_USERS_PER_PARTY)))[0]

#             loc_ids = df_l.sample(how_many_locations).index.to_list()
#             user_ids = df_u.sample(how_many_users).index.to_list()

#             item_loc = pd.read_sql_query(f"select id from item_location where location_id in ({arger(loc_ids)});", conn)
#             item_loc_user_dt = item_loc.sample(randint(2, min(MAX_ITEMS_USER_PARTY, item_loc.shape[0])))
#             item_loc_user_dt['user_id'] = choices(user_ids, k=item_loc_user_dt.shape[0])
#             rantimes = [fake.date_time_between(start_date=party.start_dt, end_date=party.end_dt, ) for _ in range(item_loc_user_dt.shape[0])]
#             item_loc_user_dt['order_dt'] = list(pd.Series(rantimes).dt.strftime('%Y-%m-%d %H:%M:%S'))
#             item_loc_user_dt.apply(lambda x: party_user_conn(party.Index, x['user_id'], x['id'], x['order_dt']), axis=1)


# if __name__ == '__main__':
#     main()