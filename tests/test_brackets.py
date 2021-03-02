from brackets import Region


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
        "Dogs": 16,
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
