import asyncio
from datetime import datetime, timedelta

from binance import AsyncClient, BinanceSocketManager

from binanceparser.settings import BINANCE_API_KEY, BINANCE_SECRET_KEY


async def stream_price(ts):
    """
    Start stream the price of a given trading socket, and if the price
    falls by more than one percent in one hour, the function yields
    the percentage, maximum price in one hour, and current price.

    Args:
        ts: trade socket

    Yields:
        List[float, float, float]: Percent, max price, current price
    """
    last_hour = datetime.now()
    max_price = None
    while True:
        res = await ts.recv()
        price = float(res["p"])
        is_hour_passed = datetime.now() - last_hour >= timedelta(hours=1)
        if not max_price or price > max_price or is_hour_passed:
            last_hour = datetime.now()
            max_price = price
            continue
        percent = 1 - price / max_price
        if percent >= 0.01:
            last_hour = datetime.now()
            max_price = price
            yield percent, max_price, price


async def init():
    client = await AsyncClient.create(
        api_key=BINANCE_API_KEY,
        api_secret=BINANCE_SECRET_KEY,
    )
    bsm = BinanceSocketManager(client)

    print(
        'Application is started successfully.\n'
        'Stream price...'
    )

    async with bsm.trade_socket('XRP/USDT') as ts:
        async for percent, max_price, price in stream_price(ts):
            print(
                f'Price changed by {percent * 100}%:\n'
                f'\tBefore price: {max_price}\n'
                f'\tThen price: {price}'
            )

    await client.close_connection()


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init())


if __name__ == '__main__':
    main()
