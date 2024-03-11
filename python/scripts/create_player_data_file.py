import argparse
import csv
import pandas as pd
from python.data import players_by_team

csv_file = '../data/output_file.csv'


def avg_percentage_for_player(player_name, target):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Filter the DataFrame to include only rows corresponding to the specified player
    player_df = df[df['Player'] == player_name]

    # Select the last 5 entries
    last_5_entries = player_df.tail(5)

    # Calculate the average for the target variable over the last 5 entries
    avg_percentage_last_5_entries = last_5_entries[target].mean()

    return avg_percentage_last_5_entries


def main():
    # Create ArgumentParser object
    argparse.ArgumentParser(description="A question-answer program")

    # Parse arguments
    team_1 = input("First team do you want data for:")

    # Load data from file
    team_1_players = players_by_team.get_dict().get(team_1)
    if len(team_1_players) == 0:
        print("Invalid TEAM name")
        return

    # Parse arguments
    team_2 = input("Second team do you want data for:")

    # Load data from file
    team_2_players = players_by_team.get_dict().get(team_2)
    if len(team_2_players) == 0:
        print("Invalid TEAM name")
        return

    # Write the data to a CSV file
    with open("../data/predict_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        # Write headers
        writer.writerow(
            ["Team", "Opponent", "Player", "AVG_MP%", "AVG_FG", "AVG_FGA", "AVG_FG%", "AVG_3P%", "AVG_TRB", "AVG_AST", "PTS", "TRB", "AST", "3P"])
        # TODO get average %
        for player in team_1_players:
            writer.writerow(
                [
                    team_1,
                    team_2,
                    player,
                    avg_percentage_for_player(player, "MP"),
                    avg_percentage_for_player(player, "FG"),
                    avg_percentage_for_player(player, "FGA"),
                    avg_percentage_for_player(player, "FG%"),
                    avg_percentage_for_player(player, "3P%"),
                    avg_percentage_for_player(player, "TRB"),
                    avg_percentage_for_player(player, "AST")
                ],
            )
        for player in team_2_players:
            writer.writerow(
                [
                    team_2,
                    team_1,
                    player,
                    avg_percentage_for_player(player, "MP"),
                    avg_percentage_for_player(player, "FG"),
                    avg_percentage_for_player(player, "FGA"),
                    avg_percentage_for_player(player, "FG%"),
                    avg_percentage_for_player(player, "3P%"),
                    avg_percentage_for_player(player, "TRB"),
                    avg_percentage_for_player(player, "AST")
                ],
            )


if __name__ == "__main__":
    main()
