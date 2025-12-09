from datetime import datetime as dt

def convert_ts_to_right_format(ts):
    try:
        return dt.strptime(ts, '%Y-%m-%d %H:%M:%S').date()
    except:
        ts = ts[:-6]
        return dt.strptime(ts, '%Y-%m-%d %H:%M:%S').date()