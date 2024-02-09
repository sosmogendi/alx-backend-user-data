import logging
import re
import mysql.connector
from typing import List


class CustomFormatter(logging.Formatter):
    """ Custom Formatter class """

    def __init__(self, fields: List[str]):
        """
        Initialize CustomFormatter with a list of fields to redact.

        Args:
            fields (List[str]): List of strings representing fields to redact.
        """
        super().__init__("[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s")
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, redacting sensitive fields.

        Args:
            record (logging.LogRecord): Log record to be formatted.

        Returns:
            str: Formatted log message.
        """
        message = record.getMessage()
        for field in self.fields:
            message = re.sub(f'{field}=.*?(?={self.SEPARATOR})',
                             f'{field}={self.REDACTION}', message)
        record.msg = message
        return super().format(record)


def filter_data(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """ Returns a log message obfuscated """
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def initialize_logger() -> logging.Logger:
    """ Returns a Logger Object """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(CustomFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)

    return logger


def initialize_database_connection() -> mysql.connector.connection.MySQLConnection:
    """ Returns a connector to a MySQL database """
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")

    connection = mysql.connector.connection.MySQLConnection(user=username,
                                                            password=password,
                                                            host=host,
                                                            database=db_name)
    return connection


def main():
    """
    Obtain a database connection using initialize_database_connection and retrieves all rows
    in the users table and display each row under a filtered format
    """
    connection = initialize_database_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users;")
    field_names = [i[0] for i in cursor.description]

    logger = initialize_logger()

    for row in cursor:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, field_names))
        logger.info(str_row.strip())

    cursor.close()
    connection.close()


if __name__ == '__main__':
    main()
