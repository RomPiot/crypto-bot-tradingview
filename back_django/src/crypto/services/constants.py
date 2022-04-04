# # TODO : timeframe in db
TIMEFRAME = {
    "1m": {"db_name": "minute", "ms": 60000},
    "5m": {"db_name": "five_minutes", "ms": 300000},
    "15m": {"db_name": "fiveteen_minutes", "ms": 900000},
    "1h": {"db_name": "hour", "ms": 3600000},
    "4h": {"db_name": "four_hours", "ms": 14400000},
    "12h": {"db_name": "twelve_hours", "ms": 43200000},
    "1d": {"db_name": "day", "ms": 86400000},
    "1w": {"db_name": "week", "ms": 604800000},
}

# from datetime import datetime, timedelta
# from pprint import pprint
# from django.utils import timezone

# since = datetime(2012, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)
# now = datetime.now(tz=timezone.utc)

# print(since)
# print(now)

# datetime_array = []

# while since < now:
#     ms = 1000 * 900000
#     since = since + timedelta(milliseconds=ms)
#     if since < now:
#         datetime_array.append(since)

# pprint(datetime_array)
