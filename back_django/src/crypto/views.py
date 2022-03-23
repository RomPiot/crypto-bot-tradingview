from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
from crypto.models import Historical, Symbol
from crypto.services.import_currency import import_candles
from datetime import datetime
from django.utils import timezone


def page_home(request):
    date_start = datetime(2012, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)
    # Historical.objects.all().delete()
    Historical.objects.filter(timeframe="1d").delete()

    context = {
        "symbol": "btc/usdt",
        "timeframe": "1m",
        "since": date_start,
    }

    return render(request, "page/home.html", context)


def get_candles(request):
    date_start = datetime(2017, 12, 25, 0, 0, 0, 0, tzinfo=timezone.utc)

    historicals = Historical.objects.filter(datetime__gte=date_start).order_by("datetime")
    historicals = serializers.serialize("json", historicals)

    return JsonResponse(historicals, safe=False)


def import_candles_request(request):
    # date_start = datetime(2012, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)

    # results = import_candles(symbol="btc/usdt", since=date_start)

    # return JsonResponse({"results": results})

    symbols = Symbol.objects.all()

    for symfolObj in symbols:
        if symfolObj.last_imported_minute:
            date_start = symfolObj.last_imported_minute
        else:
            date_start = datetime(2012, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)

        symbol = f"{symfolObj.currency.slug}/{symfolObj.to_currency.slug}"

        print(symbol)
        print(symfolObj.from_exchange.slug)

        import_candles(symbol=symbol, since=date_start, exchange_id=symfolObj.from_exchange.slug, timeframe="1d")

        return JsonResponse({"results": True})
