from abc import ABC, abstractmethod
from os import path
from re import split, compile, match


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

    File should contain lines line:
    [Country][Date][Time][Temperature][Pressure*][wind direction*]

    Between all elements must be delimiter - one of the symbols: # or <-> or tabulation (>= two spaces).
    * - value can be provided or writen as 'none'

    Country - any plain text.
    Date - date in format DD:MM:YYYY or DD/MM/YYYY.
    Time - time in format HH:MM.
    Temperature - integer value.
    Pressure - integer value.
    Wind direction - one of the symbols: N or NE or E or SE or S or SW or W or NW
    """

    def __init__(self):
        self.__date_format = compile(r"(\d{2}[/.]\d{2}[/.]\d{4})|(today)")
        self.__time_format = compile(r"\d{2}:\d{2}")
        self.__temperature_format = compile(r"-?\d+")
        self.__pressure_format = compile(r"\d+|(none)")
        self.__wind_format = compile(r"N|(NE)|E|(SE)|S|(SW)|W|(NW)|(none)")
        self.__formats = [self.__date_format, self.__time_format, self.__temperature_format, self.__pressure_format,
                          self.__wind_format]
        self.__delimiter = compile(r"<->|#|\s{2}")
        self.__encoding = "utf-8"
        super(TextWeatherParser, self).__init__()

    @property
    def exception(self) -> Exception:
        return FileNotFoundError(f"\"{self._source}\" is not found.")

    def validate_source(self, source: str) -> bool:
        self._source = source
        return source.endswith(".txt") and path.exists(source)

    def parse_weather(self, source: str) -> dict:
        valid_lines = self.get_valid_lines(source)
        # TODO: build a dictionary based on valid_lines
        return {}

    def get_valid_lines(self, source: str) -> list[list[str]]:
        """
        Read from the source all lines validates them and preprocess.

        :param source: filepath to the weather's data.
        :returns: list of all needed parameters for each valid line.
        """

        with open(source, 'r', encoding=self.__encoding) as file:
            lines = [valid_line for valid_line in
                     [[string.strip() for string in split(self.__delimiter, line) if string.strip() != ""]
                      for line in file.readlines()] if self.is_valid_line(valid_line)]

        return lines

    def is_valid_line(self, line: list[str]) -> bool:
        """
        Checks is line is valid.

        :param line: split by delimiter file line where all elements are stripped.
        :returns: True - if line contains 6 parameters, and it matches the format.
        """

        return len(line) == 6 and all([pattern.match(target) for pattern, target in zip(self.__formats, line[1:])])
# endregion


def main():
    txt = TextWeatherParser()
    txt.parse("input.txt")


if __name__ == "__main__":
    main()
