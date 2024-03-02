from sklearn.experimental import enable_hist_gradient_boosting  # noqa
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder
import pandas as pd

# Sample data (replace this with your actual data)
data = {
    'Player': ['Player1', 'Player2', 'Player3', 'Player4'],
    'Opponent': ['Opponent1', 'Opponent2', 'Opponent3', 'Opponent4'],
    'MP': [25, 30, 20, 28],
    'FG%': [0.45, 0.55, 0.42, 0.48],
    '3P%': [0.38, 0.40, 0.35, 0.36],
    'FT%': [0.82, 0.85, 0.78, 0.80],
    'PTS': [28, 32, 25, 30]  # Assuming PTS is the target variable
}

df = pd.DataFrame(data)

# Encoding categorical variables
label_encoders = {}
for column in ['Player', 'Opponent']:
    label_encoders[column] = LabelEncoder()
    df[column] = label_encoders[column].fit_transform(df[column])

# Separate features and target variable
X = df[['Player', 'Opponent', 'MP', 'FG%', '3P%', 'FT%']]
y = df['PTS']

# Training the model
model = HistGradientBoostingClassifier()
model.fit(X, y)

# After training, when you want to predict with nullable fields
# For example, predicting for a new player against a new opponent with missing features
new_data = {
    'Player': ['Player4'],
    'Opponent': ['Opponent4'],
    'MP': [None],  # Nullable fields
    'FG%': [None],  # Nullable fields
    '3P%': [None],  # Nullable fields
    'FT%': [None]  # Nullable fields
}

new_df = pd.DataFrame(new_data)

# Encoding categorical variables for prediction
for column in ['Player', 'Opponent']:
    new_df[column] = label_encoders[column].transform(new_df[column])

# Predicting with nullable fields
predicted_pts = model.predict(new_df[['Player', 'Opponent', 'MP', 'FG%', '3P%', 'FT%']])
print("Predicted PTS:", predicted_pts)
