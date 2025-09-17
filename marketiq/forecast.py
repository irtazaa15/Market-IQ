import pandas as pd

def prophet_forecast(df_monthly: pd.DataFrame, periods:int=6):
    try:
        from prophet import Prophet
    except Exception:
        return None, 'Prophet not installed'
    if df_monthly.empty:
        return None, 'No data'
    m = Prophet(seasonality_mode='multiplicative')
    fit_df = df_monthly.rename(columns={'month':'ds','revenue':'y'})
    m.fit(fit_df[['ds','y']])
    future = m.make_future_dataframe(periods=periods, freq='MS')
    fc = m.predict(future)[['ds','yhat','yhat_lower','yhat_upper']]
    return fc.tail(periods), None
