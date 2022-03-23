import ccxt
from datetime import datetime, timedelta
import os
import pandas as pd
from crypto.models import Currency, Exchange, Historical, Symbol
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


def import_candles(
    symbol,
    since: datetime = datetime(2012, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc),
    limit=1000000,
    exchange_id="binance",
    max_retries=9999999999,
    timeframe="1m",
):
    symbol = symbol.upper()

    exchange_class = getattr(ccxt, exchange_id)
    exchange = exchange_class(
        {"apiKey": os.environ.get("BINANCE_API_KEY"), "secret": os.environ.get("BINANCE_API_SECRET")}
    )

    return fetch_all_candles(exchange, max_retries, symbol, timeframe, since, limit)


def fetch_all_candles(exchange, max_retries, symbol, timeframe, since, limit):
    retry_nb = 0
    candles = []

    exchangeObj = Exchange.objects.get(name=exchange)
    symbolPair = symbol.split("/")
    currencyObj = Currency.objects.get(slug=symbolPair[0])
    toCurrencyObj = Currency.objects.get(slug=symbolPair[1])

    symbolObj, created = Symbol.objects.get_or_create(
        from_exchange=exchangeObj,
        from_currency=currencyObj,
        to_currency=toCurrencyObj,
    )

    last_imported_timeframe_attr = f"last_imported_{TIMEFRAME[timeframe]}"
    last_imported = getattr(symbolObj, last_imported_timeframe_attr)

    if last_imported:
        if since < last_imported:
            since = last_imported

    while True:
        if retry_nb >= max_retries:
            break

        print(since)

        ohlcv = retry_fetch_ohlcv(exchange, symbol, timeframe, since, limit)

        if not ohlcv:
            break

        candles = candles + ohlcv
        since = save_candles(exchangeObj, symbolObj, timeframe, candles)
        candles = []
        retry_nb += 1

    return "All imported"


def retry_fetch_ohlcv(exchange, symbol, timeframe, since, limit):
    since_unixtimestamp = int(since.timestamp() * 1000)
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since_unixtimestamp, limit)
    return ohlcv


def save_candles(exchangeObj, symbolObj, timeframe, candles):
    candles = pd.DataFrame(
        data=candles,
        columns=["datetime", "open", "high", "low", "close", "volume"],
    )
    candles["datetime"] = candles["datetime"].apply(lambda x: datetime.fromtimestamp(int(x) / 1000, tz=timezone.utc))

    historical_list = []

    for _, candle in candles.iterrows():
        historical = Historical(
            from_exchange=exchangeObj,
            symbol=symbolObj,
            timeframe=timeframe,
            datetime=candle["datetime"],
            open=candle["open"],
            close=candle["close"],
            high=candle["high"],
            low=candle["low"],
            volume=candle["volume"],
        )

        historical_list.append(historical)

    # update all historical
    Historical.objects.bulk_create(historical_list, ignore_conflicts=True)

    # update Symbol last imported datetime from timeframe type
    last_imported_timeframe_attr = f"last_imported_{TIMEFRAME[timeframe]}"
    last_imported = candles.iloc[-1]["datetime"]
    setattr(symbolObj, last_imported_timeframe_attr, last_imported)
    symbolObj.save()

    next_datetime = getattr(symbolObj, last_imported_timeframe_attr) + timedelta(seconds=1)
    return next_datetime
