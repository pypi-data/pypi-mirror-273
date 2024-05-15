"""This module contains logger related utilities."""

from __future__ import annotations
import logging
import os

from sys import stdout
from . import style


class Logger:
    """A generic logger class allowing logs to be send to stdout and a log file.

    Attributes:
        logger: The logger object.
    """

    def __init__(
        self,
        log_name: str,
        log_file: None | str = None,
        log_level: int = logging.CRITICAL,
        log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    ):
        """Initializes the logger.

        Args:
            log_name: A name for the logger, allowing differentiating between logs.
            log_file: The path to the log file.
            log_level: The level threshold of the logs to be displayed.
            log_format: The format of the logs.

        Example using the Logger class to log to stdout and a file:
        >>> logger = Logger("my_logger", log_file="my_log.log", log_level=logging.DEBUG)

        Example using the Logger class to log to stdout only:
        >>> logger = Logger("my_logger", log_level=logging.DEBUG)
        """
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(log_level)
        console_handler = logging.StreamHandler(stdout)

        console_handler.setFormatter(logging.Formatter(log_format))
        self.logger.addHandler(console_handler)

        if log_file:
            log_dir = os.path.dirname(log_file)
            if not os.path.exists(log_dir) and len(log_dir.strip()) > 0:
                os.makedirs(log_dir, exist_ok=True)
            file_handler = logging.FileHandler(log_file, mode="w")
            file_handler.setFormatter(logging.Formatter(log_format))
            self.logger.addHandler(file_handler)

    def _log(self, msg: str, level: str) -> None:
        """Logs a message with a given level.

        Args:
            msg: The message to log.
            level: The level of the message.
        """
        if level == "info":
            self.logger.info(msg)
        if level == "debug":
            self.logger.debug(msg)
        if level == "warning":
            self.logger.warning("%s%s", style.Color.WARNING, msg)
        if level == "error":
            self.logger.error("%s%s", style.Color.ERROR, msg)

    def debug(self, msg: str) -> None:
        """Logs a debug message.

        Args:
            msg: The message to log.
        """
        self._log(msg, "debug")

    def info(self, msg: str) -> None:
        """Logs an info message.

        Args:
            msg: The message to log.
        """
        self._log(msg, "info")

    def warning(self, msg: str) -> None:
        """Logs a warning message.

        Args:
            msg: The message to log.
        """
        self._log(msg, "warning")

    def error(self, msg: str) -> None:
        """Logs an error message.

        Args:
            msg: The message to log.
        """
        self._log(msg, "error")
