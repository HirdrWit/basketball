import csv

import joblib
import pandas as pd


def predict(prediction):
    # Prediction example
    # Prepare input data for prediction
    point_pipeline = joblib.load('../models/linear_02_26_24_PTS.pkl')
    total_rebound_pipeline = joblib.load('../models/linear_02_26_24_TRB.pkl')
    assist_pipeline = joblib.load('../models/linear_02_26_24_AST.pkl')
    three_point_pipeline = joblib.load('../models/linear_02_26_24_3P.pkl')

    for player, values in prediction.items():
        opp = values[0]
        new_data = pd.DataFrame({
            'Player': [str(int.from_bytes(player.encode('utf-8'), byteorder='big'))],
            'Opponent': [str(int.from_bytes(opp.encode('utf-8'), byteorder='big'))]
        })
        # Make prediction
        print(player)
        projected_points = point_pipeline.predict(new_data)
        projected_rebounds = total_rebound_pipeline.predict(new_data)
        projected_assits = assist_pipeline.predict(new_data)
        projected_3p = three_point_pipeline.predict(new_data)
        print(
            '\tPredicted PTS: {:.2f} Difference: {:.2f}'.format(projected_points[0], (values[1] - projected_points[0])))
        print(
            '\tPredicted REB: {:.2f} Difference: {:.2f}'.format(projected_rebounds[0],
                                                                (values[2] - projected_rebounds[0])))
        print(
            '\tPredicted AST: {:.2f} Difference: {:.2f}'.format(projected_assits[0], (values[3] - projected_assits[0])))
        print('\tPredicted 3P:  {:.2f} Difference: {:.2f}'.format(projected_3p[0], (values[4] - projected_3p[0])))


def main():

    data = {}
    with open("../data/predict_data.csv", 'r', newline='') as csvfile:
        # Create a CSV reader object
        csv_reader = csv.reader(csvfile)

        # Iterate over each row in the CSV file
        for index, row in enumerate(csv_reader):
            if index == 0:
                continue
            data[row[2]] = [row[1], float(row[3]), float(row[4]), float(row[5]), float(row[6])]

    predict(data)


if __name__ == "__main__":
    main()
