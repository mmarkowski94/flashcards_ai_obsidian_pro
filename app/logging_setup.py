import atexit
import logging
import os
import tomllib
from pathlib import Path
from typing import Any


def setup_logging() -> None:
    if os.getenv("TESTS") == "1":
        return None

    config_file: Path = Path(".logging_configs/config.toml")
    with open(config_file, "rb") as file:
        config: dict[str, Any] = tomllib.load(file)

    logging.config.dictConfig(config)

    queue_handler: logging.Handler | None = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()  # type: ignore [attr-defined]
        atexit.register(queue_handler.listener.stop)  # type: ignore [attr-defined]
