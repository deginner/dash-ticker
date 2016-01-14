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
