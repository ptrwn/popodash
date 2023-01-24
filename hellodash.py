from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

import sqlite3
from sql_statements import SQL_stmt

conn = sqlite3.connect('popo.db') 
          
sql_query = pd.read_sql_query (SQL_stmt.select_full_data, conn)

# df = pd.DataFrame(sql_query, columns = ['product_id', 'product_name', 'price'])
df = pd.DataFrame(sql_query)
df.set_axis(['user_id', 'user_name', 'item_id', 'item_name', 'party_id', 'party_name'], axis=1, inplace=True)

app = Dash(__name__)

# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
