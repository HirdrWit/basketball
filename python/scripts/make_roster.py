import csv

input_file_path = '../../basic_box_score_stats.csv'
output_file_path = '../data/players_by_team.py'

# This script takes all the raw basic box score stats and creates a python dictionary for the players who have
# played on a certain team this year. NOTE: It does not current have any way to validate if the player is still on the
# team.
def main():
    data = {}
    with open(input_file_path, 'r', newline='') as csvfile:
        # Create a CSV reader object
        csv_reader = csv.reader(csvfile)

        # Iterate over each row in the CSV file
        for row in csv_reader:
            team = row[0]
            player_name = row[2]

            if team not in data:
                data[team] = []

            players = data.get(team)
            if player_name not in players:
                players.append(player_name)
                data[team] = players

    # Write the dictionary to a Python file
    with open(output_file_path, 'w') as py_file:
        py_file.write('def get_dict(): \n')
        py_file.write('\t return ')
        py_file.write(repr(data))  # Write the representation of the dictionary as Python code

    print("Dictionary written to", output_file_path)


if __name__ == "__main__":
    main()
