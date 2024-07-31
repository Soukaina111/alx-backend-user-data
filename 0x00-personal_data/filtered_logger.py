#!/usr/bin/env python3
""" Use of regex in replacing occurrences of certain field values """
import re
from typing import List
import logging
import mysql.connector
import os


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
        """ Returns filtered values from log records """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


PII_FIELDS = ("name", "email", "password", "ssn", "phone")


def get_db() -> mysql.connector.connection.MYSQLConnection:
    """ Connection to MySQL environment """
    db_connect = mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )
    return db_connect


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ Obfuscate specified fields in log messages """
    for fd in fields:
        message = re.sub(f'{fd}=(.*?){separator}',
                         f'{fd}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """ Returns a logging.Logger object """
    ggl = logging.getLogger("user_data")
    ggl.setLevel(logging.INFO)
    ggl.propagate = False

    to_handler = logging.StreamHandler()
    to_handler.setLevel(logging.INFO)

    formatter = RedactingFormatter(list(PII_FIELDS))
    to_handler.setFormatter(formatter)

    ggl.addHandler(to_handler)
    return ggl


def main() -> None:
    """ Obtain database connection, retrieve all rows from users table,
    and display each row under a filtered format """
    datab = get_db()
    sor = db.cursor()
    sor.execute("SELECT * FROM users;")

    headers = [field[0] for field in sor.description]
    ggl = get_logger()

    for r in sor:
        data_res = ''
        for f, p in zip(r, headers):
            data_res += f'{p}={(f)}; '
        ggl.info(data-res)

    sor.close()
    datab.close()


if __name__ == '__main__':
    main()
