from __future__ import annotations

import logging
from enum import StrEnum
from logging.handlers import RotatingFileHandler
from pathlib import Path


class LoggingLevel(StrEnum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'


class FixedLengthFilter(logging.Filter):
    def __init__(self, max_length: int) -> None:
        """Initialize the filter with a maximum length.

        Args:
            max_length: The maximum length of log messages.
        """
        super().__init__()
        self.max_length = max_length

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Filters the log record by limiting the length of the message.

        Args:
            record (logging.LogRecord): The log record to be filtered.

        Returns:
            bool: True if the record should be logged, False otherwise.
        """
        record.msg = self.limit_string_length(record.msg, self.max_length)
        return True

    @staticmethod
    def limit_string_length(string: str, max_length: int = 100):
        if len(string) <= max_length:
            return string
        half = max_length // 2
        return string[:half] + '...' + string[-half:]


def setup_logger(
    name: str,
    file_max_size_bytes: int = 1000000,
    files_count: int = 5,
    log_length: int = 100,
    level: LoggingLevel = logging.DEBUG,
) -> logging.Logger:
    """
    Setup a logger for the given name.

    Args:
        name (str): The name of the logger.
        file_max_size_bytes (int, optional): The maximum size of each log file in bytes. Defaults to 1000000.
        files_count (int, optional): The maximum number of log files to keep. Defaults to 5.
        log_length (int, optional): The maximum length of each log message. Defaults to 100.

    Returns:
        logging.Logger: The logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    logs_folder = Path(__file__).resolve().parent.parent / 'logs'
    log_file = logs_folder / f'{name}.log'
    log_file.parent.mkdir(parents=True, exist_ok=True)
    if not log_file.exists():
        log_file.touch()

    file_handler = RotatingFileHandler(
        log_file, maxBytes=file_max_size_bytes, backupCount=files_count
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    file_handler.addFilter(FixedLengthFilter(max_length=log_length))

    logger.addHandler(file_handler)
    return logger
