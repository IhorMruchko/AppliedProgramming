from abc import ABC, abstractmethod
from os import path
# region Parsers


class WeatherParser(ABC):
    """
    Class that represents functionality of the weather parser.
    Can be inherited for different formats: .txt, html, etc.
    """
    def __init__(self):
        """
        Initiates weather parser fields.

        weather - result of the parsing.
        source - source of the weather's data.
        """
        self.weather: dict = {}
        self._source: str = ""

    @abstractmethod
    def exception(self) -> Exception:
        """
        Returns exception in case of invalid source.
        """
        pass

    @abstractmethod
    def validate_source(self, source: str) -> bool:
        """
        Validates source to the weather data container.

        :param source: source of the weather data.
        """
        pass

    @abstractmethod
    def parse_weather(self, source: str) -> dict:
        """
        Returns weather data in the dictionary format.

        :param source: source of the weather data.
        :returns: True - if source is acceptable by the parser. False - otherwise.
        """
        pass

    def parse(self, source: str) -> dict:
        """
        Returns dictionary of the weather data.

        :param source: source of the weather data.
        :returns: weather data in the dictionary format.
        :raise Exception: Parser's exception if format is not valid.
        """
        if self.validate_source(source):
            return self.parse_weather(source)
        raise self.exception


class TextWeatherParser(WeatherParser):
    """
    Parse weather data from the text file.
    """
    def __init__(self):
        super(TextWeatherParser, self).__init__()

    @property
    def exception(self) -> Exception:
        return FileNotFoundError(f"\"{self._source}\" is not found.")

    def validate_source(self, source: str) -> bool:
        self._source = source
        return source.endswith(".txt") and path.exists(source)

    def parse_weather(self, source: str) -> dict:
        pass
# endregion


def main():
    txt = TextWeatherParser()
    txt.parse("input.txt")


if __name__ == "__main__":
    main()
