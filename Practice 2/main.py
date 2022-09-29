from datetime import datetime
from abc import ABC, abstractmethod
from os import path, getcwd
from re import split, compile


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

    class TextLineError:
        """
        Information about invalid lines in the text file.
        """

        def __init__(self, position: int, line: list[str]):
            """
            Creates instance of the TextLineError.

            :param position: position of the line in the file.
            :param line: value of the line.
            """

            self.position = position
            self.line = line

        def __str__(self):
            return f"Line \"{' '.join(self.line)}\" at position {self.position} is invalid."

    def __init__(self):
        """
        Creates TextWeatherParser with all needed format validators.
        """

        self.__date_format = compile(r"(\d{2}[/.]\d{2}[/.]\d{4})|(today)")
        self.__time_format = compile(r"\d{1,2}:\d{2}")
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

        for line in valid_lines:
            city, date, time, temp, press, wind = line
            if city not in self.weather:
                self.weather[city] = {}
            if date not in self.weather[city]:
                self.weather[city][date] = {}

            self.weather[city][date][time] = [int(temp) if temp != 'none' else 'none',
                                              int(press) if press != 'none' else 'none',
                                              wind]
        return self.weather

    def get_valid_lines(self, source: str) -> list[list[str]]:
        """
        Read from the source all lines validates them and preprocess.

        :param source: filepath to the weather's data.
        :returns: list of all needed parameters for each valid line.
        """

        with open(source, 'r', encoding=self.__encoding) as file:
            lines = [[string.strip() for string in split(self.__delimiter, line) if string.strip() != ""]
                     for line in file.readlines()]

        line_errors = [self.TextLineError(position, line)
                       for (position, line) in enumerate(lines, start=1)
                       if not self.is_valid_line(line)]

        for error in line_errors:
            lines.remove(error.line)

        to_save = [str(not_empty) for not_empty in line_errors if not_empty.line]
        if to_save:
            self.save('\n'.join(to_save))

        return lines

    def is_valid_line(self, line: list[str]) -> bool:
        """
        Checks is line is valid.

        :param line: split by delimiter file line where all elements are stripped.
        :returns: True - if line contains 6 parameters, and it matches the format.
        """

        return len(line) == 6 and all([pattern.match(target) for pattern, target in zip(self.__formats, line[1:])])

    def save(self, validation_errors):
        """
        Saves errors data to debug.

        :param validation_errors: errors to debug.
        """

        file_to_save = f"{getcwd()}\\Errors" + \
                       f"_{datetime.now().strftime('%Y_%d_%m_%H_%M_%S')}.txt"
        with open(file_to_save, 'w+', encoding=self.__encoding) as file:
            file.write(validation_errors)


# endregion


# region Operations


