import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

today = "02_26_24"

def linear_regression(data_frame, target_variable, debug=False):
    # Define features and target variable
    X = data_frame[['Player', 'Opponent']]
    y = data_frame[target_variable]

    # Define preprocessing steps
    preprocessor = ColumnTransformer(
        transformers=[
            ('encoder', OneHotEncoder(handle_unknown='ignore'), ['Player', 'Opponent'])
        ],
        remainder='passthrough'
    )

    # Create a pipeline with preprocessing and linear regression model
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Fit the pipeline to the training data
    pipeline.fit(X_train, y_train)
    output = 'linear_' + today + '_' + target_variable +'.pkl'
    joblib.dump(pipeline, output)



file_path = '../data/output_file.csv'
# Read the CSV file into a pandas DataFrame
data = pd.read_csv(file_path)
# Convert the data dictionary to a DataFrame
df = pd.DataFrame(data)

linear_regression(df, 'PTS')
linear_regression(df, 'TRB')
linear_regression(df, 'AST')
linear_regression(df, '3P')

