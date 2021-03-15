import streamlit as st
import pandas as pd
from seaborn import color_palette
from simulation import main

# -- Set page config
apptitle = "2019 Lehigh Method NCAA Tournament Cheat Sheet"


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

st.set_page_config(page_title=apptitle, page_icon=":basketball:", layout="wide")

# st.set_page_config(layout="wide")
# df.style.format({"E": "{:.2f}"})


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
    return df


def simulate_tourney(num_sims, ratings_type):
    df = main(num_sims, ratings_type)
    return formatted_df(df)


# stable_spr_all, stable_spr_rookies = load_dataframes()


# Title the app
st.title("2019 Lehigh Method NCAA Tournament Cheat Sheet")
st.write("by Nathan Walker")


select_subset = st.sidebar.selectbox(
    "Select Ratings Type:", ["Sports Reference", "The Lehigh Method"]
)

num_sims = st.sidebar.text_input("How many simulations to run (100-100,000):")
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


# if select_subset == "All Players":
#     display_frame = stable_spr_all
# elif select_subset == "Rookies Only":
#     display_frame = stable_spr_rookies


# cm = color_palette("RdYlGn", as_cmap=True)
# display_frame = display_frame.style.background_gradient(cmap=cm, subset=['Adj Stable SPR'])
# st.dataframe(display_frame, width=3000, height=2000)
