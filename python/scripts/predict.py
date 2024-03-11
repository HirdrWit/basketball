import csv
import string

from python.data import team_standings
import joblib
import pandas as pd


def predict(prediction):
    # Prediction example
    # Prepare input data for prediction
    # point_pipeline = joblib.load('../models/linear_03_02_24_PTS.pkl')
    # total_rebound_pipeline = joblib.load('../models/linear_03_02_24_TRB.pkl')
    # assist_pipeline = joblib.load('../models/linear_03_02_24_AST.pkl')
    # three_point_pipeline = joblib.load('../models/linear_03_02_24_3P.pkl')
    point_pipeline = joblib.load('../models/linear_03_02_24_PTS.pkl')
    total_rebound_pipeline = joblib.load('../models/linear_03_02_24_TRB.pkl')
    assist_pipeline = joblib.load('../models/linear_03_02_24_AST.pkl')
    three_point_pipeline = joblib.load('../models/linear_03_02_24_3P.pkl')

    for player, values in prediction.items():
        data_list = []
        opp = float(team_standings.get_dict().get(values[0]))
        avg_mp = values[1]
        avg_fg = values[2]
        avg_fg_attempted = values[3]
        avg_fg_percentage = values[4]
        avg_3p = values[5]
        avg_rebounds = values[6]
        avg_assists = values[7]
        proj_pts = values[8]
        proj_trb = values[9]
        proj_ast = values[10]
        proj_3p = values[11]

        # Append data for each player to the data list
        data_list.append([
            opp,
            avg_mp,
            avg_fg,
            avg_fg_attempted,
            avg_fg_percentage,
            avg_3p,
            avg_rebounds,
            avg_assists])

        # Convert the data list to a DataFrame
        new_data = pd.DataFrame(data_list, columns=['Opponent', 'MP', 'FG', 'FGA', 'FG%', '3P%', 'TRB', 'AST'])

        # Make predictions for all players at once
        projected_points = point_pipeline.predict(new_data)
        projected_rebounds = total_rebound_pipeline.predict(new_data)
        projected_assists = assist_pipeline.predict(new_data)
        projected_3p = three_point_pipeline.predict(new_data)

        print(f"{player}\n\tPredicted PTS: {projected_points} Difference: {projected_points - proj_pts}")
        print(f"\tPredicted REB: {projected_rebounds} Difference: {projected_rebounds - proj_trb}")
        print(f"\tPredicted AST: {projected_assists} Difference: {projected_assists - proj_ast}")
        print(f"\tPredicted 3P:  {projected_3p} Difference: {projected_3p - proj_3p}")


def main():
    data = {}
    with open("../data/predict_data.csv", 'r', newline='') as csvfile:
        # Create a CSV reader object
        csv_reader = csv.reader(csvfile)

        # Iterate over each row in the CSV file
        for index, row in enumerate(csv_reader):
            if index == 0:
                continue
            player = row[2]
            opponent = row[1]
            avg_mp = float(row[3])
            avg_fg = float(row[4])
            avg_fg_attempted = float(row[5])
            avg_fg_percentage = float(row[6])
            avg_3p = float(row[7])
            avg_rebounds = float(row[8])
            avg_assists = float(row[9])
            proj_pts = float(row[10])
            proj_trb = float(row[11])
            proj_ast = float(row[12])
            proj_3p = float(row[13])
            data[player] = [opponent,
                            avg_mp,
                            avg_fg,
                            avg_fg_attempted,
                            avg_fg_percentage,
                            avg_3p,
                            avg_rebounds,
                            avg_assists,
                            proj_pts,
                            proj_trb,
                            proj_ast,
                            proj_3p]
    predict(data)


if __name__ == "__main__":
    main()
