import pickle
import os
from django.conf import settings
import pandas as pd

# Define the path to the trained prediction model
model_path = os.path.join(os.path.dirname(__file__), 'statistics', 'predict_win.pkl')
# Load the Random Forest model from the specified path
with open(model_path, 'rb') as file:
    rf_model = pickle.load(file)

# Define the path to the averages data file
def load_averages_data():
    # Load and return the data as a pandas DataFrame
    data_path = os.path.join(os.path.dirname(__file__), 'statistics', 'averages_df.csv')
    return pd.read_csv(data_path)