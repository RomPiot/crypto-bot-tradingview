import ccxt

from datetime import datetime as dt
import os
import pandas as pd

from crypto.models import Currency, Exchange, Historical, Symbol


def retry_fetch_ohlcv(exchange, symbol, timeframe, since, limit):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit)
    return ohlcv


def fetch_all_candles(exchange, max_retries, symbol, timeframe, since, limit):
    retry_nb = 0
    candles = []

    while True:
        ohlcv = retry_fetch_ohlcv(exchange, symbol, timeframe, since, limit)

        if not ohlcv:
            break

        candles = candles + ohlcv
        retry_nb += 1

        if retry_nb >= max_retries:
            save_candles(exchange, symbol, timeframe, candles)
            retry_nb = 0

    return True


def save_candles(exchange, symbol, timeframe, candles):
    candles = pd.DataFrame(
        data=candles,
        columns=["datetime", "open", "high", "low", "close", "volume"],
    )
    candles["datetime"] = candles["datetime"].apply(lambda x: dt.fromtimestamp(int(x) / 1000))
    # candles = candles.sort_values(by=["datetime"], ascending=[True])
    # candles = candles.set_index("datetime")

    exchangeObj = Exchange.objects.get(name=exchange)
    symbol = symbol.split("/")

    currencyObj = Currency.objects.get(slug=symbol[0])
    toCurrencyObj = Currency.objects.get(slug=symbol[1])

    # TODO move some object in fetch_all_candles
    # TODO if last inserted > date requested => start from last
    symbolObj, created = Symbol.objects.get_or_create(
        from_exchange=exchangeObj,
        currency=currencyObj,
        to_currency=toCurrencyObj,
    )

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

        # save historical
        historical.save()

    # update Symbol last insertion
    symbolObj.last_imported = candles.iloc[-1]["datetime"]
    symbolObj.save()


def import_candles(symbol, since: dt = dt(2012, 1, 1, 0, 0, 0, 0), limit=10, exchange_id="binance", max_retries=3, timeframe="1m"):

    symbol = symbol.upper()
    since_datetime = int(since.timestamp() * 1000)

    exchange_class = getattr(ccxt, exchange_id)
    exchange = exchange_class({"apiKey": os.environ.get("BINANCE_API_KEY"), "secret": os.environ.get("BINANCE_API_SECRET")})

    fetch_all_candles(exchange, max_retries, symbol, timeframe, since_datetime, limit)

    # for candle in candles:
    #     print(candle)
