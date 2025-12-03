from datetime import datetime, timedelta

def last_7_days():
    end = datetime.now()
    start = end - timedelta(days=7)
    return start, end 

def last_30_days():
    end = datetime.now()
    start = end - timedelta(days=30)
    return start, end