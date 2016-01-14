import os
import json
import errno

import redis
import websocket

from dashticker.log import get_logger


class Client:
    def __init__(self, url, handler):
        self.logger = handler.logger

        if int(os.getenv('WS_DEBUG', default='0')):
            websocket.enableTrace(True)
            self.logger.debug("websocket debug enabled")

        self.url = url
        self._setup(handler.on_message)

    def _setup(self, on_message):
        ws = websocket.WebSocketApp(self.url,
                                    on_message=on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        ws.on_open = self.on_open
        ws.run_forever()

    def on_open(self, ws):
        self.logger.info("connection open")

    def on_close(self, ws):
        self.logger.info("connection closed")
        # Let the process die. When running under supervisord or similar,
        # it will be restarted automatically.
        raise SystemExit(errno.EHOSTDOWN)

    def on_error(self, ws, error):
        self.logger.error(error)


class Handler:

    def __init__(self, logger, on_message):
        self.redis = redis.StrictRedis()
        # Check if a redis-server is running.
        self.redis.get('test')

        if isinstance(logger, basestring):
            self.logger = get_logger(logger)
        else:
            self.logger = logger
        self._on_message = on_message

    def on_message(self, ws, message):
        data = json.loads(message)
        self._on_message(data, self.redis)
