import time
import json

import redis
from dashticker import redis_key


def test_simple():
    red = redis.StrictRedis()
    # Erase any previous ticker data.
    red.delete(redis_key)

    # Check if a new one shows up
    data = None
    attempts = 10
    time.sleep(0.1)
    while attempts > 0:
        attempts -= 1
        data = red.get(redis_key)
        if data:
            data = json.loads(data)
            break
        time.sleep(1)

    assert data is not None
    assert data['market'] == 'USD_DASH'
    assert data['source'] == 'coinapult_poloniex'
    assert data['ask'] > data['bid']
    assert isinstance(data['ask'], int)
    assert isinstance(data['bid'], int)
    assert isinstance(data['ask_display'], basestring)
    assert isinstance(data['bid_display'], basestring)
    assert isinstance(data['timestamp'], float)
