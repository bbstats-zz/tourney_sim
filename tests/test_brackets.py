from brackets import Region, Bracket
import numpy as np
from itertools import permutations
import math

def test_single_playin():
    teams = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]
    play_in_dict = {15: ("North Carolina", "West Virginia")}
    region = Region("E", teams, play_in_dict)
    expected_team_seeds = {
        "A": 1,
        "B": 16,
        "C": 8,
        "D": 9,
        "E": 5,
        "F": 12,
        "G": 4,
        "H": 13,
        "I": 6,
        "J": 11,
        "K": 3,
        "L": 14,
        "M": 7,
        "N": 10,
        "O": 2,
        "North Carolina": 15,
        "West Virginia": 15,
    }
    assert region.team_seeds == expected_team_seeds


def test_multiple_playins():
    teams = ["A", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]

    play_in_dict = {15: ("North Carolina", "West Virginia"), 16: ("Dogs", "Frogs")}
    region = Region("E", teams, play_in_dict)

    expected_team_seeds = {
        "A": 1,
        "Dogs": 16,""
        "Frogs": 16,
        "C": 8,
        "D": 9,
        "E": 5,
        "F": 12,
        "G": 4,
        "H": 13,
        "I": 6,
        "J": 11,
        "K": 3,
        "L": 14,
        "M": 7,
        "N": 10,
        "O": 2,
        "North Carolina": 15,
        "West Virginia": 15,
    }
    assert region.team_seeds == expected_team_seeds


def test_create_bracket_no_playin():
    teams = [''.join(p) for p in permutations('abcdefghijklmnopqrstuvwxyz',2)][:64]
    team_ratings = np.random.normal(0, 16.5, 64)
    region_a = Region("region_a", teams[:16])
    region_b = Region("region_b", teams[16:32])
    region_c = Region("region_c", teams[32:48])
    region_d = Region("region_d", teams[48:64])
    ratings = {team: rating for team, rating in zip(teams, team_ratings)}
    bracket = Bracket(ratings, region_a, region_b, region_c, region_d)
    bracket.run_simulations(num_sims=10000)
    prob = bracket.probabilities_df.loc[["ab","bc"]]["p_win_a"][0]
    observed_prob = bracket.output_df.loc[bracket.output_df["team"]=="ab"][2][0]
    assert math.isclose(prob,observed_prob, abs_tol=0.05)

#test that probabilities match