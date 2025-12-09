def convert_date_to_right_format(datestr):
    from datetime import datetime as dt
    try:
        return dt.strftime(datestr, '%Y-%m-%d').date()
    except:
        return None