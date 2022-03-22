import ccxt
from datetime import datetime
import os
import pandas as pd
from crypto.models import Currency, Exchange, Historical, Symbol
from django.utils import timezone


# TODO function can be called from api or cron
def import_candles(
    symbol,
    since: datetime = datetime(2012, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc),
    limit=1000,
    exchange_id="binance",
    max_retries=9999999999,
    timeframe="1m",
):
    symbol = symbol.upper()
    since_datetime = int(since.timestamp() * 1000)

    exchange_class = getattr(ccxt, exchange_id)
    exchange = exchange_class({"apiKey": os.environ.get("BINANCE_API_KEY"), "secret": os.environ.get("BINANCE_API_SECRET")})

    return fetch_all_candles(exchange, max_retries, symbol, timeframe, since_datetime, limit)


def fetch_all_candles(exchange, max_retries, symbol, timeframe, since, limit):
    retry_nb = 0
    candles = []

    exchangeObj = Exchange.objects.get(name=exchange)
    symbolPair = symbol.split("/")
    currencyObj = Currency.objects.get(slug=symbolPair[0])
    toCurrencyObj = Currency.objects.get(slug=symbolPair[1])

    symbolObj, created = Symbol.objects.get_or_create(
        from_exchange=exchangeObj,
        currency=currencyObj,
        to_currency=toCurrencyObj,
    )

    if symbolObj.last_imported:
        last_imported_timesamp = int(symbolObj.last_imported.timestamp()) * 1000
        if since < last_imported_timesamp:
            since = last_imported_timesamp

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
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit)
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

    # update Symbol last insertion
    symbolObj.last_imported = candles.iloc[-1]["datetime"]
    symbolObj.save()

    last_imported_timestamp = int(symbolObj.last_imported.timestamp()) * 1000  # type: ignore
    return last_imported_timestamp
