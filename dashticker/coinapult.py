import json
import time
from decimal import Decimal

from dashticker import redis_key
from dashticker.ws import Client, Handler


def on_message(data, redis):
    market = 'USD_BTC'
    if data['type'] != 'ticker':
        return

    ticker = {
        'source': 'coinapult',
        'market': market,
        'timestamp': time.time(),
        'ask': int(Decimal(data['small']['ask']) * 100),
        'bid': int(Decimal(data['small']['bid']) * 100)
    }

    redis.publish(redis_key, json.dumps(ticker))


def main():
    handler = Handler('coinapult', on_message)
    cli = Client("wss://stream.coinapult.com:8123/websocket", handler)


if __name__ == "__main__":
    main()
