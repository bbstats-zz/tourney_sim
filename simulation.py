from src.brackets import Region, Bracket
from src.stats import (
    get_ratings,
    get_lehigh_method,
    get_srapm_ratings,
    get_fivethirtyeight,
)
from src.constants import (
    west_teams,
    west_playin,
    east_teams,
    east_playin,
    south_teams,
    south_playin,
    midwest_teams,
    midwest_playin,
)


def main(num_sims=1000, select_subset="Sports Reference"):
    if select_subset == "The Lehigh Method":
        ratings_df = get_lehigh_method()
        ratings = dict(zip(ratings_df["School"], ratings_df["TLM_NetRtg"]))

    elif select_subset == "Sports Reference":
        ratings_df = get_ratings()
        ratings = dict(zip(ratings_df["School"], ratings_df["NRtg"]))

    elif select_subset == "538":
        ratings_df = get_fivethirtyeight()
        ratings = dict(zip(ratings_df["team"], ratings_df["rating"]))

    elif select_subset == "Flancer sRAPM":
        ratings_df = get_srapm_ratings()
        ratings = dict(zip(ratings_df["School"], ratings_df["RAPM"]))

    west = Region("W", west_teams, west_playin)
    east = Region("E", east_teams, east_playin)
    south = Region("S", south_teams, south_playin)
    midwest = Region("MW", midwest_teams, midwest_playin)
    bracket = Bracket(ratings, west, east, south, midwest)
    bracket.run_simulations(num_sims=num_sims)
    return bracket.output_df
    # bracket.output_df.to_csv("output.csv")
