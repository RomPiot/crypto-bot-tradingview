from pprint import pprint
import ccxt.async_support as ccxt
from datetime import datetime, timedelta, timezone
import pandas as pd
import asyncio
import time
import asyncio


EXCHANGES = ["binance"]
SYMBOL_PAIRS = ["BTC/USDT"]
TIMEFRAMES = ["1h", "1d", "1w"]
TIMEFRAMES = ["1h"]
LIMIT = 1000


async def fetch_history_data(start_time: datetime):
    start_time = start_time.replace(second=0, microsecond=0)

    ohlcv_datas = {}
    exchanges = []

    # for exchange in ccxt.exchanges:
    for exchange_slug in EXCHANGES:
        # Turn on rate limiting
        exchange = getattr(ccxt, exchange_slug)({"enableRateLimit": True})
        exchange.throttle.config["maxCapacity"] = 100000
        exchange.throttle.config["delay"] = 0.01
        exchanges.append(exchange)

        if not exchange.has["fetchOHLCV"]:
            print(f"Skipping {exchange_slug}")
            continue
        if exchange.timeframes is None:
            print(f"Skipping {exchange_slug}")
            continue

        if exchange_slug not in ohlcv_datas:
            ohlcv_datas[exchange_slug] = {}

        await exchange.load_markets()

        for timeframe in TIMEFRAMES:
            if timeframe not in exchange.timeframes:
                print(f"Skipping {exchange_slug} - {timeframe}")
                continue

            if timeframe not in ohlcv_datas[exchange_slug]:
                ohlcv_datas[exchange_slug][timeframe] = {}

            intervals = pd.date_range(start_time, datetime.now().replace(second=0, microsecond=0), freq=timeframe)
            # print(len(intervals))

            for symbol_pair in SYMBOL_PAIRS:
                if symbol_pair not in exchange.symbols:
                    continue

                reqests_to_execute = []

                for index in range(0, len(intervals), LIMIT):
                    timestamp = int(intervals[index].replace(tzinfo=timezone.utc).timestamp() * 1000)
                    reqests_to_execute.append(
                        exchange.fetch_ohlcv(symbol_pair, timeframe, since=timestamp, limit=LIMIT)
                    )

                print(f"Fetching : {exchange} - {symbol_pair} - {timeframe}")

                try:
                    data = await asyncio.gather(*reqests_to_execute)

                    history = []
                    for chunk in data:
                        history += chunk

                    ohlcv_datas[exchange_slug][timeframe][symbol_pair] = history

                except BaseException as error:
                    print(f"Unexpected {error=}, {type(error)=}")

    for exchange in exchanges:
        await exchange.close()

    columns = ["datetime", "open", "high", "low", "close", "volume"]

    df = pd.DataFrame(columns=(["exchange", "timeframe", "symbol_pair"] + columns))

    for exchange, data_per_timeframe in ohlcv_datas.items():
        for timeframe, datas in data_per_timeframe.items():
            for symbol_pair, history in datas.items():
                idf = pd.DataFrame(history, columns=columns)
                idf["exchange"] = exchange
                idf["timeframe"] = timeframe
                idf["symbol_pair"] = symbol_pair
                df = pd.concat([df, idf])

    df["datetime"] = df["datetime"].apply(lambda x: datetime.fromtimestamp(int(x) / 1000, tz=timezone.utc))

    df = df.set_index(["exchange", "symbol_pair", "timeframe", "datetime"]).sort_index()

    return df


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(fetch_history_data(datetime(2012, 1, 1, 0, 0, 0, 0)))

    print(data)
