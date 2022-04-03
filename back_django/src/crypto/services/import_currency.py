import asyncio
import ccxt.async_support as ccxt
from datetime import datetime, timedelta
import os
import pandas as pd
from crypto.services.constants import TIMEFRAME
from crypto.models import Currency, Exchange, Historical, Symbol
from django.utils import timezone


async def import_multiple_currency(symbols, timeframes):
    if not symbols:
        symbols = Symbol.objects.all()

    if not timeframes:
        # TODO : get entries from TIMEFRAME
        timeframes = {
            "1h": "hour",
            "4h": "four_hours",
            "12h": "twelve_hours",
            "1d": "day",
            "1w": "week",
        }

    for timeframe in timeframes:
        for symbol_obj in symbols:
            timeframe_db_name = TIMEFRAME[timeframe]["db_name"]
            last_imported_timeframe_attr = f"last_imported_{timeframe_db_name}"
            last_imported = getattr(symbol_obj, last_imported_timeframe_attr)

            if last_imported:
                date_start = last_imported
            else:
                date_start = datetime(2012, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)

            symbol = f"{symbol_obj.from_currency.slug}/{symbol_obj.to_currency.slug}"

            print(symbol)
            print(timeframe)

            await import_multiple_historical(
                symbol_obj=symbol_obj,
                since=date_start,
                exchange=symbol_obj.from_exchange,
                timeframe=timeframe,
            )


async def import_multiple_historical(
    symbol_obj,
    since,
    exchange_obj: Exchange,
    timeframe,
):
    timeframe_db_name = TIMEFRAME[timeframe]["db_name"]
    last_imported_timeframe_attr = f"last_imported_{timeframe_db_name}"
    last_imported = getattr(symbol_obj, last_imported_timeframe_attr)

    if last_imported:
        date_start = last_imported
    else:
        date_start = datetime(2012, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)

    now = datetime.utcnow()

    datetime_array = [date_start]
    last_datetime = date_start
    result_ohlcv = []
    current_request = 0

    while last_datetime < now:
        last_datetime = last_datetime + (exchange_obj.limit) * timeframe["ms"]
        if last_datetime < now:
            datetime_array.append(last_datetime)

    # total_request = len(datetime_array)

    pair_symbol = f"{symbol_obj.from_currency.slug}/{symbol_obj.to_currency.slug}".upper()

    print(pair_symbol)
    print(timeframe)

    exchange_class = getattr(ccxt, exchange_obj.slug)
    exchange = exchange_class(
        {"apiKey": os.environ.get("BINANCE_API_KEY"), "secret": os.environ.get("BINANCE_API_SECRET")}
    )

    for datetime_item in datetime_array:
        since_unixtimestamp = int(datetime_item.timestamp() * 1000)

        ohlcv = await exchange.fetch_ohlcv(
            symbol=pair_symbol, timeframe=timeframe, since=since_unixtimestamp, limit=exchange.limit
        )
        asyncio.run(
            retry_fetch_ohlcv(
                exchange=exchange,
                symbol=pair_symbol,
                timeframe=timeframe,
                since=datetime_item,
                limit=exchange.limit,
            )
        )
        result_ohlcv = result_ohlcv.append(ohlcv)
        current_request += 1


def import_historical(
    symbol,
    since: datetime = datetime(2012, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc),
    limit=1000000,  # TODO : remove & create symbol_obj.from_exchange.limit
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

    symbol_obj, created = Symbol.objects.get_or_create(
        from_exchange=exchangeObj,
        from_currency=currencyObj,
        to_currency=toCurrencyObj,
    )

    timeframe_db_name = TIMEFRAME[timeframe]["db_name"]
    last_imported_timeframe_attr = f"last_imported_{timeframe_db_name}"
    last_imported = getattr(symbol_obj, last_imported_timeframe_attr)

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

        print(candles)
        print(type(candles))
        print(ohlcv)
        print(type(ohlcv))

        candles = candles + asyncio.run(ohlcv)

        since = save_candles(exchangeObj, symbol_obj, timeframe, candles)
        candles = []
        retry_nb += 1

    return "All imported"


async def retry_fetch_ohlcv(exchange, symbol, timeframe, since, limit):
    since_unixtimestamp = int(since.timestamp() * 1000)
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since_unixtimestamp, limit)
    return ohlcv


def save_candles(exchangeObj, symbol_obj, timeframe, candles):
    candles = pd.DataFrame(
        data=candles,
        columns=["datetime", "open", "high", "low", "close", "volume"],
    )
    candles["datetime"] = candles["datetime"].apply(lambda x: datetime.fromtimestamp(int(x) / 1000, tz=timezone.utc))

    historical_list = []

    for _, candle in candles.iterrows():
        historical = Historical(
            from_exchange=exchangeObj,
            symbol=symbol_obj,
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
    timeframe_db_name = TIMEFRAME[timeframe]["db_name"]
    last_imported_timeframe_attr = f"last_imported_{timeframe_db_name}"
    last_imported = candles.iloc[-1]["datetime"]
    setattr(symbol_obj, last_imported_timeframe_attr, last_imported)
    symbol_obj.save()

    next_datetime = getattr(symbol_obj, last_imported_timeframe_attr) + timedelta(seconds=1)
    return next_datetime
