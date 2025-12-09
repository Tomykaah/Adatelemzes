from datetime import datetime as dt

def convert_ts_to_right_format(ts):
    try:
        return dt.strptime(ts, '%Y-%m-%d %H:%M:%S').date()
    except:
        ts = ts[:-6]
        return dt.strptime(ts, '%Y-%m-%d %H:%M:%S').date()
    
def determine_season(gameDate: dt)-> str:
    year = gameDate.year
    if gameDate.month >= 10:
        return f"{year}-{year + 1}"
    else:
        return f"{year - 1}-{year}"