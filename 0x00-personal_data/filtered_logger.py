#!/usr/bin/env python3
""" 0. Regex-ing """

import re
from typing import List
import logging


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ Create regex pattern to match fields and
    Replace matched fields with redaction"""
    for field in fields:
        message = re.sub(f'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Displays filtered values from log records """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


PII_FIELDS: List[str] = ["name", "email", "ssn", "phone"]


def get_logger() -> logging.Logger:
    """ Returns a logging.Logger object """
    user_logger = logging.getLogger("user_data")
    user_logger.setLevel(logging.INFO)
    user_logger.propagate = False

    log_handler = logging.StreamHandler()
    log_handler.setLevel(logging.INFO)

    log_formatter = RedactingFormatter(list(PII_FIELDS))
    log_handler.setFormatter(log_formatter)

    user_logger.addHandler(log_handler)
    return user_logger
