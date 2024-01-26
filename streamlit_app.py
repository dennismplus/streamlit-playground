import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from icecream import ic
from sqlalchemy import text
from streamlit_echarts import st_echarts

# Create the SQL connection to pets_db as specified in your secrets file.
conn = st.connection('neon_db', type='sql')

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

# Reward Coupons
with conn.session as s:
    trx_group = s.execute(text(
        """
            SELECT
                CASE
                    WHEN coupon_id IS NULL AND reward_id IS NULL THEN 'Not Using Any'
                    WHEN coupon_id IS NOT NULL AND reward_id IS NOT NULL THEN 'Using Both'
                    WHEN coupon_id IS NOT NULL AND reward_id IS NULL THEN 'Using Coupon Only'
                    WHEN coupon_id IS NULL AND reward_id IS NOT NULL THEN 'Using Reward Only'
                END AS transaction_group,
                COUNT(*) AS transaction_count
            FROM Transactions
            WHERE transaction_type = 'Purchase'
            GROUP BY transaction_group;
        """))
    trx_group_df = pd.DataFrame(trx_group, columns=['name', 'value'])
    pie_chart_dict = trx_group_df.to_dict(orient='records')
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
                "data": pie_chart_dict,
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
                        "fontSize": 14,
                        "fontWeight": 'bold',
                        "lineHeight": 33
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


######################################################
def get_data():
    df = pd.DataFrame({
        "lat": np.random.randn(200) / 50 + 37.76,
        "lon": np.random.randn(200) / 50 + -122.4,
        "team": ['A', 'B'] * 100
    })
    return df


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
