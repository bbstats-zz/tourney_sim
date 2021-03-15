import pandas as pd
import ssl
from src.constants import URL, JAKE_TO_BBR


def get_ratings(url=URL):
    
    # ssl._create_default_https_context = ssl._create_unverified_context
    # df = pd.read_html(URL)[0]
    # df.columns = df.columns.droplevel()
    # df = df.loc[~df["NRtg"].isin(["Adjusted", "NRtg"])]
    # df = df.apply(pd.to_numeric, errors="ignore")
    # df = df[[col for col in df.columns if "Unnamed: " not in col]]
    # df.to_pickle("src/2021_sr.p")
    return pd.read_pickle("src/2021_sr.p")


def get_lehigh_method():
    return pd.read_pickle("src/2021_tlm.p")

def get_srapm_ratings():
    df= pd.read_csv('srapm.csv')
    df = df.loc[df["Season"]=="2020-21"]
    return df



def main():
    df = get_ratings()
    print(df)


if __name__ == "__main__":
    main()