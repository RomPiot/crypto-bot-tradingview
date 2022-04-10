import time
from datetime import datetime, timedelta

# import os
import pandas as pd
import asyncio
from django.utils import timezone
import ccxt.async_support as ccxt
from crypto.services.constants import TIMEFRAME
from crypto.models import Exchange, Historical, Symbol


def exchange_api(exchange: Exchange):
    # exchange_class = getattr(ccxt, exchange.slug)
    # env_exchange_api_key = f"{exchange.slug}_API_KEY".upper()
    # env_exchange_api_secret = f"{exchange.slug}_API_SECRET".upper()

    # return exchange_class(
    #     {
    #         "options": {
    #             "adjustForTimeDifference": True,
    #             "recvWindow": 10000,
    #         },
    #         "apiKey": os.environ.get(env_exchange_api_key),
    #         "secret": os.environ.get(env_exchange_api_secret),
    #         "enableRateLimit": True,
    #     }
    # )

    exchange_class = getattr(ccxt, exchange.slug)({"enableRateLimit": True})
    exchange_class.throttle.config["maxCapacity"] = 100000
    exchange_class.throttle.config["delay"] = 0.01

    # if not exchange_class.has["fetchOHLCV"]:
    #     print(f"Skipping {exchange.slug}")
    #     return
    # if exchange_class.timeframes is None:
    #     print(f"Skipping {exchange.slug}")
    #     return

    # # TODO : get timeframe
    # if "1m" not in exchange_class.timeframes:
    #     print(f"Skipping {exchange.slug}")
    #     return

    return exchange_class


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

    if getattr(pair_symbol, last_imported_timeframe_attr) < last_imported:
        setattr(pair_symbol, last_imported_timeframe_attr, last_imported)
        pair_symbol.save()

    print(
        pair_symbol.from_currency,
        timeframe,
        pair_symbol.to_currency,
        getattr(pair_symbol, last_imported_timeframe_attr),
    )


async def fetch_ohlcv(exchange: Exchange, pair_symbol: Symbol, timeframe: str, since, limit: int):
    since_unixtimestamp = int(since.timestamp() * 1000)

    # exchange_api(exchange).fetch_ohlcv(pair_symbol.name, timeframe, since_unixtimestamp, int(limit))
    ohlcv = await exchange_api(exchange).fetch_ohlcv(pair_symbol.name, timeframe, since_unixtimestamp, int(limit))
    return ohlcv
    # if ohlcv:
    #     save_historical(exchange=exchange, pair_symbol=pair_symbol, timeframe=timeframe, ohlcv_list=ohlcv)


async def fetch_historical_data(exchange: Exchange, timeframes: list, pair_symbols=None):
    LIMIT = 500
    reqests_loop = []

    now = datetime.now(tz=timezone.utc)

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

            datetime_loops = [since]

            while since < now:
                ms_to_add = int(exchange.limit) * int(TIMEFRAME[timeframe]["ms"])
                since = since + timedelta(milliseconds=ms_to_add)
                if since < now:
                    datetime_loops.append(since)

            # request_executed = 0
            # total_request = len(datetime_loops)

            for since_date in range(0, len(datetime_loops), LIMIT):
                # print(since_date)
                reqests_loop.append(
                    fetch_ohlcv(
                        exchange=exchange,
                        pair_symbol=pair,
                        timeframe=timeframe,
                        since=since_date,
                        limit=int(exchange.limit),
                    )
                )

                

            #     ohlcv = await asyncio.gather(*ohlcv_to_execute)

            #     all_ohlcv.append(ohlcv)

            #     request_executed += 1

            # while request_executed <= total_request:
            #     print(f"Loading {request_executed}/{total_request} requests | {len(all_ohlcv)} candles loaded")
            #     time.sleep(2)

            # )
    # while loops:
    #     print(len(loops))
    #     current_loops = loops[0:9]
    #     await asyncio.gather(*current_loops)
    #     del loops[0:9]
    # await asyncio.gather(*loops)

    # asyncio.wait

    # await asyncio.gather(*loops)
    # pending = asyncio.Task.all_tasks()
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # loop.run_until_complete(asyncio.gather(*pending))

    print("END")

    await exchange_api(exchange).close()


def import_currencies(exchange: Exchange, timeframes: list, pair_symbols=None):
    start = time.process_time()

    loop = asyncio.get_event_loop()

    data = loop.run_until_complete(
        fetch_historical_data(exchange=exchange, timeframes=timeframes, pair_symbols=pair_symbols)
    )

    print(data)

    duration = time.process_time() - start
    print(f"Seconds Elapsed: {duration}")


if __name__ == "__main__":
    exchange = Exchange.objects.get(slug="binance")
    timeframes = ["1h"]
    pair_symbol = Symbol.objects.get(name="BTC/USDT")
    import_currencies(exchange=exchange, timeframes=timeframes, pair_symbols=[pair_symbol])
