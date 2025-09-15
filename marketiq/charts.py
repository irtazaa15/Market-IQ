import plotly.express as px

def kpi_cards(st, df_monthly):
    if df_monthly.empty:
        cols = st.columns(5)
        for c in cols: c.metric('-', '-')
        return
    revenue = float(df_monthly['revenue'].sum())
    orders = int(df_monthly['orders'].sum())
    customers = int(df_monthly['customers'].sum())
    aov = float(df_monthly['aov'].mean())
    cols = st.columns(5)
    cols[0].metric('Revenue', f'{revenue:,.0f}')
    cols[1].metric('Orders', f'{orders:,}')
    cols[2].metric('Customers', f'{customers:,}')
    cols[3].metric('AOV', f'{aov:,.2f}')
    if len(df_monthly) >= 2:
        last = df_monthly.iloc[-1]['revenue']
        prev = df_monthly.iloc[-2]['revenue']
        delta = 0 if prev == 0 else (last - prev) / prev * 100
        cols[4].metric('MoM Revenue', f'{last:,.0f}', f'{delta:+.1f}%')
    else:
        cols[4].metric('MoM Revenue', '-', '-')

def line_monthly(df):
    fig = px.line(df, x='month', y=['revenue','orders'], markers=True)
    fig.update_layout(height=360, legend_title='Metric', margin=dict(t=30,r=10,l=10,b=10))
    return fig

def donut_share(df):
    fig = px.pie(df, names='channel_name', values='revenue', hole=0.5)
    fig.update_layout(height=360, margin=dict(t=30,r=10,l=10,b=10))
    return fig

def bar_top(df):
    fig = px.bar(df, x='revenue', y='product_id', orientation='h')
    fig.update_layout(height=480, margin=dict(t=30,r=10,l=10,b=10), yaxis={'categoryorder':'total ascending'})
    return fig
