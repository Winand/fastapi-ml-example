If API versioning is required use the following api folder structure:
```
api/
|- routers/
   |- health.py
   |- v1/
      |- health.py
```


uvicorn logging is configured on startup in Docker via --log-config=log_config.json
When started manually `core.logging.configure_logging` is used for basic config.


Log records filters can be configured in `docker/log_config.json` for handlers or loggers:
```
{
    "filters": {
      "drop_health": {
        "()": "fastapi_ml_example.core.logging.LogRecordFilter",
        "patterns": ["~", "GET /health"]
      }
    },
    "handlers": {
        "console": {..., "filters": ["drop_health"]}
    },
    "loggers": {
        "uvicorn.access": {..., "filters": ["drop_health"]},
    }
}
```
