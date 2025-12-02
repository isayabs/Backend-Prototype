import pandas as pd

DATA_PATH = "data/"

def load_csv(file_name):
    return pd.read_csv(DATA_PATH + file_name)