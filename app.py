import streamlit as st
import pandas as pd
from simulation import main
from frontend.utils import get_table_download_link, formatted_df
from frontend.constants import TLM_NAME, FTE_NAME



#@st.cache
def simulate_tourney(num_sims, ratings_type):
    df = main(num_sims, ratings_type)
    return df

def run(num_sims=5000, select_subset=TLM_NAME):
    raw_frame = simulate_tourney(int(num_sims), select_subset)
    display_frame = formatted_df(raw_frame)

    link = get_table_download_link(
        display_frame.data.reset_index(drop=False), num_sims, select_subset
    )

    slot1.markdown(link, unsafe_allow_html=True)
    slot2.dataframe(display_frame, width=4000, height=2000)

@st.cache
def first_run():
    run()


apptitle = "2021 Lehigh Method NCAA Tournament Cheat Sheet"

st.set_page_config(
    page_title=apptitle,
    page_icon=":basketball:",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.title("2021 Lehigh Method NCAA Tournament Cheat Sheet")
st.write("by Nathan Walker")
slot1 = st.empty()
slot2 = st.empty()
st.image("src/dukesucks.png")

select_subset = st.sidebar.selectbox(
    "Select Ratings Type:",
    [
        TLM_NAME,
        FTE_NAME,
        #"Flancer sRAPM",
        #"Sports Reference",
    ],
    index=0,  # , "Flancer sRAPM (Minutes = Average)"]
)

num_sims = st.sidebar.slider(
    "Number of Simulations to run:", 1000, 20000, value=5000, step=1000
)
go = st.sidebar.button("Run Simulations!")

first_run()
if go:
    run(num_sims, select_subset)
