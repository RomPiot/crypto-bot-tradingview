from django.http import JsonResponse
from crypto.models import Symbol
from crypto.services.import_currency import import_candles
from datetime import datetime
from django.utils import timezone


date_start = datetime(2012, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)

# TODO : for each symbol
# import historical in 1m

symbols = Symbol.objects.all()

for symfolObj in symbols:
    if symfolObj.last_imported_minute:
        date_start = symfolObj.last_imported_minute
    else:
        date_start = datetime(2012, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)

    symbol = f"{symfolObj.currency}/{symfolObj.currency}"

    import_candles(symbol=symbol, since=date_start, exchange_id=symfolObj.from_exchange, timeframe="1m")

JsonResponse({"results": True})
