from datetime import datetime, timedelta, UTC


def utc_to_kst(utc_datetime):
    return utc_datetime + timedelta(hours=9)


def kst_today():
    return utc_to_kst(datetime.now(UTC)).replace(hour=0, minute=0, second=0, microsecond=0)


def datetime_range(end_time=datetime.now(UTC)):
    start_time = end_time - timedelta(minutes=1)

    return start_time, end_time
