import time
import json
import urllib2


def poll(url, delay):
    while True:
        res = urllib2.urlopen(urllib2.Request(url))
        data = json.loads(res.read())
        yield data

        time.sleep(delay)
