import logging
import os
from datetime import UTC, datetime

import colorlog


class IsoTimeFormatter(colorlog.ColoredFormatter):
    def formatTime(self, record, datefmt=None):
        return datetime.fromtimestamp(record.created, tz=UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def init_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name=name)
    logger.setLevel(os.getenv("LOG_LEVEL", "INFO").upper())

    if logger.handlers:
        return logger

    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s")

    console = logging.StreamHandler()

    formatter = IsoTimeFormatter(
        "[%(asctime)s] %(log_color)s[%(levelname)s]%(reset)s [%(name)s] %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )

    console.setFormatter(formatter)

    logger.addHandler(console)

    return logger
