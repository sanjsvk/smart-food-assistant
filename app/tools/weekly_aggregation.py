from datetime import timedelta

def get_last_7_days(datestr):
    return [datestr - timedelta(days=i) for i in range(7)]