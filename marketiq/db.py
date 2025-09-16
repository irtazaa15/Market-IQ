import os
from sqlalchemy import create_engine, text
import pandas as pd

def get_engine():
    url = os.getenv('DATABASE_URL', 'sqlite:///marketiq.db')
    return create_engine(url, pool_pre_ping=True)

def fetch_df(sql: str, params: dict | None = None) -> pd.DataFrame:
    params = params or {}
    eng = get_engine()
    with eng.connect() as conn:
        return pd.read_sql(text(sql), conn, params=params)
