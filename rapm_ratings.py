from src.constants import INJURIES
import pandas as pd
from src.stats import get_lehigh_method
import numpy as np
import math


# this code sucks massively
# someone make it better please


class AdjustedLehighRatings:
    def __init__(self):
        self.get_name_remapper()
        self.get_rapm_data()
        self.get_team_ratings()
        self.force_fit_player_ratings()
        self.remove_injured_players()
        self.keep_only_top_n()
        self.force_fit_team_minutes()
        self.get_team_final_ratings()

    def get_rapm_data(self):
        df = pd.read_csv("src/player_data.csv")
        df["Team"] = df["Team"].map(self.name_remap)
        self.player_ratings = df.loc[df["Season"] == "2020-21"]

    def get_name_remapper(self):
        df = pd.read_csv("src/srapm.csv")[["Team", "School"]].drop_duplicates()
        self.name_remap = dict(zip(df["Team"], df["School"]))


    def get_team_ratings(self):
        self.team_ratings = get_lehigh_method()[["School", "TLM_NetRtg"]]

    def add_minutes_pct_column(self, team_suffix, min_pct_name, mins_column="MINS"):
        self.team_minutes = (
            self.player_ratings.groupby("Team")[mins_column]
            .sum()
            .reset_index(drop=False)
        )
        if mins_column + team_suffix in self.player_ratings.columns:
            self.player_ratings.drop(columns=[mins_column+team_suffix],inplace=True)
        self.player_ratings = self.player_ratings.merge(
            self.team_minutes, on="Team", suffixes=("", team_suffix)
        )
        self.player_ratings[min_pct_name] = (
            self.player_ratings[mins_column]
            / self.player_ratings[mins_column + team_suffix]
            * 5
        )

    def force_fit_player_ratings(self):
        self.add_minutes_pct_column(team_suffix="_team", min_pct_name="min_pct")
        self.player_ratings["Contrib"] = (
            self.player_ratings["RAPM"] * self.player_ratings["min_pct"]
        )

        self.team_contrib = (
            self.player_ratings.groupby("Team")["Contrib"].sum().reset_index(drop=False)
        )
        self.player_ratings = self.player_ratings.merge(
            self.team_contrib, on="Team", suffixes=("", "_team")
        )

        self.player_ratings = self.player_ratings.merge(
            self.team_ratings, left_on="Team", right_on="School", suffixes=("", "_team")
        )
        self.player_ratings["team_adjustment"] = (
            self.player_ratings["TLM_NetRtg"] - self.player_ratings["Contrib_team"]
        ) / 5
        self.player_ratings["adj_RAPM"] = (
            self.player_ratings["RAPM"] + self.player_ratings["team_adjustment"]
        )

    def remove_injured_players(self, injuries=INJURIES):
        self.player_ratings = self.player_ratings.set_index(["Team", "cleanName"])
        for team, players in injuries.items():
            for player in players:
                self.player_ratings.drop((team, player), inplace=True)

    def adjust_and_clip_minutes(self, mins_column="MINS"):
        self.add_minutes_pct_column(team_suffix="_adj", min_pct_name="min_pct_adj", mins_column=mins_column)
        self.player_ratings["min_pct_adj"] = self.player_ratings["min_pct_adj"].clip(
            upper=1
        )
        grpd = self.player_ratings.groupby("Team")["min_pct_adj"].sum()
        self.max_team_minutes = grpd.max()
        self.min_team_minutes = grpd.min()

    def check_minutes_complete(self):
        self.minutes_complete = math.isclose(self.max_team_minutes, 5.0, abs_tol=0.001) and math.isclose(self.min_team_minutes,5.0, abs_tol=0.001)

    def keep_only_top_n(self, n=8):
        self.player_ratings = self.player_ratings.sort_values(
            ["Team", "MINS"], ascending=False
        )
        self.player_ratings = self.player_ratings.groupby("Team").head(n).reset_index()
        self.adjust_and_clip_minutes()
        self.check_minutes_complete()

    def force_fit_team_minutes(self):
        while not self.minutes_complete:
            print(f"adjusting and clipping {self.min_team_minutes} - {self.max_team_minutes}")
            self.adjust_and_clip_minutes(mins_column="min_pct_adj")
            self.check_minutes_complete()

    def get_team_final_ratings(self):
        self.player_ratings["final_Contrib"]=self.player_ratings["RAPM"]*self.player_ratings["min_pct_adj"]
        self.adjusted_team_ratings = self.player_ratings.groupby("Team")["RAPM"].sum().reset_index()
            


def main():
    teamratings = AdjustedLehighRatings()
    teamratings.adjusted_team_ratings.to_csv("src/adjusted_lehigh_ratings.csv")
    teamratings.player_ratings.to_csv("src/adjusted_lehigh_player_ratings.csv")


if __name__ == "__main__":
    main()
