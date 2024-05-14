from datetime import datetime as dt


class Parser:

    IGNORE_STR_VALUES = []

    CHAIN_ID_MAP = {
        "ethereum": 1,
    }

    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def get_timestamp() -> int:
        """
        Get the current timestamp in milliseconds
        :return: 13 digit timestamp
        """
        return int(dt.now().timestamp() * 1000)

    def parse_str(self, value: str, to_type: callable) -> any:
        """
        Parse a string to a specific type
        :param value: The value to parse
        :param to_type: The type to parse to
        :return: The parsed value
        """
        if value in self.IGNORE_STR_VALUES or value is None:
            return None
        return to_type(value)
