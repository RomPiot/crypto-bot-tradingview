from asyncio import get_event_loop
import asyncio
import threading
from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
from crypto.services.import_curr import import_currencies
from crypto.services.constants import TIMEFRAME
from crypto.models import Currency, Exchange, Historical, Symbol
from crypto.services.import_currency import import_historical, import_multiple_currency, import_multiple_historical
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
    exchange = Exchange.objects.get(slug="binance")
    # timeframe = "1h"

    # timeframes = ["1h", "4h", "12h", "1d", "1w"]
    timeframes = ["15m"]
    # TODO : timeframe_array
    import_currencies(exchange=exchange, timeframes=timeframes)

    return JsonResponse({"results": True})
