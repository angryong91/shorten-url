from datetime import datetime, timedelta, UTC


def utc_to_kst(utc_datetime):
    return utc_datetime + timedelta(hours=9)


def kst_today():
    return utc_to_kst(datetime.now(UTC)).replace(hour=0, minute=0, second=0, microsecond=0)


def datetime_range(end_time=datetime.now(UTC), days=7):
    return sorted([(end_time + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=d)
                   for d in range(0, days + 1)])
