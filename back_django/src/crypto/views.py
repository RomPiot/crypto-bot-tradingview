from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
from crypto.services.import_curr import import_currencies
from crypto.models import Currency, Exchange, Historical, Symbol
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

    timeframe = "15m"
    from_currency = Currency.objects.get(slug="ETH")
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


async def import_historical_request(request):
    exchange = Exchange.objects.get(slug="binance")
    # timeframes = ["1h", "4h", "12h", "1d", "1w"]
    timeframes = ["1h"]

    pair_symbol = Symbol.objects.get(name="BTC/USDT")
    # pair_symbol.last_imported_hour = None
    # pair_symbol.save()

    # Historical.objects.filter(symbol=pair_symbol).delete()

    await import_currencies(exchange=exchange, timeframes=timeframes, pair_symbols=[pair_symbol])

    return JsonResponse({"results": True})
