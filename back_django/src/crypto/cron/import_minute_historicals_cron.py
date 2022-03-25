from django.http import JsonResponse
from back_django.src.crypto.services.constants import TIMEFRAME
from crypto.models import Symbol
from crypto.services.import_currency import import_historical
from datetime import datetime
from django.utils import timezone


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
        timeframe_db_name = TIMEFRAME[timeframe]["db_name"]
        last_imported_timeframe_attr = f"last_imported_{timeframe_db_name}"
        last_imported = getattr(symbolObj, last_imported_timeframe_attr)

        if last_imported:
            date_start = last_imported
        else:
            date_start = datetime(2012, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)

        symbol = f"{symbolObj.from_currency.slug}/{symbolObj.to_currency.slug}"

        print(symbol)
        print(timeframe)

        import_historical(
            symbol=symbol, since=date_start, exchange_id=symbolObj.from_exchange.slug, timeframe=timeframe
        )

JsonResponse({"results": True})
