from datetime import datetime, timedelta, UTC


def utc_to_kst(utc_datetime):
    return utc_datetime + timedelta(hours=9)


def kst_today():
    return utc_to_kst(datetime.now(UTC)).replace(hour=0, minute=0, second=0, microsecond=0)


def datetime_range():
    utc_now = datetime.now(UTC)
    # kst_now = utc_to_kst(utc_now)

    start_time = utc_now - timedelta(minutes=1)

    return start_time, utc_now
