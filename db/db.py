from sqlalchemy import create_engine

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float, Enum
from sqlalchemy.orm import declarative_base, relationship

import pandas as pd

from random import randint, choice
from constants import users, locations_to_kinds, MAX_USERS_PER_PARTY, MAX_LOC_PER_PARTY, MAX_ITEMS_USER_PARTY
from functools import partial

from faker import Faker
fake = Faker()

Base = declarative_base()

def revert(d):
    '''Reverts a dictionary to 
        {value1: [key1, key2, ...],
        value2: [key1, key3, ...]}'''

    rev = {}
    for k in [*d]:
        for v in d[k]:
            if v not in [*rev]:
                rev[v] = [k]
            else:
                rev[v].append(k)
    return rev

def df_to_sql(conn, df, table_name):
    df.to_sql(table_name, con=conn, if_exists='append', index_label='id')


class User(Base):
    __tablename__ = "user_"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255), nullable=True, unique=True)
    tg_username = Column(String(255), nullable=True, unique=True)
    parties = relationship("Party", secondary="party_user_itemloc", back_populates="users")
    itemlocs = relationship("ItemLocation", secondary="party_user_itemloc", back_populates="users")


class Party(Base):
    __tablename__ = "party"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    start_dt = Column(DateTime(), nullable=True, default=None)
    end_dt = Column(DateTime(), nullable=True, default=None)
    users = relationship("User", secondary="party_user_itemloc", back_populates="parties")
    itemlocs = relationship("ItemLocation",secondary="party_user_itemloc", back_populates="parties")


class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    address = Column(String(255))
    items = relationship("Item", secondary="item_location", back_populates="locations")


class Item(Base):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    abv = Column(Float)
    drink_kinds = ('beer', 'wine', 'spirit', 'cocktail')
    kind = Column(Enum(*drink_kinds, name='drink_kinds_enum', create_type=False))
    locations = relationship("Location", secondary="item_location", back_populates="items")


class ItemLocation(Base):
    __tablename__ = "item_location"
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("location.id"), nullable=False)
    volume = Column(Float)
    price = Column(Float)
    users = relationship("User", secondary="party_user_itemloc", back_populates="itemlocs")
    parties = relationship("Party", secondary="party_user_itemloc", back_populates="itemlocs")


class PartyUserItemloc(Base):
    __tablename__ = "party_user_itemloc"
    id = Column(Integer, primary_key=True)
    party_id = Column(Integer, ForeignKey("party.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user_.id"), nullable=False)
    itemloc_id = Column(Integer, ForeignKey("item_location.id"), nullable=False)
    order_dt = Column(DateTime(), nullable=True, default=None)


def main():

    try:
        engine = create_engine("postgresql+psycopg2://popodash:123qwe@localhost/popodash")
    except Exception as e:
        #TODO: replace with logger
        print('Could not access postgres database', repr(e))

    Base.metadata.create_all(engine)

    df_p = pd.read_csv('data/parties_dates.csv', parse_dates=['start_dt', 'end_dt'])
    df_u = pd.DataFrame({'name': users})
    df_i = pd.read_csv('data/drinks_vol_price_excl.csv')
    df_l = pd.DataFrame({'name': [*locations_to_kinds]})

    with engine.begin() as conn:
        withconn = partial(df_to_sql, conn)
        for df, table_name in zip((df_p, df_u, df_i.loc[:, ['name', 'abv', 'kind']], df_l), ('party', 'user_', 'item', 'location')):
            withconn(df, table_name)

    df_excl = df_i.loc[df_i.exclusive_in.notna()]
    df_excl['location'] = df_excl['exclusive_in'] 
    df_any = df_i.loc[~df_i.exclusive_in.notna()]

    kinds_to_locations = revert(locations_to_kinds)
    df_any['location'] = df_any.kind.apply(lambda x: choice(kinds_to_locations[x]))
    df_any1 = pd.DataFrame.copy(df_any)
    df_any1['location'] = df_any.kind.apply(lambda x: choice(kinds_to_locations[x]))
    df_any = pd.concat([df_any, df_any1], ignore_index=True)
    df_any = df_any.drop_duplicates()

    df_itemloc = pd.concat([df_any, df_excl], ignore_index=True)
    df_itemloc["location_id"] = df_itemloc["location"].apply(lambda x: df_l[df_l['name'] == x].index[0])
    df_itemloc["item_id"] = df_itemloc["name"].apply(lambda x: df_i[df_i['name'] == x].index[0])
    df_itemloc = df_itemloc.rename(columns={'vol': 'volume'})
    df_itemloc = df_itemloc.loc[:, ["item_id", "location_id", "volume", "price"]]

    with engine.begin() as conn:
        df_to_sql(conn, df_itemloc, "item_location")

    
    parties_itemlocs = []   
    for party in df_p.itertuples():

        how_many_locations, how_many_users = randint(1, MAX_LOC_PER_PARTY), randint(1, MAX_USERS_PER_PARTY)
        loc_ids = df_l.sample(how_many_locations).index.to_list()
        user_ids = df_u.sample(how_many_users).index.to_list()

        df_itemlocs_party = df_itemloc.loc[df_itemloc['location_id'].isin(loc_ids), 'location_id']
        df_itemlocs_party = df_itemlocs_party.reset_index().rename(columns={'index':'itemloc_id'})

        itemlocs_for_users = []
        for u_id in user_ids:
            df_u_itemlocs = df_itemlocs_party.sample(randint(2, len(loc_ids) * MAX_ITEMS_USER_PARTY), replace=True)
            df_u_itemlocs['user_id'] = u_id
            itemlocs_for_users.append(df_u_itemlocs)
        
        df_itemlocs_party_users = pd.concat(itemlocs_for_users)
        rantimes = [fake.date_time_between(start_date=party.start_dt, end_date=party.end_dt, ) for _ in range(df_itemlocs_party_users.shape[0])]

        df_itemlocs_party_users['location_id'] = df_itemlocs_party_users['location_id'].astype('category')
        df_itemlocs_party_users['location_id'] = df_itemlocs_party_users['location_id'].cat.set_categories(loc_ids)
        df_itemlocs_party_users.sort_values(['location_id'], inplace=True)

        df_itemlocs_party_users = df_itemlocs_party_users.drop('location_id', axis=1)
        df_itemlocs_party_users['order_dt'] = sorted(pd.Series(rantimes).dt.strftime('%Y-%m-%d %H:%M:%S'))
        df_itemlocs_party_users['party_id'] = party.Index

        parties_itemlocs.append(df_itemlocs_party_users)

    df_parties_itemlocs = pd.concat(parties_itemlocs).reset_index().drop('index', axis=1)

    with engine.begin() as conn:
        df_to_sql(conn, df_parties_itemlocs, "party_user_itemloc")

if __name__ == '__main__':
    main()
