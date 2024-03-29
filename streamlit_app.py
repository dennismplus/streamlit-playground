import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from icecream import ic
from streamlit_echarts import st_echarts
import polars as pl

# Reward Coupons
st.title('CDM Rewards and Coupons Consumption Dashboard')
# Create the SQL connection to pets_db as specified in your secrets file.
conn = st.connection('neon_db', type='sql')
with conn.connect() as s:
    query = """
            SELECT
                DATE_TRUNC('month', transaction_date) AS month,
                SUM(CASE WHEN coupon_id IS NOT NULL THEN 1 ELSE 0 END) AS coupon,
                SUM(CASE WHEN reward_id IS NOT NULL THEN 1 ELSE 0 END) AS reward
            FROM Transactions
            WHERE coupon_id IS NOT NULL OR reward_id IS NOT NULL
            GROUP BY month
            ORDER BY month;
        """
    pl_df = pl.read_database(query=query, connection=s)
    ic(pl_df)
    st.header('Monthly Total Coupons & Rewards Used', divider='rainbow')
    st.bar_chart(data=pl_df, x='month', y=['coupon', 'reward'], color=["#f446a6", "#0000FF"], width=0, height=0,
                 use_container_width=True)

    # Weekly transactions
    st.header('Weekly transaction volume and amount', divider='rainbow')
    query = """
            SELECT
                DATE_TRUNC('week', transaction_date) AS transaction_week,
                COUNT(*) AS transaction_count,
                CAST(CEIL(SUM(amount)) AS INTEGER) AS total_transaction_amount
            FROM Transactions
            GROUP BY transaction_week
            ORDER BY transaction_week;
        """
    weekly_trx_df = pl.read_database(query, connection=s)
    ic(weekly_trx_df)
    weekly_trx_df = weekly_trx_df.rename(
        {"transaction_week": "week", "total_transaction_amount": "amount", "transaction_count": "volume"})
    st.bar_chart(data=weekly_trx_df, x='week', y=['volume'],
                 color=["#f446a6"], width=0, height=0, use_container_width=True)

    st.bar_chart(data=weekly_trx_df, x='week', y=['amount'],
                 color=["#0000FF"], width=0, height=0, use_container_width=True)

    query = """
            SELECT
                CASE
                    WHEN coupon_id IS NULL AND reward_id IS NULL THEN 'None'
                    WHEN coupon_id IS NOT NULL AND reward_id IS NOT NULL THEN 'Both'
                    WHEN coupon_id IS NOT NULL AND reward_id IS NULL THEN 'Coupon'
                    WHEN coupon_id IS NULL AND reward_id IS NOT NULL THEN 'Reward'
                END AS trx_group,
                COUNT(*) AS count
            FROM Transactions
            WHERE transaction_type = 'PURCHASE'::transaction_type_enum
            GROUP BY trx_group;
        """
    pl_df = pl.read_database(query, connection=s)
    pl_df = pl_df.rename({"trx_group": "name", "count": "value"})
    ic(pl_df)
    st.header('Transaction Allocation', divider='rainbow')
    option = {
        "legend": {"top": "bottom"},
        "toolbox": {
            "show": True,
            "feature": {
                "mark": {"show": True},
                "dataView": {"show": True, "readOnly": False},
                "restore": {"show": True},
                "saveAsImage": {"show": True},
            },
        },
        "series": [
            {
                "name": "Transaction Allocation",
                "type": "pie",
                "radius": [50, 250],
                "center": ["50%", "50%"],
                "roseType": "area",
                "itemStyle": {"borderRadius": 8},
                "data": pl_df.to_dicts(),
                "label": {
                    "formatter": '{a|{a}}{abg|}\n{hr|}\n  {b|{b}：}{c}  {per|{d}%}  ',
                    "backgroundColor": '#F6F8FC',
                    "borderColor": '#8C8D8E',
                    "borderWidth": 1,
                    "borderRadius": 4,
                    "rich": {
                        "a": {
                            "color": '#6E7079',
                            "lineHeight": 22,
                            "align": 'center'
                        },
                        "hr": {
                            "borderColor": '#8C8D8E',
                            "width": '100%',
                            "borderWidth": 1,
                            "height": 0
                        },
                        "b": {
                            "color": '#4C5058',
                            "fontSize": 12,
                            "fontWeight": 'bold',
                            "lineHeight": 25
                        },
                        "per": {
                            "color": '#fff',
                            "backgroundColor": '#4C5058',
                            "padding": [3, 4],
                            "borderRadius": 4
                        }
                    }
                },
            }
        ],
    }
    st_echarts(
        options=option, height="600px",
    )

    if s:
        s.close()

# Yahoo Finance
# Input for the stock ticker
st.header('Input Form', divider='rainbow')
ticker = st.text_input("Enter the stock ticker", "AAPL")
period = st.text_input("Enter the stock ticker ['1mo', '3mo', '6mo', 'ytd', '1y', '2y', '5y', '10y', 'max']", "5y")


@st.cache_data
def load_data(tick, p):
    tick_hist = yf.download(tick, period=p)
    tick_hist['MA50'] = tick_hist['Close'].rolling(50).mean()
    return tick_hist


hist = load_data(ticker, period)
st.header(ticker + ' Close Price (' + period + ' period) ', divider='rainbow')
close_price_df = pd.DataFrame(hist, columns=['Close'])
st.line_chart(data=close_price_df, x=None, y=None, color="#f446a6", width=0, height=0, use_container_width=True)

st.header(ticker + ' Volume (' + period + ' period) ', divider='rainbow')
volume_price_df = pd.DataFrame(hist, columns=['Volume'])
st.bar_chart(data=volume_price_df, x=None, y=None, color="#f446a6", width=0, height=0, use_container_width=True)

st.header(ticker + ' 50-days moving average', divider='rainbow')
# Set the title of the app
price_ma = pd.DataFrame(hist, columns=['Close', 'MA50'])
st.line_chart(data=price_ma, x=None, y=None, color=["#f446a6", "#f2f246"], width=0, height=0, use_container_width=True)


######################################################
def get_data():
    return pd.DataFrame({
        "lat": np.random.randn(200) / 50 + 37.76,
        "lon": np.random.randn(200) / 50 + -122.4,
        "team": ['A', 'B'] * 100
    })


# Initialization
if st.button('Generate new points'):
    st.session_state.df = get_data()
if 'df' not in st.session_state:
    st.session_state.df = get_data()
df = st.session_state.df

with st.form("my_form"):
    header = st.columns([1, 2, 2])
    header[0].subheader('Color')
    header[1].subheader('Opacity')
    header[2].subheader('Size')

    row1 = st.columns([1, 2, 2])
    colorA = row1[0].color_picker('Team A', '#0000FF')
    opacityA = row1[1].slider('A opacity', 20, 100, 50, label_visibility='hidden')
    sizeA = row1[2].slider('A size', 50, 200, 100, step=10, label_visibility='hidden')

    row2 = st.columns([1, 2, 2])
    colorB = row2[0].color_picker('Team B', '#FF0000')
    opacityB = row2[1].slider('B opacity', 20, 100, 50, label_visibility='hidden')
    sizeB = row2[2].slider('B size', 50, 200, 100, step=10, label_visibility='hidden')

    st.form_submit_button('Update map')

alphaA = int(opacityA * 255 / 100)
alphaB = int(opacityB * 255 / 100)

df['color'] = np.where(df.team == 'A', colorA + f'{alphaA:02x}', colorB + f'{alphaB:02x}')
df['size'] = np.where(df.team == 'A', sizeA, sizeB)

st.map(df, size='size', color='color')
