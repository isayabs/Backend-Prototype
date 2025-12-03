import pandas as pd

def parse_date(date_str: str, is_start: bool):
    if len(date_str) == 10:
        return pd.to_datetime(date_str + (" 00:00:00" if is_start else " 23:59:59"))
    
    return pd.to_datetime(date_str)