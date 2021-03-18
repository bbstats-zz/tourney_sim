from src.brackets import Region, Bracket
from src.stats import (
    get_ratings,
    get_lehigh_method,
    get_srapm_ratings,
    get_fivethirtyeight,
    get_adjusted_lehigh_method
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
from frontend.constants import TLM_NAME, FTE_NAME


def main(num_sims=1000, select_subset=TLM_NAME):
    print(select_subset)
    if select_subset == TLM_NAME:
        ratings_df = get_adjusted_lehigh_method()
        ratings = dict(zip(ratings_df["Team"], ratings_df["RAPM"]))

    elif select_subset == FTE_NAME:
        ratings_df = get_fivethirtyeight()
        ratings = dict(zip(ratings_df["team"], ratings_df["rating"]))

    west = Region("W", west_teams, west_playin)
    east = Region("E", east_teams, east_playin)
    south = Region("S", south_teams, south_playin)
    midwest = Region("MW", midwest_teams, midwest_playin)
    bracket = Bracket(ratings, west, east, south, midwest)
    bracket.run_simulations(num_sims=num_sims)
    return bracket.output_df
