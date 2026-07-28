import logging
from pathlib import Path
from typing import override


class LogRecordFilter(logging.Filter):
    """
    Custom log records filter handler.

    "filters": {
      "drop_health": {
        "()": "fastapi_ml_example.core.logging.LogRecordFilter",
        "patterns": ["~", "GET /health"]
      }
    }

    See also: https://docs.python.org/3/library/logging.config.html
    """
    def __init__(self, patterns: str | list[str], *, exclude: bool = False) -> None:
        "Initialize log filter with specified patterns."
        super().__init__()
        self.exclude = exclude
        self.patterns = patterns if isinstance(patterns, list) else [patterns]

    @override
    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        matches = any(filt in msg for filt in self.patterns)
        return self.exclude ^ matches


def configure_logging(level: int = logging.INFO, log_file: Path | None = None) -> None:
    "Configure app root logger on startup."
    handlers: list[logging.Handler] = [logging.StreamHandler()]  # default stream=sys.stderr
    if log_file:
        # TODO: flag to clear log file contents?
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=level, handlers=handlers,
        format="INTERNAL %(asctime)s %(levelname)-8s %(name)s: %(message)s",
    )


# def get_logger(name: str) -> logging.Logger:
#     "Get a logger by its name (usually module __name__) wrapper."
#     return logging.getLogger(name)
