from typing import Dict

# data via Jake Flancer: https://github.com/jflancer/march_madness/blob/master/short_model.R

INJURIES = {
    # For now opting to keep in all questionable players, closer to gametime consider changing (just uncomment)
    # "Josh Primo_Alabama", # Questionable
    # "RJ Cole_UConn", #Questionable
    # "J'Wan Roberts_Houston", #Questionable
    # "Jalen Wilson_Kansas", #Doubtful (COVID)
    # "Kyle Young_Ohio St.", #Questionable
    # "Ethan Morton_Purdue", #Questionable
    # "Isaiah Poor Bear-Chandler_Wichita St.", #Questionable
    # "Jaden Seymour_Wichita St.", #Questionable
    # "Trevin Wade_Wichita St.", #Questionable
    # "Shereef Mitchell_Creighton", #Questionable

    "Arkansas": ["Jaylin Williams", "Khalen Robinson"],
    "Drake": ["Roman Penn", "ShanQuan Hemphill"],
    "Florida": ["Keyontae Johnson"],
    "Georgetown": ["Jalen Harris"],
    "Houston": ["Caleb Mills"],
    "Iowa": ["Jack Nunge"],
    "Kansas": ["David McCormack", "Tristan Enaruna"],
    #"Louisiana Tech": ["Jace Bass"],
    "Michigan": ["Isaiah Livers"],
    "North Carolina": ["Puff Johnson"],
    "North Texas": ["Rubin Jones"],
    "Ohio State": ["Jimmy Sotos"],
    "Oklahoma State": [
        "Chris Harris Jr.",
        "Donovan Williams",
    ],
    "Oregon": ["N'Faly Dante"],
    "St. Bonaventure": ["Anthony Roberts"],
    "Syracuse": [
        "Bourama Sidibe",
        "Frank Anselem",
    ],
    "Tennessee": ["John Fulkerson"],
    "Texas Tech": [
        "Jamarius Burton",
        "Joel Ntambwe",
    ],
    "UCLA": [
        "Chris Smith",
        "Jalen Hill",
    ],
    "Virginia Commonwealth": ["Keshawn Curry"],
    "Villanova": ["Collin Gillespie"],
    "Virginia Tech": [
        "Jalen Cone",
        "Cartier Diarra",
    ],
}

ESPN_SCORES = [10, 20, 40, 80, 160, 320]

AVG_SEED_WINS = {
    1: 3.36,
    2: 2.43,
    3: 1.79,
    4: 1.52,
    5: 1.17,
    6: 1.26,
    7: 0.87,
    8: 0.67,
    9: 0.59,
    10: 0.63,
    11: 0.5,
    12: 0.48,
    13: 0.24,
    14: 0.18,
    15: 0.04,
    16: 0,
}

SEEDS = [1, 16, 8, 9, 5, 12, 4, 13, 6, 11, 3, 14, 7, 10, 2, 15]

YEAR = "2021"
URL = f"https://www.sports-reference.com/cbb/seasons/{YEAR}-ratings.html"

west_teams = [
    "Gonzaga",
    "Oklahoma",
    "Missouri",
    "Creighton",
    "UC-Santa Barbara",
    "Virginia",
    "Ohio",
    "Southern California",
    "Kansas",
    "Eastern Washington",
    "Oregon",
    "Virginia Commonwealth",
    "Iowa",
    "Grand Canyon",
]
west_playin = {
    16: ["Norfolk State", "Appalachian State"],
    11: ["Wichita State", "Drake"],
}

east_teams = [
    "Michigan",
    "Louisiana State",
    "St. Bonaventure",
    "Colorado",
    "Georgetown",
    "Florida State",
    "North Carolina-Greensboro",
    "Brigham Young",
    "Texas",
    "Abilene Christian",
    "Connecticut",
    "Maryland",
    "Alabama",
    "Iona",
]
east_playin = {
    16: ["Mount St. Mary's", "Texas Southern"],
    11: ["Michigan State", "UCLA"],
}
south_teams = [
    "Baylor",
    "Hartford",
    "North Carolina",
    "Wisconsin",
    "Villanova",
    "Winthrop",
    "Purdue",
    "North Texas",
    "Texas Tech",
    "Utah State",
    "Arkansas",
    "Colgate",
    "Florida",
    "Virginia Tech",
    "Ohio State",
    "Oral Roberts",
]
south_playin: Dict = {}
midwest_teams = [
    "Illinois",
    "Drexel",
    "Loyola (IL)",
    "Georgia Tech",
    "Tennessee",
    "Oregon State",
    "Oklahoma State",
    "Liberty",
    "San Diego State",
    "Syracuse",
    "West Virginia",
    "Morehead State",
    "Clemson",
    "Rutgers",
    "Houston",
    "Cleveland State",
]
midwest_playin: Dict = {}

TOURNEY_TEAMS = (
    east_teams
    + west_teams
    + south_teams
    + midwest_teams
    + west_playin[16]
    + west_playin[11]
    + east_playin[16]
    + east_playin[11]
)

bbr_to_jake = {
    "UNC": "North Carolina",
    "Manhattan College": "Manhattan",
    "St. John's": "St. John's (NY)",
    "Wichita State": "Wichita St.",
    "Florida State": "Florida St.",
    "South Florida": "South Fla.",
    "Samford University": "Samford",
    "Iowa State": "Iowa St.",
    "Ohio State": "Ohio St.",
    "Oklahoma State": "Oklahoma St.",
    "University of California, Irvine": "UC Irvine",
    "Purdue-Fort Wayne": "Purdue Fort Wayne",
    "Pitt": "Pittsburgh",
    "Harvard University": "Harvard",
    "San Diego State": "San Diego St.",
    "USC": "Southern California",
    "Michigan State": "Michigan St.",
    "Georgia State University": "Georgia St.",
    "Mississippi State": "Mississippi St.",
    "Oregon State": "Oregon St.",
    "Rutgers University": "Rutgers",
    "Arizona State": "Arizona St.",
    "Penn State": "Penn St.",
    "UMass": "Massachusetts",
    "Western Kentucky": "Western Ky.",
    "University of Northern Iowa": "UNI",
    "Howard University": "Howard",
    "Texas A&M-CC": "A&M-Corpus Christi",
    "Utah State": "Utah St.",
    "Youngstown State": "Youngstown St.",
    "Connecticut": "UConn",
    "Brigham Young": "BYU",
    "Southern Methodist": "SMU",
    "Northern Iowa": "UNI",
    "Stephen F. Austin": "SFA",
    "Appalachian State": "Appalachian St.",
    "Norfolk State": "Norfolk St.",
}

JAKE_TO_BBR = {v: k for k, v in bbr_to_jake.items()}
