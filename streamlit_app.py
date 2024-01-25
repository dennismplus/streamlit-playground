import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from icecream import ic

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)

# Yahoo Finance
msft = yf.Ticker("MSFT")
# ic(msft.info)
hist = msft.history(period="12mo")
# ic(hist)
# st.data_editor(
#     hist,
#     column_config={
#         "Close": st.column_config.LineChartColumn(
#             "Close Prices",
#             width="medium",
#             help="The sales volume in the last 6 months",
#             y_min=0,
#             y_max=100,
#         ),
#     },
#     hide_index=True,
# )
st.header('MSFT Close Price (12 months) ', divider='rainbow')
close_price_df = pd.DataFrame(hist, columns=['Close'])
st.line_chart(data=close_price_df, x=None, y=None, color=None, width=0, height=0, use_container_width=True)

st.header('MSFT Volume (12 months)', divider='rainbow')
volume_price_df = pd.DataFrame(hist, columns=['Volume'])
st.bar_chart(data=volume_price_df, x=None, y=None, color="#f446a6", width=0, height=0, use_container_width=True)

######################################################
left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})

option = st.selectbox(
    'Which number do you like best?',
    df['first column'])

'You selected: ', option


##########################################################
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