class WeatherOperator:
    """
    Provides access to the weather database based on the dictionary.
    """

    HISTORY = ""
    CITY = 0
    DATE = 1
    TIME = 2
    TEMPERATURE = 3
    PRESSURE = 4
    WIND = 5
    RESPONSE_SEPARATOR = '\n' + "=" * 50 + '\n'
    CITY_NOT_FOUND = "There is no such city: {0}."
    CITY_DATE_NOT_FOUND = "There is no info about {0} for {1}"
    DEFAULT_FORMAT = "|{0:<12}|{1:^8}|{2:^6}|{3:^8}|{4:^4}|"

    @staticmethod
    def tracker(func):
        """
        Decorator to store save all invocation data and print it.

        :param func: function to decorate.
        """
        def inner(*args):
            """
            Invokes function and save needed data about it.

            :params args: argument of the func.
            """

            response = f"Response for: {func.__name__}({','.join([str(arg) for arg in args[1:]])})\n" \
                       + str(func(*args)) \
                       + WeatherOperator.RESPONSE_SEPARATOR
            print(response)
            WeatherOperator.HISTORY += response

        return inner

    def __init__(self, weather: dict):
        """
        Creates WeatherOperator instance the database dictionary.

        :param weather: weather as dictionary.
        """

        self.weather = weather

    def to_list(self):
        """
        Converts value from the dictionary to the list.

        :returns: list of tuples of (city, date, time, temperature, pressure, wind).
        """

        return [(city, date, time, self.weather[city][date][time][0],
                 self.weather[city][date][time][1],
                 self.weather[city][date][time][2])
                for city in self.weather
                for date in self.weather[city] for time in self.weather[city][date]]

    @tracker
    def format_city(self, city: str, city_format: str = None) -> str:
        """
        Returns weather data for the city in the set format.

        :param city: city to get info about.
        :param city_format: format to display data.
        :returns: information about city in format - if city exists in db. Else - city not found response.
        """

        validated_format = city_format if city_format else self.DEFAULT_FORMAT
        return self.CITY_NOT_FOUND.format(city) if city not in self.weather \
            else '\n'.join([str(validated_format.format(date, time,
                                                        self.weather[city][date][time][0],
                                                        self.weather[city][date][time][1],
                                                        self.weather[city][date][time][2]))
                            for date in self.weather[city]
                            for time in self.weather[city][date]])

    @tracker
    def max_temperature(self) -> str:
        """
        Finds name of the city where the temperature is the highest.

        :returns: name of the city where were the highest temperature.
        """

        temperatures = self.to_list()
        return max(temperatures, key=lambda temp: temp[self.TEMPERATURE])[self.CITY]

    @tracker
    def min_temperature(self) -> str:
        """
        Finds name of the city where the temperature is the lowest.

        :returns: name of the city where were the highest lowest.
        """

        temperatures = self.to_list()
        return min(temperatures, key=lambda temp: temp[self.TEMPERATURE])[self.CITY]

    @tracker
    def changes(self, city: str, date: str) -> str:
        """
        Finds all data about temperature changes for the concrete city at the concrete date.

        :returns: all temperature for that date.
        """

        return self.CITY_DATE_NOT_FOUND.format(city, date) \
            if city not in self.weather or date not in self.weather[city] \
            else ', '.join([str(item[self.TEMPERATURE]) for item in self.to_list()
                            if item[self.CITY] == city and item[self.DATE] == date])

    @tracker
    def domain_wind(self, *cities) -> str:
        """
        Defines the domain wind for all cities.

        :params: cites: all cities to get wind info from.
        :returns: value of the wind direction. (One of the symbols: N or NE or E or SE or S or SW or W or NW)
        """

        for city in cities:
            if city not in self.weather:
                return self.CITY_NOT_FOUND.format(city)
        winds = [item[self.WIND] for item in self.to_list() if item[self.CITY] in cities]
        winds_as_dict = {wind: winds.count(wind) for wind in set(winds)}
        return max(winds_as_dict, key=winds_as_dict.get)

    @tracker
    def filter_temp(self, predicate) -> str:
        """
        Returns all records in the default format for records, where temperature is valid due to the predicate.

        :returns: formatted valid records.
        """

        return '\n'.join([self.DEFAULT_FORMAT.format(item[self.CITY],
                                                     item[self.DATE],
                                                     item[self.TIME],
                                                     item[self.TEMPERATURE],
                                                     item[self.PRESSURE],
                                                     item[self.WIND])
                          for item in self.to_list() if item[self.TEMPERATURE] != 'none' and
                          predicate(item[self.TEMPERATURE])])

    def save_session(self):
        """
        Saves all the request's history if it is not empty.
        """

        if not self.HISTORY:
            return
        file_to_save = f"{getcwd()}\\weather_response" + \
                       f"_{datetime.now().strftime('%Y_%d_%m_%H_%M_%S')}.txt"
        with open(file_to_save, 'w+', encoding="utf-8") as file:
            file.write(self.HISTORY)


# endregion


def main():
    wo = WeatherOperator(TextWeatherParser().parse_weather("input.txt"))
    wo.format_city("Стрий", "{0}, {1}, {2}, {3}, {4}")
    wo.format_city("Сколе")
    wo.format_city("С")
    wo.max_temperature()
    wo.min_temperature()
    wo.changes("Львів", "01.10.2022")
    wo.changes("Львів", "29.10.2022")
    wo.changes("Сколе", "30.09.2022")
    wo.domain_wind("Стрий", "Львів")
    wo.domain_wind("Сколе")
    wo.domain_wind("Стрий", "Львів", "Золочів")
    wo.filter_temp(lambda temp: temp > 15)
    wo.save_session()


if __name__ == "__main__":
    main()
