import logging
from logging.handlers import RotatingFileHandler
import os


LOG_DIR = "logs"
LOG_FILE = "app.log"


def setup_logger():
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger("poem_bot")
    logger.setLevel(logging.INFO)

    # ❗ щоб не було дублювання логів
    if logger.handlers:
        return logger

    log_path = os.path.join(LOG_DIR, LOG_FILE)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 🔹 FILE handler
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # 🔹 CONSOLE handler (залишаємо, дуже корисно)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
