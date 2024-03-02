import pandas as pd
import shap as shap
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from sklearn.utils import check_array
import joblib

test_size = 0.1


def preprocess_minutes_played(mp):
    try:
        hours, minutes = map(int, mp.split(':'))
        return hours + minutes / 60
    except ValueError:
        return None  # Handle cases where 'MP' is not in the expected format


def histogram_classifier(data_frame, target_variable, test_size=0.2, debug=False):
    # Separate features and target variable
    X = data_frame[['Player', 'Opponent', 'MP', 'FG%', '3P%', 'FT%']]
    y = data_frame['PTS']

    # Training the model
    model = HistGradientBoostingClassifier()
    model.fit(X, y)

    return model


file_path = '../../output_file.csv'
data = pd.read_csv(file_path)
data['MP'] = data['MP'].apply(preprocess_minutes_played)
df = pd.DataFrame(data)
label_encoders = {}
for column in ['Player', 'Opponent']:
    label_encoders[column] = LabelEncoder()
    df[column] = label_encoders[column].fit_transform(df[column])

# Convert the data dictionary to a DataFrame

# Assuming you have a DataFrame named 'data' with relevant columns like 'Player', 'Opponent', 'FG', 'FGA', 'PTS', etc.
prediction = {
    # Opponent, Points, Rebounds, Assist, 3 Pointers
    'Shai Gilgeous-Alexander': ['HOU', 25.5, 0, 0, 0],
    'Chet Holmgren': ['HOU', 15.5, 8.5, 2.5, 1.5],
    ###
    'Cam Whitmore': ['BOS', 12.5, 3.5, 0.5, 1.5],
    'Dillon Brooks': ['BOS', 11.5, 3.5, 1.5, 1.5],
    'Alperen Şengün': ['BOS', 19.5, 9.5, 4.5, 0.5],
    'Jalen Green': ['BOS', 15.5, 3.5, 2.5, 1.5],
    'Fred Vanvleet': ['BOS', 15.5, 3.5, 6.5, 2.5],
    'Jabari Smith': ['BOS', 13.5, 8.5, 1.5, 1.5],
    'Amen Thompson': ['BOS', 11.5, 6.5, 3.5, 0.5],
    'Jeff Green': ['BOS', 4.5, 1.5, 0.5, 0.5],

}
try:
    pipe = joblib.load('pipeline.pkl')
except FileNotFoundError:
    pipe = histogram_classifier(df, 'PTS', debug=True)

for player, values in prediction.items():
    opp = values[0]
    new_data = pd.DataFrame({
        'Player': [player],
        'Opponent': [opp],
        'MP': [None],  # Nullable fields
        'FG%': [None],  # Nullable fields
        '3P%': [None],  # Nullable fields
        'FT%': [None]  # Nullable fields
    })
    new_df = pd.DataFrame(new_data)
    # Encoding categorical variables for prediction
    for column in ['Player', 'Opponent']:
        new_df[column] = label_encoders[column].transform(new_df[column])
    # Make prediction
    print(player)
    # Predicting with nullable fields
    predicted_pts = pipe.predict(new_df[['Player', 'Opponent', 'MP', 'FG%', '3P%', 'FT%']])
    print('\tPredicted PTS: {:.2f} Difference: {:.2f}'.format(predicted_pts[0], (values[1] - predicted_pts[0])))

# random_forest_regression(df, 'PTS', debug=True)
# neural_network_regression(df, 'PTS', debug=True)
