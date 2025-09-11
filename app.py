import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from marketiq.db import fetch_df
from marketiq.queries import MONTHLY_KPIS, CHANNEL_SHARE, TOP_PRODUCTS
from marketiq.charts import kpi_cards, line_monthly, donut_share, bar_top
from marketiq.forecast import prophet_forecast

load_dotenv()

st.set_page_config(page_title='MarketIQ, Real-Time Sales & Forecasting', page_icon='📈', layout='wide')
st.title('📈 MarketIQ, Real-Time Sales & Forecasting')
st.caption('SQL-backed analytics with forecasting. Demo uses SQLite; set DATABASE_URL for Postgres/MySQL.')

fallback_start = '2024-01-01'
fallback_end = '2025-10-31'

st.sidebar.header('Filters')
start = st.sidebar.date_input('Start date', value=pd.to_datetime(fallback_start).date())
end = st.sidebar.date_input('End date', value=pd.to_datetime(fallback_end).date())
params = {'start': start.isoformat(), 'end': end.isoformat()}

st.subheader('Overview')
monthly = fetch_df(MONTHLY_KPIS, params)
if not monthly.empty:
    monthly['month'] = pd.to_datetime(monthly['month'])
kpi_cards(st, monthly)

c1, c2 = st.columns((3,2))
with c1:
    st.plotly_chart(line_monthly(monthly), config={'responsive': True})
with c2:
    ch = fetch_df(CHANNEL_SHARE, params)
    st.plotly_chart(donut_share(ch), config={'responsive': True})

st.subheader('Top Products')
top = fetch_df(TOP_PRODUCTS, params)
st.plotly_chart(bar_top(top), config={'responsive': True})

st.header('Forecasts')
if monthly.empty:
    st.info('No monthly data to forecast.')
else:
    fc, err = prophet_forecast(monthly[['month','revenue']])
    if err:
        st.warning(f'Forecast unavailable: {err}')
    else:
        st.dataframe(fc)
