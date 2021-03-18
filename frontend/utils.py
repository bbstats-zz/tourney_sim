from frontend.constants import CM, HOT, MONEY, NEW_COLUMNS
import base64
from io import BytesIO
from datetime import datetime
import pandas as pd

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
    df["team"]=df["team"]+" ("+df["seed"].map(str)+")"
    df.rename(columns=column_mapping, inplace=True)
    df = df[
        [
            "Region",
            #"Seed",
            "Team",
            "Ro32",
            "Sweet16",
            "Elite8",
            "Final4",
            "Championship",
            "Winner",
            "Sim # Wins",
            "Wins>Seed Exp",
            "Volatility",
            "ESPN ROI",
            "Value Rating"
        ]
    ]
    df = df.sort_values("Sim # Wins", ascending=False)
    df.set_index("Team", inplace=True, drop=True)

    rounding_formatting = {
        "Ro32": "{:,.1%}",
        "Sweet16": "{:,.1%}",
        "Elite8": "{:,.1%}",
        "Final4": "{:,.1%}",
        "Championship": "{:,.1%}",
        "Winner": "{:,.1%}",
        "Sim # Wins": "{:,.2f}",
        "Wins>Seed Exp":"{:,.2f}",
        "Volatility": "{:,.1f}",
        "ESPN ROI": "{:.0f}",
        "Value Rating": "{:.0f}",
    }

    s = (
        df.style.background_gradient(cmap=CM, subset=["Winner", "Sim # Wins","Wins>Seed Exp"])
        .background_gradient(cmap=HOT, subset=["Volatility"])
        .background_gradient(cmap=MONEY, subset=["ESPN ROI","Value Rating"])
        .format(rounding_formatting)
    )
    return s




