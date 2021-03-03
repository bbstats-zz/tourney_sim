from itertools import permutations
from typing import List
import pandas as pd
import scipy.stats
import numpy as np
import random


def flatten(lst: List) -> List:
    return [item for sublist in lst for item in sublist]


class Region:
    def __init__(self, region_name, bid_teams, play_in_dict={}):
        self.region_name = region_name
        self.bid_teams = bid_teams
        self.seeds = [1, 16, 8, 9, 5, 12, 4, 13, 6, 11, 3, 14, 7, 10, 2, 15]
        self.play_in_dict = play_in_dict
        self.play_in_seeds = list(self.play_in_dict.keys())
        self.play_in_teams = flatten(list(self.play_in_dict.values()))
        self.teams = self.bid_teams + self.play_in_teams
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


class Bracket:
    def __init__(self, ratings, *regions, exp_stdev=16.5):

        self.regions = regions
        self.ratings = ratings
        self.exp_stdev = exp_stdev

        self.teams = []
        for region in self.regions:
            self.teams += region.teams

        self.get_probabilities_df()

        self.play_in_matchups = flatten([region.play_in_teams for region in regions])
        self.play_in = len(self.play_in_matchups) > 0

        self.n_rounds = int(np.log2(len(self.teams))) + self.play_in
        print(f'rounds: {self.n_rounds}')

        self.current_round = None
        self.current_round_is_play_in = False
        self.current_round_team_a_list = []
        self.current_round_team_b_list = []
        

    def get_probabilities_df(self):
        # by using permutations we are technically 2x the computational work here
        # but this makes the code much simpler
        team_combos = permutations(self.ratings.keys(), 2)
        df = pd.DataFrame(list(team_combos), columns=["a", "b"])
        df["a_rtg"] = df["a"].map(self.ratings)
        df["b_rtg"] = df["b"].map(self.ratings)
        df["rtg_diff"] = df["a_rtg"] - df["b_rtg"]
        df["p_win_a"] = scipy.stats.norm(0, self.exp_stdev).cdf(
            df["a_rtg"] - df["b_rtg"]
        )
        df["p_win_b"] = 1 - df["p_win_a"]
        self.probabilities_df = df

    def run_simulations(self, num_sims=100):
        self.simulation_results = []
        for sim in range(num_sims):
            self.current_round = 1
            while self.current_round <= self.n_rounds:
                self.run_round()

    def check_play_in(self):
        self.current_round_is_play_in = self.current_round == 1 and self.play_in

    def set_current_matchups(self):
        if self.current_round == 1:
            if self.play_in:
                self.current_matchups = self.play_in_matchups
            else:
                self.current_matchups = self.teams
        else:
            self.current_matchups = self.remaining_teams



    def update_teams(self):
        self.current_round_team_a_list = self.current_matchups[::2]
        self.current_round_team_b_list = self.current_matchups[1::2]

    def increment_current_round(self):
        self.current_round += 1

    def generate_simulation_seed(self):
        self.simulation_values = np.random.uniform(
            size=int(len(self.current_matchups) / 2)
        )

    def get_team_a_probs(self):
        team_a_mask = self.probabilities_df['a'].isin(self.current_round_team_a_list)
        self.team_a_probs = self.probabilities_df.loc[team_a_mask]['p_win_a'].values

    @staticmethod
    def simulate_game(team_a, team_b, team_a_prob, rand_val):
        # why waste a function call on this?
        # this gives us flexibility to try different things in our simulation
        return team_a if rand_val <= team_a_prob else team_b

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

    def store_simulation_results(self):
        for remaining_team in self.remaining_teams:
            self.simulation_results.append({'team': remaining_team, 'round':self.current_round})

    def run_round(self):
        self.check_play_in()
        self.set_current_matchups()
        self.update_teams()
        self.generate_simulation_seed()
        self.get_team_a_probs()
        self.get_winners()
        self.store_simulation_results()
        self.increment_current_round()
