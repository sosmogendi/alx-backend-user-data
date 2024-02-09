import logging
import re


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    def __init__(self, fields: list):
        """
        Initialize RedactingFormatter with a list of fields to redact.

        Args:
            fields (list): List of strings representing fields to redact.
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


if __name__ == "__main__":
    message = "name=Bob;email=bob@dylan.com;ssn=000-123-0000;password=bobby2019;"
    log_record = logging.LogRecord("my_logger", logging.INFO, None, None, message, None, None)
    formatter = RedactingFormatter(fields=("email", "ssn", "password"))
    print(formatter.format(log_record))
