import logging
from rich.logging import RichHandler

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"

_initialized = False

def init_logging(level: int = logging.INFO):
    global _initialized
    if _initialized:
        return
    logging.basicConfig(
        level=level,
        format=LOG_FORMAT,
        datefmt="%H:%M:%S",
        handlers=[RichHandler(rich_tracebacks=True)]
    )
    _initialized = True


def get_logger(name: str) -> logging.Logger:
    if not _initialized:
        init_logging()
    return logging.getLogger(name)
