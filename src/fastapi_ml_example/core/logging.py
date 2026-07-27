import logging
import sys

def configure_logging(level: int = logging.INFO) -> None:
    "Configure app root logger on startup."
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        ),
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(handler)


# def get_logger(name: str) -> logging.Logger:
#     "Get a logger by its name (usually module __name__) wrapper."
#     return logging.getLogger(name)
