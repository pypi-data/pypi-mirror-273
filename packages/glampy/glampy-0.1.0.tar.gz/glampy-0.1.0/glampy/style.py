"""Utility functions for styling terminal output."""

from enum import Enum


class Sign(str, Enum):
    """Unicode symbols for use in terminal output."""

    WARNING = "\u26A0"
    CRASH = "\U0001F4A5"
    PERSON = "\U0001F464"
    LOADING = "\U0001F5D8"
    CHECKMARK = "\u2713"
    TRIANGLE = "\u25B6"
    CIRCLE = "\u25EF"


class Color(str, Enum):
    """Colours for use in terminal output."""

    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    ERROR = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    ITALIC = "\33[3m"
    UNDERLINE = "\033[4m"
    GREY = "\033[90m"
