import streamlit as st
import pandas as pd
from seaborn import color_palette
from simulation import main
import base64
from io import BytesIO
from datetime import datetime

# -- Set page config
apptitle = "2021 Lehigh Method NCAA Tournament Cheat Sheet"

CM = color_palette("RdYlGn", as_cmap=True)
NEW_COLUMNS = {
    "2": "Ro32",
    "3": "Sweet16",
    "4": "Elite8",
    "5": "Final4",
    "6": "Championship",
    "7": "Winner",
    "total_proj_wins": "Simulated # Wins",
    "true_volatility": "Volatility",
    "team": "Team",
}

st.set_page_config(
    page_title=apptitle,
    page_icon=":basketball:",
    layout="wide",
    initial_sidebar_state="expanded",
)


def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    df.to_excel(writer, index=False, sheet_name="Sheet1", float_format="%.2f")
    writer.save()
    processed_data = output.getvalue()
    return processed_data


def get_table_download_link(df, num_sims, source):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    curr_time = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{source}_{num_sims}_sims_{curr_time}.xlsx">Download Excel file</a>'  # decode b'abc' => abc


def formatted_df(df, column_mapping=NEW_COLUMNS):
    df.rename(columns=column_mapping, inplace=True)
    df = df[
        [
            "Team",
            "Ro32",
            "Sweet16",
            "Elite8",
            "Final4",
            "Championship",
            "Winner",
            "Simulated # Wins",
            "Volatility",
        ]
    ]
    df = df.sort_values("Simulated # Wins", ascending=False)
    df.set_index("Team", inplace=True, drop=True)

    rounding_formatting = {
        "Ro32": "{:,.1%}",
        "Sweet16": "{:,.1%}",
        "Elite8": "{:,.1%}",
        "Final4": "{:,.1%}",
        "Championship": "{:,.1%}",
        "Winner": "{:,.1%}",
        "Simulated # Wins": "{:,.1f}",
        "Volatility": "{:,.1f}",
    }

    dsmok_style = df.style.background_gradient(cmap=CM, subset=["Winner"])
    rounding_style = df.style.format(rounding_formatting)
    return rounding_style.use(dsmok_style.export())


def simulate_tourney(num_sims, ratings_type):
    df = main(num_sims, ratings_type)
    return df


st.title("2021 Lehigh Method NCAA Tournament Cheat Sheet")
st.write("by Nathan Walker")


select_subset = st.sidebar.selectbox(
    "Select Ratings Type:",
    [
        "The Lehigh Method",
        "538",
        "Sports Reference",
    ],  # , "Flancer sRAPM (Minutes = Average)"]
)

num_sims = st.sidebar.slider(
    "Number of Simulations to run:", 1000, 20000, value=5000, step=1000
)
go = st.sidebar.button("Run Simulations!")
working = False

if go:
    raw_frame = simulate_tourney(int(num_sims), select_subset)
    display_frame = formatted_df(raw_frame)

    link = get_table_download_link(
        display_frame.data.reset_index(drop=False), num_sims, select_subset
    )

    st.markdown(link, unsafe_allow_html=True)
    st.dataframe(display_frame, width=3000, height=2000)