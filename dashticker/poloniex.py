import json
import time
from decimal import Decimal

import redis

from dashticker import redis_key
from dashticker.polling import poll


def main():
    red = redis.StrictRedis()
    red.get('test')

    poller = poll('https://poloniex.com/public?command=returnTicker', 1)
    while True:
        market = 'BTC_DASH'
        data = poller.next()[market]

        ticker = {
            'source': 'poloniex',
            'market': market,
            'timestamp': time.time(),
            'bid': data['highestBid'],
            'ask': data['lowestAsk']
        }

        red.publish(redis_key, json.dumps(ticker))


if __name__ == "__main__":
    main()
