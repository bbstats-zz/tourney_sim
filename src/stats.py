import pandas as pd
import ssl
from src.constants import URL, JAKE_TO_BBR, TOURNEY_TEAMS
from scipy.stats import zscore

gt_df = pd.read_pickle("src/2021_sr.p")
GROUND_TRUTH = gt_df.loc[gt_df["School"].isin(TOURNEY_TEAMS)]["NRtg"]


def steal_ratings(
    df, ratings_col, ground_truth=GROUND_TRUTH.sort_values(ascending=False)
):
    df = df.sort_values(ratings_col, ascending=False).reset_index()
    df[ratings_col] = list(ground_truth)
    return df


def scale_ratings(ratings, ground_truth=GROUND_TRUTH):
    std = ground_truth.std()
    mean = ground_truth.mean()
    return zscore(ratings) * std + mean


def scale_ratings_from_df(df, rating_column):
    df[rating_column] = scale_ratings(df[rating_column])
    return df


def get_ratings(url=URL):

    # ssl._create_default_https_context = ssl._create_unverified_context
    # df = pd.read_html(URL)[0]
    # df.columns = df.columns.droplevel()
    # df = df.loc[~df["NRtg"].isin(["Adjusted", "NRtg"])]
    # df = df.apply(pd.to_numeric, errors="ignore")
    # df = df[[col for col in df.columns if "Unnamed: " not in col]]
    # df.to_pickle("src/2021_sr.p")
    df = pd.read_pickle("src/2021_sr.p")
    return df.loc[df["School"].isin(TOURNEY_TEAMS)]


def get_lehigh_method():
    df = pd.read_pickle("src/2021_tlm.p")
    return steal_ratings(df.loc[df["School"].isin(TOURNEY_TEAMS)], "TLM_NetRtg")


def get_srapm_ratings():
    df = pd.read_csv("src/srapm.csv")
    df = df.loc[(df["Season"] == "2020-21") & df["School"].isin(TOURNEY_TEAMS)]
    return steal_ratings(df, "RAPM")


def get_fivethirtyeight():
    df = pd.read_csv("src/fivethirtyeight.csv")
    return steal_ratings(df.loc[df["team"].isin(TOURNEY_TEAMS)], "rating")


def main():
    df = get_ratings()
    print(df)


if __name__ == "__main__":
    main()