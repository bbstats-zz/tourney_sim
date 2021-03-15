import streamlit as st
import pandas as pd
from seaborn import color_palette
from simulation import main

# -- Set page config
apptitle = "2021 Lehigh Method NCAA Tournament Cheat Sheet"


NEW_COLUMNS = {
    "2": "Ro32",
    "3": "Sweet16",
    "4": "Elite8",
    "5": "Final4",
    "6": "Championship",
    "7": "Winner",
    "total_proj_wins": "Simulated # Wins",
    "total_volatility": "Volatility",
    "team": "Team",
}

st.set_page_config(page_title=apptitle, page_icon=":basketball:", layout="wide",initial_sidebar_state = "expanded")


def formatted_df(df, column_mapping=NEW_COLUMNS):
    df = df.rename(columns=column_mapping)
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
    df.set_index("Team",inplace=True, drop=True)
    return df


def simulate_tourney(num_sims, ratings_type):
    df = main(num_sims, ratings_type)
    return formatted_df(df)


st.title("2021 Lehigh Method NCAA Tournament Cheat Sheet")
st.write("by Nathan Walker")


select_subset = st.sidebar.selectbox(
    "Select Ratings Type:", ["Sports Reference", "The Lehigh Method"]
)

num_sims = st.sidebar.slider("Number of Simulations to run:", 1, 20000)
go = st.sidebar.button("Run Simulations!")
working = False

if working:
    st.text("Working...")
else:
    st.text("")

if go:
    working = True
    display_frame = simulate_tourney(int(num_sims), select_subset)
    working = False
    cm = color_palette("RdYlGn", as_cmap=True)
    display_frame = display_frame.style.background_gradient(cmap=cm, subset=["Winner"])
    st.dataframe(display_frame, width=3000, height=2000)