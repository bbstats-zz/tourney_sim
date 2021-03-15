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
}

JAKE_TO_BBR= {v: k for k, v in bbr_to_jake.items()}
