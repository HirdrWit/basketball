import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
import joblib

today = "03_04_24"
file_path = '../data/output_file.csv'

def random_forest_regression(data_frame, target_variable, debug=False):
    # Define features and target variable
    X = data_frame[['Opponent', 'MP', 'FG', 'FGA', 'FG%', '3P%', 'TRB', 'AST']]
    y = data_frame[target_variable]

    # Define preprocessing steps
    preprocessor = ColumnTransformer(
        transformers=[
            ('encoder', OneHotEncoder(handle_unknown='ignore'), ['Opponent', 'MP', 'FG', 'FGA', 'FG%', '3P%', 'TRB', 'AST'])
        ],
        remainder='passthrough'
    )

    # Create a pipeline with preprocessing and Random Forest regression model
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor())
    ])

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Fit the pipeline to the training data
    pipeline.fit(X_train, y_train)
    # Predict on the testing data
    y_pred = pipeline.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print('Random Forest Regression Mean Squared Error:', mse)
    output = 'random_forest_' + today + '_' + target_variable + '.pkl'
    joblib.dump(pipeline, output)

# Read the CSV file into a pandas DataFrame
data = pd.read_csv(file_path)
# Convert the data dictionary to a DataFrame
df = pd.DataFrame(data)

random_forest_regression(df, 'PTS')
random_forest_regression(df, 'TRB')
random_forest_regression(df, 'AST')
random_forest_regression(df, '3P')
