Project structure:
- `api` - FastAPI HTTP routes and dependencies
  - `deps.py` - FastAPI dependencies used in routes (ML model, prediction service, etc.)
- `schemas` - Pydantic models for input/output data
- `ml` - machine learning (ML) business logic
- `services` - data flow orchestration between HTTP and ML (prediction service)
- `core` - logging, exceptions, metrics, etc.
- `main.py` creates FastAPI app instance, includes routers, loads resources (ML model)


If API versioning is required use the following api folder structure:
```
api/
|- routers/
   |- health.py
   |- v1/
      |- health.py
```


uvicorn logging is configured on startup in Docker via `--log-config=log_config.json`.
When started manually `core.logging.configure_logging` is used for basic configuration.


Log records filter can be configured in `docker/log_config.json` for handlers or loggers:
```
{
    "filters": {
      "drop_health": {
        "()": "fastapi_ml_example.core.logging.LogRecordFilter",
        "patterns": ["GET /health"], "exclude": true
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
