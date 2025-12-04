import pandas as pd

def group_by_date(df, timestamp_col):
    
    df = df.copy()
    df["_date"] = df[timestamp_col].dt.date
    
    grouped = {}
    for date_value, df_day in df.groupby("_date"):
        grouped[date_value] = df_day.drop(columns=["_date"])  # keep original columns only
    
    return grouped
