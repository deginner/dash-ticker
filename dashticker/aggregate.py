import json
from decimal import Decimal

import redis
from dashticker import redis_key
from dashticker.log import get_logger


def get_ticker(usdbtc, btcdash):
    if usdbtc is None or btcdash is None:
        return

    oldest = min(usdbtc['timestamp'], btcdash['timestamp'])

    ticker = {
        'source': '{}_{}'.format(usdbtc['source'], btcdash['source']),
        'market': 'USD_DASH',
        'timestamp': oldest,
        'ask': None,
        'bid': None
    }

    for key in ('ask', 'bid'):
        cents = int(round(usdbtc[key] * Decimal(btcdash[key])))
        ticker[key] = cents
        ticker['{}_display'.format(key)] = '{:.2f}'.format(cents / Decimal(100))

    assert ticker['ask'] is not None
    assert ticker['bid'] is not None
    assert ticker['ask'] >= ticker['bid']

    return ticker


def store(red, logger, ticker):
    if ticker is None:
        return

    raw = json.dumps(ticker)
    logger.info(ticker)

    red.set(redis_key, raw)


def main():
    logger = get_logger('aggregate')

    red = redis.StrictRedis()
    red.get('test')

    sub = red.pubsub()
    sub.subscribe(redis_key)

    last_usdbtc_quote = None
    last_btcdash_quote = None

    for message in sub.listen():
        if message['type'] != 'message':
            continue

        data = json.loads(message['data'])
        market = data.pop('market')
        if data['source'] == 'poloniex':
            if market != 'BTC_DASH':
                raise Exception("Unknown market {}".format(market))
            last_btcdash_quote = data

        elif data['source'] == 'coinapult':
            if market != 'USD_BTC':
                raise Exception("Unknown market {}".format(market))
            last_usdbtc_quote = data

        tick = get_ticker(last_usdbtc_quote, last_btcdash_quote)
        store(red, logger, tick)


if __name__ == "__main__":
    main()
