import argparse
import csv

import joblib
import pandas as pd

from python.data import players_by_team


def get_players_user_cares_about(players):
    players_user_cares_about = []
    for player in players:
        user_input = input("Collect metrics for {}:".format(player))
        if user_input == "y":
            players_user_cares_about.append(player)
    return players_user_cares_about

def main():
    # Create ArgumentParser object
    argparse.ArgumentParser(description="A question-answer program")

    # Parse arguments
    team_1 = input("First team do you want data for:")

    # Load data from file
    players_1 = players_by_team.get_dict().get(team_1)
    if len(players_1) == 0:
        print("Invalid TEAM name")
        return

    # Parse arguments
    team_2 = input("Second team do you want data for:")

    # Load data from file
    players_2 = players_by_team.get_dict().get(team_2)
    if len(players_2) == 0:
        print("Invalid TEAM name")
        return

    # Write the data to a CSV file
    with open("../data/predict_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        # Write headers
        writer.writerow(
            ["Team", "Opponent", "Player", "PTS", "TRB", "AST", "3P"])
        for player in players_1:
            writer.writerow(
                [team_1, team_2, player])
        for player in players_2:
            writer.writerow(
                [team_2, team_1, player])


if __name__ == "__main__":
    main()
