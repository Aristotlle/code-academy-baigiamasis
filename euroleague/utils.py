import pickle
import os
from django.conf import settings
import pandas as pd

# For the model path
model_path = os.path.join(os.path.dirname(__file__), 'statistics', 'predict_win.pkl')

with open(model_path, 'rb') as file:
    rf_model = pickle.load(file)

def load_averages_data():
    # For the data path
    data_path = os.path.join(os.path.dirname(__file__), 'statistics', 'averages_df.csv')
    return pd.read_csv(data_path)