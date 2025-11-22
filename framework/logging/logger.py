import logging
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Adjust imports to match your project structure
from framework.config import LOG_BACKUP_COUNT, LOG_DIR, LOG_FILE_NAME, LOG_MAX_BYTES
from framework.utils.singleton_meta import SingletonMeta


class Logger(metaclass=SingletonMeta):
    def __init__(self):
        self.logger = logging.getLogger("FrameworkLogger")
        self.logger.setLevel(logging.DEBUG)

        if self.logger.hasHandlers():
            return

        # Create log directory if it doesn't exist
        Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

        # Format: YYYY-MM-DD_HH-MM-SS (e.g., 2023-11-22_14-30-05)
        # We use underscores instead of colons because colons are illegal in Windows filenames.
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Result: logs/app_log_2023-11-22_14-30-05.log
        current_log_name = f"{LOG_FILE_NAME}_{timestamp}.log"
        log_file_path = Path(LOG_DIR) / current_log_name

        # Create file handler
        file_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=LOG_MAX_BYTES,
            backupCount=LOG_BACKUP_COUNT,
            encoding="utf-8",
        )
        file_handler.setLevel(logging.DEBUG)

        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger


# Initialize the logger instance
logger = Logger().get_logger()
