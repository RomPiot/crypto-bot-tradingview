from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
from crypto.models import Currency, Exchange, Historical, Symbol
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


def page_home(request):
    date_start = datetime(2019, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)
    # Historical.objects.all().delete()
    # Historical.objects.filter(timeframe="1d").delete()

    context = {
        "symbol": "btc/usdt",
        "timeframe": "1w",
        "since": date_start,
    }

    return render(request, "page/home.html", context)


def get_candles(request):
    date_start = datetime(2012, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)

    timeframe = "1h"
    from_currency = Currency.objects.get(slug="BTC")
    to_currency = Currency.objects.get(slug="USDT")
    exchange = Exchange.objects.get(slug="binance")
    symbol = Symbol.objects.get(from_exchange=exchange, from_currency=from_currency, to_currency=to_currency)

    historicals = Historical.objects.filter(
        from_exchange=exchange, symbol=symbol, timeframe=timeframe, datetime__gte=date_start
    ).order_by("datetime")

    print(timeframe)
    print(from_currency)
    print(to_currency)
    print(exchange)
    print(symbol)
    historicals = serializers.serialize("json", historicals)

    return JsonResponse(historicals, safe=False)


def import_candles_request(request):
    symbols = Symbol.objects.all()
    timeframe = "1h"

    for symbolObj in symbols:
        last_imported_timeframe_attr = f"last_imported_{TIMEFRAME[timeframe]}"
        last_imported = getattr(symbolObj, last_imported_timeframe_attr)

        if last_imported:
            date_start = last_imported
        else:
            date_start = datetime(2012, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)

        symbol = f"{symbolObj.from_currency.slug}/{symbolObj.to_currency.slug}"

        print(symbol)

        import_candles(symbol=symbol, since=date_start, exchange_id=symbolObj.from_exchange.slug, timeframe=timeframe)

    return JsonResponse({"results": True})
