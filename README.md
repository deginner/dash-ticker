# dash-ticker
USD/DASH ticker service

## Install and run

```
git clone https://github.com/deginner/dash-ticker
cd dash-ticker
make
supervisord
```

Python 2.7 is required and a virtualenv is recommended. You can run `make test` to check if the ticker is working as intended.

#### supervisord files

The default config included will store pid and log files under `dash-ticker/service`. To change that, edit `supervisord.conf` and change the `[supervisord]` section to reflect your desired locations. After changing it, run `supervisorctl shutdown && supervisord` to restart it fresh.

## Serving the ticker

The USD/DASH ticker is stored under the Redis key `dashticker`, so an API would need to serve that data to clients. It's formatted to be served as JSON:

```
$ redis-cli get dashticker
"{\"timestamp\": 1452786211.806615, \"bid\": 346, \"bid_display\": \"3.46\", \"source\": \"coinapult_poloniex\", \"ask\": 355, \"ask_display\": \"3.55\", \"market\": \"USD_DASH\"}"
```

#### Serving using nginx + redis

To avoid some overhead you can serve the data directly via nginx combined with a redis module. You might want to use the `openresty` distribution of nginx which includes that as well other useful modules, and the following example assumes it's being used.

Just like the `openresty` documentation mentions, you can start by creating the following dirs:

```
mkdir work
cd work
mkdir conf logs
```

Then create `conf/nginx.conf` with the following content:

```
worker_processes 4;
error_log logs/error.log;

events {
  worker_connections 1024;
}

http {
  server {
    listen 8450;
    location = /v1/ticker/USD_DASH {
    default_type application/json;

    content_by_lua '
      local json = require "cjson"
      local redis = require "resty.redis"
      local red = redis:new()
      red:set_timeout(500)

      local ok, err = red:connect("127.0.0.1", 6379)
      if not ok then
        ngx.say(json.encode({error = "server not active"}))
        return
      end

      local res, err = red:get("dashticker")
      if not res then
        ngx.say(json.encode({error = "server misconfigured"}))
        return
      end
      if res == ngx.null then
        ngx.say(json.encode({error = "no ticker data"}))
        return
      end

      ngx.say(res)
    ';
    }
  }
}
```

Then nginx/openresty can be started as:

```
openresty -p `pwd` -c conf/nginx.conf
```

If this server is serving the data directly to clients, it will likely be doing so by using ssl certs. The above config can be updated to include any diretives that you would use in a typical nginx configuration.
