import os
import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine

SCHEMA = 'prices'

DB_CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING")

engine = create_engine(f"postgresql+psycopg2://{DB_CONNECTION_STRING}")

df = yf.download('AAPL', start='2023-04-01', end='2023-04-06')

df.to_sql('AAPL_prices', engine, if_exists='append', schema=SCHEMA)

res = pd.read_sql_table('AAPL_prices', engine, schema=SCHEMA)

print(res)