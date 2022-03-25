from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
from back_django.src.crypto.services.constants import TIMEFRAME
from crypto.models import Currency, Exchange, Historical, Symbol
from crypto.services.import_currency import import_historical
from datetime import datetime
from django.utils import timezone


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


def import_historical_request(request):
    symbols = Symbol.objects.all()
    # timeframe = "1h"

    # TODO : get entries from TIMEFRAME
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

    return JsonResponse({"results": True})
