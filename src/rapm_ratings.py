from src.constants import INJURIES
import pandas as pd
from src.stats import get_lehigh_method


class AdjustedLehighRatings:
    def __init__(self):
        self.get_name_remapper()
        self.get_rapm_data()
        self.get_team_ratings()
        self.force_fit_player_ratings()
        self.remove_injured_players()

    def get_rapm_data(self):
        df = pd.read_csv("src/player_data.csv")
        df["Team"] = df["Team"].map(self.name_remap)
        df = df.set_index(["Team", "Player"])
        self.player_ratings = df.loc[df["Season"] == "2020-21"]

    def get_name_mapper(self):
        df = pd.read_csv("src/srapm.csv")[["Team", "School"]].drop_duplicates()
        self.name_remap = dict(zip(df["Team"], df["School"]))

    def get_team_ratings(self):
        self.team_ratings = get_lehigh_method()[["School", "TLM_NetRtg"]]

    def add_minutes_pct_column(self, team_suffix, min_pct_name):
        self.team_minutes = (
            self.player_ratings.groupby("Team")["MINS"].sum().reset_index(drop=False)
        )
        self.player_ratings = self.player_ratings.merge(
            self.team_minutes, on="Team", suffixes=("", team_suffix)
        )
        self.player_ratings[min_pct_name] = (
            self.player_ratings["MINS"] / self.player_ratings["MINS" + team_suffix] * 5
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
            self.player_ratings["TLM_NetRtg_team"] - self.player_ratings["Contrib_team"]
        ) / 5
        self.player_ratings["adj_RAPM"] = (
            self.player_ratings["RAPM"] + self.player_ratings["team_adjustment"]
        )

    def remove_injured_players(self, injuries=INJURIES):
        for team, players in injuries.items():
            for player in players:
                self.player_ratings.drop((team, player), inplace=True)

    def keep_only_top_n(self, n=8):
        self.player_ratings = self.player_ratings.sort_values(
            ["Team", "MINS"], ascending=False
        )
        self.player_ratings = self.player_ratings.groupby("Team").head(n).reset_index()

        self.add_minutes_pct_column(suffix="_adj", min_pct_name="min_pct_adj")
        self.player_ratings["min_pct_adj"]=self.player_ratings["min_pct_adj"].clip(upper=1)
        self.redistribute_minutes(minutes_col="min_pct_adj")

        while self.max_min_pct >= 1:
            self.max_

    def redistribute_minutes(self, minutes_col):
        



def main():
    teamratings = AdjustedLehighRatings()
    teamratings.player_ratings.to_csv("src/adjusted_lehigh_ratings.csv")


if __name__ == "__main__":
    main()
