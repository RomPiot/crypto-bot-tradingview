from django.http import JsonResponse
from django.shortcuts import render
from crypto.services.import_currency import import_candles
from datetime import datetime as dt


def page_home(request):
    date_start = dt(2012, 1, 1, 0, 0, 0, 0)

    context = {
        "symbol": "btc/usdt",
        "timeframe": "1m",
        "since": date_start,
    }

    return render(request, "page/home.html", context)


def get_candles():
    return JsonResponse({"done": True})


def import_candles_request(request):
    date_start = dt(2012, 1, 1, 0, 0, 0, 0)

    import_candles(symbol="btc/usdt", since=date_start)

    return JsonResponse({"done": True})
