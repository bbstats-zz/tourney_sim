import pandas as pd
import ssl


YEAR = "2021"
URL = f"https://www.sports-reference.com/cbb/seasons/{YEAR}-ratings.html"


def get_ratings(url=URL):
    ssl._create_default_https_context = ssl._create_unverified_context
    df = pd.read_html(URL)[0]
    df.columns = df.columns.droplevel()
    df = df.loc[~df["NRtg"].isin(["Adjusted", "NRtg"])]
    df = df.apply(pd.to_numeric, errors="ignore")
    df = df[[col for col in df.columns if "Unnamed: " not in col]]
    return df


def main():
    df = get_ratings()
    print(df)


if __name__ == "__main__":
    main()