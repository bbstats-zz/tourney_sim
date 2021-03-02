# bracket = [{'E':['1_seed','16_seed','8_seed','9_seed','5_seed','12_seed','4_seed','13_seed','6_seed','11_seed','3_seed','14_seed','7_seed','10_seed','2_seed','15_seed'],
# ]

# play_in_dict = {16: ('North Carolina','West Virginia')}
from itertools import combinations
from typing import List
import pandas as pd
import scipy.stats


def flatten(lst: List) -> List:
    return [item for sublist in lst for item in sublist]


class Region:
    def __init__(self, region_name, bid_teams, play_in_dict):
        self.region_name = region_name
        self.bid_teams = bid_teams
        self.seeds = [1, 16, 8, 9, 5, 12, 4, 13, 6, 11, 3, 14, 7, 10, 2, 15]
        self.play_in_dict = play_in_dict
        self.play_in_seeds = list(self.play_in_dict.keys())
        self.seed_teams()

    def seed_teams(self):
        """take the ordered list of bid teams (non-play-in)
        and play-in dictionary and make a dictionary of all team:seed combos"""
        self.team_seeds = {}
        team_idx = 0
        for seed in self.seeds:
            if seed in self.play_in_seeds:
                team_a, team_b = self.play_in_dict[seed]
                self.team_seeds[team_a] = seed
                self.team_seeds[team_b] = seed
            else:
                team = self.bid_teams[team_idx]
                self.team_seeds[team] = seed
                team_idx += 1


def get_probabilities_df(ratings, exp_stdev):
    team_combos = combinations(ratings.keys(), 2)
    df = pd.DataFrame(list(team_combos), columns=["a", "b"])
    df["a_rtg"] = df["a"].map(ratings)
    df["b_rtg"] = df["b"].map(ratings)
    df["rtg_diff"] = df["a_rtg"] - df["b_rtg"]
    df["p_win_a"] = scipy.stats.norm(0, exp_stdev).cdf(df["a_rtg"] - df["b_rtg"])
    df["p_win_b"] = 1 - df["p_win_a"]
    return df


# class Bracket(Region):
#     def __init__(self):
#         super().__init__(actuals, predictions)