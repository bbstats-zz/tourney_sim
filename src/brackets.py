from itertools import permutations
from typing import List, Dict
import pandas as pd
import scipy.stats
import numpy as np
import json
import math

#from line_profiler import profile


def store_object_as_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f)


def flatten(lst: List) -> List:
    return [item for sublist in lst for item in sublist]


class Region:
    def __init__(self, region_name: str, bid_teams: List, play_in_dict: Dict = {}):
        self.region_name = region_name
        self.bid_teams = bid_teams
        self.play_in_dict = play_in_dict
        self.seeds = [1, 16, 8, 9, 5, 12, 4, 13, 6, 11, 3, 14, 7, 10, 2, 15]
        self.play_in_seeds = list(self.play_in_dict.keys())
        self.play_in_teams = flatten(list(self.play_in_dict.values()))
        self.teams = self.bid_teams + self.play_in_teams
        self.seed_teams()

    def seed_teams(self):
        """take the ordered list of bid teams (non-play-in)
        and play-in dictionary and make a dictionary of all team:seed combos."""
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


class Bracket:
    @profile
    def __init__(self, ratings: Dict, *regions: Region, exp_stdev: float = 16.5):

        self.regions = regions
        self.ratings = ratings
        self.exp_stdev = exp_stdev

        self.teams = []
        for region in self.regions:
            self.teams += region.teams
        self.remaining_teams = self.teams

        self.get_probabilities_dict()

        self.play_in_matchups = flatten([region.play_in_teams for region in regions])
        self.play_in = len(self.play_in_matchups) > 0

        self.n_rounds = int(np.log2(len(self.teams))) + self.play_in
        print(f"rounds: {self.n_rounds}")

        self.current_round = None
        self.current_round_is_play_in = False
        self.current_round_team_a_list: List = []
        self.current_round_team_b_list: List = []
        self.num_sims = 0

    @profile
    def get_probabilities_dict(self):
        # by using permutations we are technically 2x the computational work here
        # but this makes the code much simpler
        # we use a dataframe for easy mapping and vectorization of scipy.stats.norm

        team_combos = permutations(self.ratings.keys(), 2)
        df = pd.DataFrame(list(team_combos), columns=["a", "b"])
        df["a_rtg"] = df["a"].map(self.ratings)
        df["b_rtg"] = df["b"].map(self.ratings)
        df["rtg_diff"] = df["a_rtg"] - df["b_rtg"]
        df["p_win_a"] = scipy.stats.norm(0, self.exp_stdev).cdf(
            df["a_rtg"] - df["b_rtg"]
        )
        df["p_win_b"] = 1 - df["p_win_a"]
        df.set_index(["a", "b"], inplace=True)
        self.probabilities_dict = dict(zip(df.index.values, df["p_win_a"].values))
        #print(self.probabilities_dict)

    @profile
    def run_simulations(self, num_sims=100):
        self.num_sims = num_sims
        self.simulation_results = []
        for sim in range(self.num_sims):
            self.sim_id = sim
            self.current_round = 1
            self.store_initial_round()
            while self.current_round <= self.n_rounds:
                self.run_round()
        self.sim_results_to_df_and_store()

    @profile
    def store_initial_round(self):
        self.store_simulation_results(initial_round=True)

    @profile
    def check_play_in(self):
        self.current_round_is_play_in = self.current_round == 1 and self.play_in

    @profile
    def set_current_matchups(self):
        if self.current_round == 1:
            if self.play_in:
                self.current_matchups = self.play_in_matchups
            else:
                self.current_matchups = self.teams
        else:
            self.current_matchups = self.remaining_teams

        self.current_round_team_a_list = self.current_matchups[::2]
        self.current_round_team_b_list = self.current_matchups[1::2]
        self.combined_current_matchups = zip(
            self.current_round_team_a_list, self.current_round_team_b_list
        )

    @profile
    def generate_simulation_seed(self):
        self.simulation_values = np.random.uniform(
            size=int(len(self.current_matchups) / 2)
        )

    @profile
    def get_team_a_probs(self):
        self.team_a_probs = [self.probabilities_dict[(a,b)] for a,b in self.combined_current_matchups]

    @staticmethod
    @profile
    def simulate_game(team_a, team_b, team_a_prob, rand_val):
        # why waste a function call on this?
        # this gives us flexibility to try different things in our simulation
        return team_a if rand_val <= team_a_prob else team_b

    @profile
    def get_winners(self):
        self.remaining_teams = [
            self.simulate_game(team_a, team_b, team_a_prob, rand_val)
            for team_a, team_b, team_a_prob, rand_val in zip(
                self.current_round_team_a_list,
                self.current_round_team_b_list,
                self.team_a_probs,
                self.simulation_values,
            )
        ]

    @profile
    def store_simulation_results(self, initial_round=False):
        teams_to_use = self.teams if initial_round else self.remaining_teams
        for team in teams_to_use:
            self.simulation_results.append(
                {"team": team, "round": self.current_round, "sim_id": self.sim_id}
            )

    @profile
    def increment_current_round(self):
        self.current_round += 1

    @profile
    def run_round(self):
        self.check_play_in()
        self.set_current_matchups()
        # self.update_teams()
        self.generate_simulation_seed()
        self.get_team_a_probs()
        self.get_winners()
        self.increment_current_round()
        self.store_simulation_results()

    @profile
    def sim_results_to_df_and_store(self):
        # store_object_as_json(self.simulation_results, "sim_results.json")
        full_results = pd.DataFrame(self.simulation_results)

        count_by_round = full_results.groupby(["team", "round"]).count().reset_index()
        count_by_round.columns = ["team", "round", "count"]
        count_by_round = count_by_round.pivot(
            index="team", columns="round", values="count"
        ).fillna(0)
        count_by_round = count_by_round / self.num_sims
        self.output_df = count_by_round.reset_index()
        self.output_df.to_csv("test_csv.csv", index=False)


@profile
def main():
    teams = ["".join(p) for p in permutations("abcdefghijklmnopqrstuvwxyz", 2)][:64]
    team_ratings = np.random.normal(0, 16.5, 64)
    region_a = Region("region_a", teams[:16])
    region_b = Region("region_b", teams[16:32])
    region_c = Region("region_c", teams[32:48])
    region_d = Region("region_d", teams[48:64])
    ratings = {team: rating for team, rating in zip(teams, team_ratings)}
    bracket = Bracket(ratings, region_a, region_b, region_c, region_d)
    bracket.run_simulations(num_sims=1000000)
    #prob = bracket.probabilities_dict[("ab", "bc")]
    #observed_prob = bracket.output_df.loc[bracket.output_df["team"] == "ab"][2][0]
    #print(prob, observed_prob)
    #assert math.isclose(prob, observed_prob, abs_tol=0.05)


if __name__ == "__main__":
    main()
