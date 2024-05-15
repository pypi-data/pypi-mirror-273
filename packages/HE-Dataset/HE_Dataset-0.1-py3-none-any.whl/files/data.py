import pandas as pd
import os

def get_data():
    data_path = os.path.join(os.path.dirname(__file__), '../data/cmp1.csv')
    return pd.read_csv(data_path)
