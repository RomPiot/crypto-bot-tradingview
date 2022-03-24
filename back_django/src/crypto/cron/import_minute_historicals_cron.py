from django.http import JsonResponse
from crypto.models import Symbol
from crypto.services.import_currency import import_candles
from datetime import datetime
from django.utils import timezone

# 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w
TIMEFRAME = {
    "1m": "minute",
    "5m": "five_minutes",
    "15m": "fiveteen_minutes",
    "1h": "hour",
    "4h": "four_hours",
    "12h": "twelve_hours",
    "1d": "day",
    "1w": "week",
}

symbols = Symbol.objects.all()
# timeframe = "1m"

TIMEFRAME_LOOP = {
    "1h": "hour",
    "4h": "four_hours",
    "12h": "twelve_hours",
    "1d": "day",
    "1w": "week",
}

for timeframe in TIMEFRAME_LOOP:
    for symbolObj in symbols:
        last_imported_timeframe_attr = f"last_imported_{TIMEFRAME[timeframe]}"
        last_imported = getattr(symbolObj, last_imported_timeframe_attr)

        if last_imported:
            date_start = last_imported
        else:
            date_start = datetime(2012, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)

        symbol = f"{symbolObj.from_currency.slug}/{symbolObj.to_currency.slug}"

        print(symbol)
        print(timeframe)

        import_candles(symbol=symbol, since=date_start, exchange_id=symbolObj.from_exchange.slug, timeframe=timeframe)

JsonResponse({"results": True})
