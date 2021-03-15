from typing import Dict

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
