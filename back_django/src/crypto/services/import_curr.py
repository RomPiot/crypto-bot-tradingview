import asyncio
import ccxt.async_support as ccxt
import os
from datetime import datetime
from django.utils import timezone
from crypto.services.constants import TIMEFRAME
from crypto.models import Exchange, Historical, Symbol
import pandas as pd


def exchange_api(exchange: Exchange):
    exchange_class = getattr(ccxt, exchange.slug)
    env_exchange_api_key = f"{exchange.slug}_API_KEY".upper()
    env_exchange_api_secret = f"{exchange.slug}_API_SECRET".upper()

    return exchange_class(
        {"apiKey": os.environ.get(env_exchange_api_key), "secret": os.environ.get(env_exchange_api_secret)}
    )


def save_historical(exchange: Exchange, pair_symbol: Symbol, timeframe: str, ohlcv_list):
    ohlcv_list = pd.DataFrame(
        data=ohlcv_list,
        columns=["datetime", "open", "high", "low", "close", "volume"],
    )
    ohlcv_list["datetime"] = ohlcv_list["datetime"].apply(
        lambda x: datetime.fromtimestamp(int(x) / 1000, tz=timezone.utc)
    )

    historical_list = []

    for _, ohlcv in ohlcv_list.iterrows():
        historical = Historical(
            from_exchange=exchange,
            symbol=pair_symbol,
            timeframe=timeframe,
            datetime=ohlcv["datetime"],
            open=ohlcv["open"],
            close=ohlcv["close"],
            high=ohlcv["high"],
            low=ohlcv["low"],
            volume=ohlcv["volume"],
        )

        historical_list.append(historical)

    # update all historical
    Historical.objects.bulk_create(historical_list, ignore_conflicts=True)

    # update Symbol last imported datetime from timeframe type
    timeframe_db_name = TIMEFRAME[timeframe]["db_name"]
    last_imported_timeframe_attr = f"last_imported_{timeframe_db_name}"
    last_imported = ohlcv_list.iloc[-1]["datetime"]
    setattr(pair_symbol, last_imported_timeframe_attr, last_imported)
    print(pair_symbol.from_currency, pair_symbol.to_currency, pair_symbol.last_imported_fiveteen_minutes)
    pair_symbol.save()


async def fetch_ohlcv(exchange: Exchange, pair_symbol: Symbol, timeframe: str, since, limit: int):
    since_unixtimestamp = int(since.timestamp() * 1000)
    pair_string = f"{pair_symbol.from_currency.slug}/{pair_symbol.to_currency.slug}".upper()

    ohlcv = await exchange_api(exchange).fetch_ohlcv(pair_string, timeframe, since_unixtimestamp, int(limit))
    if ohlcv:
        save_historical(exchange=exchange, pair_symbol=pair_symbol, timeframe=timeframe, ohlcv_list=ohlcv)


async def import_currencies_async(exchange: Exchange, timeframes: list, pair_symbols=None):
    loops = []

    if not pair_symbols:
        pair_symbols = Symbol.objects.all()

    for timeframe in timeframes:
        for pair in pair_symbols:
            timeframe_db_name = TIMEFRAME[timeframe]["db_name"]
            last_imported_timeframe_attr = f"last_imported_{timeframe_db_name}"
            last_imported = getattr(pair, last_imported_timeframe_attr)

            if last_imported:
                since = last_imported
            else:
                since = datetime(2012, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)

            loops.append(
                fetch_ohlcv(
                    exchange=exchange,
                    pair_symbol=pair,
                    timeframe=timeframe,
                    since=since,
                    limit=int(exchange.limit),
                )
            )

    await asyncio.gather(*loops)
    await exchange_api(exchange).close()


def import_currencies(exchange: Exchange, timeframes: list, pair_symbols=None):

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(import_currencies_async(exchange=exchange, timeframes=timeframes))
    loop.close()
