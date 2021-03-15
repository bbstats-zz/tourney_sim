from src.brackets import Region, Bracket
from src.stats import get_ratings

west = [
    "Gonzaga",
    "Oklahoma",
    "Missouri",
    "Creighton",
    "UC-Santa Barbara",
    "Virginia",
    "Ohio",
    "USC",
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

east = [
    "Michigan",
    "Louisiana State",
    "St. Bonaventure",
    "Colorado",
    "Georgetown",
    "Florida State",
    "UNC Greensboro",
    "BYU",
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
south =
# south_playin =
# midwest =
# midwest_playin =


if __name__ == "__main__":
    ratings = get_ratings()
