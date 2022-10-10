from abc import ABC
from tkinter import Tk, Frame, Listbox, Variable, Label
from tkinter.ttk import Combobox


class Alphabet:
    """
    Represents ukrainian alphabet.

    LETTERS: all ukrainian letters in the alphabetic order.
    """
    LETTERS = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'

    @staticmethod
    def as_position_list(word: str) -> list[int]:
        """
        Converts word to the list of the integers, that represents position in the alphabet.

        :param word: word to convert to the list of the integers.
        :returns: list of the integers:
        [0, 32] - if letter is in alphabet; -1 - otherwise.
        """
        return [Alphabet.LETTERS.index(letter.lower()) if letter.lower() in Alphabet.LETTERS else -1 for letter in word]


class PublicTransport(ABC):
    """
    Represents unit of the public transport.

    TRAM_TRANSPORT_TYPE - tram public transport type.
    TROLLEYBUS_TRANSPORT_TYPE - trolleybus public transport type.
    """

    TRAM_TRANSPORT_TYPE = "Трамвай"
    TROLLEYBUS_TRANSPORT_TYPE = "Тролейбус"

    STATION_NOT_FOUND = "Станції {0} нема для {1}"
    SIT_ON_STATION = "Сідайте на зупинці {0} на {1}. "
    DIFFERENT_ROUTE_WAY = SIT_ON_STATION + "Доїдьте до кінцевої {2} та на зворотньому шляху вийдіть на {3}"
    ROUTE_CONNECTION_TEXT = SIT_ON_STATION + "Проїдьте {2} зупин{3} та виходіть на станції {4}"
    STATION_DIFFERENCE = "Між станціями {0} та {1} є {2} зупин{3}."

    ENDINGS = {tuple([1]): "у", (2, 3, 4): "ки", (0, 5, 6, 7, 8, 9): "ок"}

    def __init__(self):
        """
        Creates instance of the public transport.

        transport_number - number of the public transport.
        forward_way - order of the stations in the forward way.
        backward_way - order of the stations in the backward way.
        __forward_way_set - set of the stations of the forward way.
        __backward_way_set - set of the stations of the backward way.
        __all_stations - all stations from the forward and backward ways.
        """

        self.transport_number = -1
        self.forward_way = []
        self.backward_way = []
        self.__forward_way_set = set()
        self.__backward_way_set = set()
        self.__all_stations = set()

    def __str__(self):
        """
        Represents public transport as string.

        :returns: public transport's type and number.
        """
        return f'{self.type} №{self.transport_number}'

    @property
    def forward_set(self):
        """
        Provide access to the __forward_way_set.
        Generate it if __forward_way_set is empty basing on the forward_way field.

        :returns: set of the forward_way stations.
        """
        if not self.__forward_way_set:
            self.__forward_way_set = set(self.forward_way)
        return self.__forward_way_set

    @property
    def backward_set(self):
        """
        Provide access to the __backward_way_set.
        Generate it if __backward_way_set is empty basing on the backward_way field.

        :returns: set of the backward_way stations.
        """
        if not self.__backward_way_set:
            self.__backward_way_set = set(self.backward_way)
        return self.__backward_way_set

    @property
    def all_stations(self):
        """
        Provide access to the __all_stations.
        Generate it if __all_stations is empty basing on the backward_way and forward_way fields.

        :returns:
        """
        if not self.__all_stations:
            self.__all_stations = self.backward_set | self.forward_set
        return self.__all_stations

    @property
    def type(self):
        """
        Defines a type of the public transport.

        :returns: TRAM_TRANSPORT_TYPE if instance name contains "Tram". TROLLEYBUS_TRANSPORT_TYPE - otherwise.
        """
        return self.TRAM_TRANSPORT_TYPE if "Tram" in repr(self) else self.TROLLEYBUS_TRANSPORT_TYPE

    @classmethod
    def define_ending(cls, station_difference: int) -> str:
        """
        Convert amount of the stations and ending for the word 'зупин(ок, ки, у)'.

        :param station_difference: amount of the stations between two another stations.
        :returns: ending of the word 'зупинка'. 'у' - if amount is 1, 'ки' - if amount is 2, 3 or 4, 'ок' otherwise.
        """
        return "ок" if 10 <= station_difference <= 20 else [value for key, value in cls.ENDINGS.items()
                                                            if station_difference % 10 in key][0]

    def common_station_with(self, another) -> list[str]:
        """
        Defines common stations between two public transports.

        :param another: another Public transport.
        :raise ValueError: another type must be PublicTransport.
        :returns: list of the common stations.
        """
        if not isinstance(another, PublicTransport):
            raise ValueError("Value another must be inherited from the PublicTransport class.")
        return list(self.forward_set & another.forward_set & self.backward_set & another.backward_set)

    def define_route(self, station_from: str, station_to: str) -> str:
        """
        Finds route from one station to another within his own route.

        :param station_from: station to find route from.
        :param station_to: station to find route to.
        :returns: STATION_NOT_FOUND - if station_from or station_to is not on his own route.
                  DIFFERENT_ROUTE_WAY - if station_from and station_to is on the different route-ways.
                  ROUTE_CONNECTION_TEXT - if station_from and station_to is on the same route-way.
        """
        if station_from not in self.all_stations:
            return self.STATION_NOT_FOUND.format(station_from, str(self))
        if station_to not in self.all_stations:
            return self.STATION_NOT_FOUND.format(station_to, str(self))

        if self.is_on_different_ways(station_from, station_to) != self.is_one_way(station_from, station_to):
            return self.different_route_way(station_from, station_to)

        difference = self.get_station_difference(station_from, station_to)
        return self.ROUTE_CONNECTION_TEXT.format(station_from, str(self),
                                                 difference,
                                                 self.define_ending(difference),
                                                 station_to)

    def get_station_difference(self, station_from: str, station_to: str) -> int:
        """
        Defines how many stations are between station_from and station_to.

        :param station_from: station to find route from.
        :param station_to: station to find route to.
        :returns: amount of the stations between station_from and station_to.
        """
        transport_direction = self.forward_way if station_from in self.forward_way and station_to in self.forward_way \
            else self.backward_way
        return abs(transport_direction.index(station_from) - transport_direction.index(station_to))

    def station_difference(self, station_from: str, station_to: str) -> str:
        """
        Format station difference between station_from and station_to.

        :param station_from: station to find route from.
        :param station_to: station to find route to.
        :returns: formatted text about amount of station between station_from and station_to.
        """

        station_difference = self.get_station_difference(station_from, station_to)
        return self.STATION_DIFFERENCE.format(station_from, station_to, station_difference,
                                              PublicTransport.define_ending(station_difference))

    def different_route_way(self, station_from: str, station_to: str) -> str:
        """
        Defines route for station_from and station_to in case they are on different route-ways.

        :param station_from: station to find route from.
        :param station_to: station to find route to.
        :returns: formatted text of the route between station_from and station_to.
        """
        return self.DIFFERENT_ROUTE_WAY.format(station_from, str(self), self.forward_way[-1], station_to) \
            if station_from in self.forward_way and station_to in self.backward_way else \
            self.DIFFERENT_ROUTE_WAY.format(station_from, str(self), self.backward_way[-1], station_to)

    def is_one_way(self, station_from: str, station_to: str):
        """
        Defines if station_from and station_to on the same route_way.

        :param station_from: station to find route from.
        :param station_to: station to find route to.
        :returns: True - if station_from and station_to is on the same route_way, false otherwise.
        """

        return station_from in self.forward_way and station_to in self.forward_way or \
               station_from in self.backward_way and station_to in self.backward_way

    def is_on_different_ways(self, station_from: str, station_to: str) -> bool:
        """
        Defines if station_from or station two is on different route-ways.

        :param station_from: station to find route from.
        :param station_to: station to find route to.
        :returns: True - of station_from and station_to is on different route-ways. False - otherwise
        """

        return station_from in self.forward_way and station_to in self.backward_way or \
               station_from in self.backward_way and station_to in self.forward_way


class TramOne(PublicTransport):
    def __init__(self):
        super().__init__()
        self.transport_number = 1
        self.forward_way = [
            "Залізничний вокзал",
            "Приміський вокзал",
            "Площа Кропивницького",
            "Вулиця Карпінського",
            "Львівська політехніка",
            "Головна Пошта",
            "Вулиця Петра Дорошенка",
            "Площа Ринок",
            "Вулиця Руська",
            "Площа Митна",
            "Військовий госпіталь",
            "Медичний університет",
            "Вулиця Мечникова",
            "Личаківський цвинтар",
            "Обласна інфекційна лікарня",
            "Вулиця Левицького",
            "Погулянка"
        ]
        self.backward_way = [
            "Погулянка",
            "Вулиця Левицького",
            "Личаківський цвинтар",
            "Вулиця Мечникова",
            "Медичний університет",
            "Військовий госпіталь",
            "Площа Митна",
            "Вулиця Підвальна",
            "Вулиця Театральна",
            "ТЦ \"Магнус\"",
            "Церква святої Анни",
            "Захисників України",
            "Площа Кропивницького",
            "Приміський вокзал",
            "Приміський вокзал",
            "Залізничний вокзал"
        ]


class TramTwo(PublicTransport):
    def __init__(self):
        super(TramTwo, self).__init__()
        self.transport_number = 2
        self.forward_way = [
            "Вулиця Пасічна",
            "Вулиця Богдана Котика",
            "Вулиця Мечникова",
            "Медичний університет",
            "Військовий госпіталь",
            "Площа Митна",
            "Вулиця Володимира Шухевича",
            "Вулиця Саксаганського",
            "Площа Івана Франка",
            "Парк культури",
            "Вулиця Академіка Сахарова",
            "Вулиця Київська",
            "Фабрика Левинського",
            "Вулиця Мельника",
            "Вулиця Максима Залізняка",
            "Вулиця Гординських",
            "Вулиця Коновальці (Музей Труша)"
        ]
        self.backward_way = [
            "Вулиця Коновальці (Музей Труша)",
            "Вулиця Гординських",
            "Вулиця Максима Залізняка",
            "Вулиця Мельника",
            "Фабрика Левинського",
            "Вулиця Київська",
            "Львівська політехніка",
            "Головна Пошта",
            "Вулиця Петра Дорошенка",
            "Площа Ринок",
            "Вулиця Руська",
            "Площа Митна",
            "Військовий госпіталь",
            "Медичний університет",
            "Вулиця Мечникова",
            "Вулиця Богдана Котика",
            "Вулиця Пасічна"
        ]


class TramThree(PublicTransport):
    def __init__(self):
        super().__init__()
        self.transport_number = 3
        self.forward_way = [
            "Площа Соборна",
            "Вулиця Володимира Шухевича",
            "Вулиця Саксаганського",
            "Площа Івана Франка",
            "Парк культури",
            "Вулиця Академіка Сахарова",
            "Вулиця Івана Горбачевського",
            "Вулиця Шумського",
            "Вулиця Аркаса",
            "Вулиця Бойчука (Кіноцентр)",
            "Аквапарк"
        ]
        self.backward_way = [
            "Аквапарк",
            "Вулиця Бойчука (Кіноцентр)",
            "Вулиця Аркаса",
            "Вулиця Шумського",
            "Вулиця Івана Горбачевського",
            "Вулиця Академіка Сахарова",
            "Парк культури",
            "Площа Івана Франка",
            "Вулиця Саксаганського",
            "Площа Соборна"
        ]


class TramFour(PublicTransport):
    def __init__(self):
        super().__init__()
        self.transport_number = 4
        self.forward_way = [
            "Залізничний вокзал",
            "Приміський вокзал",
            "Площа Кропивницького",
            "Вулиця Бандери",
            "Вулиця Київська",
            "Вулиця Академіка Сахарова",
            "Парк культури",
            "Площа Івана Франка",
            "Стрийський Парк",
            "Академія Мистецтв",
            "Стадіон \"Україна\"",
            "Вулиця Угорська",
            "ТРЦ \"Шувар\"",
            "Дитяча поліклініка",
            "Центр Довженка",
            "Поліклініка №4",
            "Вулиця Коломийська",
            "Санта Барбара",
            "Вулиця Вернадського"
        ]
        self.backward_way = [
            "Вулиця Вернадського",
            "Санта Барбара",
            "Вулиця Коломийська",
            "Поліклініка №4",
            "Центр Довженка",
            "Дитяча поліклініка",
            "ТРЦ \"Шувар\"",
            "Вулиця Угорська",
            "Стадіон \"Україна\"",
            "Академія Мистецтв",
            "Стрийський Парк",
            "Стрийський ринок",
            "Парк культури",
            "Вулиця Академіка Сахарова",
            "Вулиця Київська",
            "Вулиця Бандери",
            "Площа Кропивницького",
            "Приміський вокзал",
            "Залізничний вокзал"
        ]


class TramSix(PublicTransport):
    def __init__(self):
        super().__init__()
        self.transport_number = 6
        self.forward_way = [
            "Вулиця Миколайчука",
            "Фабрика \"Світанок\"",
            "Трамвайне депо №2",
            "Вулиця Промислова",
            "Вулиця Якова Остряниці",
            "Станція Підзамче",
            "Вулиця Гайдамацька",
            "Палац культури імені Гната Хоткевича",
            "Площа Старий Ринок",
            "Вулиця Театральна",
            "ТЦ \"Магнус\"",
            "Церква святої Анни",
            "Захисників України",
            "Площа Кропивницького",
            "Приміський вокзал",
            "Залізничний вокзал"
        ]
        self.backward_way = [
            "Залізничний вокзал",
            "Приміський вокзал",
            "Площа Кропивницького",
            "Церква святої Анни",
            "Вулиця Северина Наливайка",
            "Площа Старий Ринок",
            "Вулиця Під Дубом",
            "Палац культури імені Гната Хоткевича",
            "Станція Підзамче",
            "Вулиця Якова Остряниці",
            "Вулиця Промислова",
            "Трамвайне депо №2",
            "Фабрика \"Світанок\"",
            "Вулиця Липинського",
            "Вулиця Миколайчука"
        ]


class TramEight(PublicTransport):
    def __init__(self):
        super().__init__()
        self.transport_number = 8
        self.forward_way = [
            "Площа Соборна",
            "Вулиця Володимира Шухевича",
            "Вулиця Саксаганського",
            "Площа Івана Франка",
            "Стрийський Парк",
            "Академія Мистецтв",
            "Стадіон \"Україна\"",
            "Вулиця Угорська",
            "ТРЦ \"Шувар\"",
            "Дитяча поліклініка",
            "Центр Довженка",
            "Поліклініка №4",
            "Вулиця Коломийська",
            "Санта Барбара",
            "Вулиця Вернадського"
        ]
        self.backward_way = [
            "Вулиця Вернадського",
            "Санта Барбара",
            "Вулиця Коломийська",
            "Поліклініка №4",
            "Центр Довженка",
            "Дитяча поліклініка",
            "ТРЦ \"Шувар\"",
            "Вулиця Угорська",
            "Стадіон \"Україна\"",
            "Академія Мистецтв",
            "Стрийський Парк",
            "Стрийський ринок",
            "Вулиця Саксаганського",
            "Площа Соборна"
        ]


class TramNine(PublicTransport):
    def __init__(self):
        super().__init__()
        self.transport_number = 9
        self.forward_way = [
            "Залізничний вокзал",
            "Приміський вокзал",
            "Площа Кропивницького",
            "Вулиця Бандери",
            "Вулиця Київська",
            "Вулиця Академіка Сахарова",
            "Парк культури",
            "Площа Івана Франка",
            "Вулиця Саксаганського",
            "Вулиця Володимира Шухевича",
            "Вулиця Підвальна",
            "Площа Старий Ринок",
            "Вулиця Під Дубом",
            "Палац культури імені Гната Хоткевича",
            "Вулиця Гайдамацька",
            "Вулиця Городоцька",
            "Вулиця Торф'яна"
        ]
        self.backward_way = [
            "Вулиця Торф'яна",
            "Вулиця Городоцька",
            "Вулиця Гайдамацька",
            "Палац культури імені Гната Хоткевича",
            "Площа Старий Ринок",
            "Театр Ляльок",
            "Вулиця Підвальна",
            "Вулиця Володимира Шухевича",
            "Вулиця Саксаганського",
            "Площа Івана Франка",
            "Парк культури",
            "Вулиця Академіка Сахарова",
            "Вулиця Київська",
            "Вулиця Бандери",
            "Площа Кропивницького",
            "Приміський вокзал",
            "Залізничний вокзал"
        ]


class TrolleybusTwentyTwo(PublicTransport):
    def __init__(self):
        super().__init__()
        self.transport_number = 22
        self.forward_way = [
            "Університет",
            "Собор Святого Юра",
            "Вулиця Степана Бандери",
            "Вулиця Липнева",
            "Вулиця Смаль-Стоцького",
            "Вулиця Копистинського",
            "Вулиця Антоновича",
            "Кульпарків",
            "Скнилівок",
            "Вулиця Щирецька",
            "Вулиця Наукова",
            "Вулиця Василя Симоненка",
            "Клуб \"Науковий\"",
            "Центр зайнятості",
            "Вулиця Княгині Ольги",
            "Вулиця Тролейбусна",
            "Вулиця Академіка Підстригача",
            "Вулиця Стрийська-Наукова",
            "Вулиця Скорини",
            "Вулиця Ярослава Гашека",
            "Вулиця Михайла Максимовича",
            "Автовокзал"
        ]
        self.backward_way = [
            "Автовокзал",
            "Вулиця Михайла Максимовича",
            "Вулиця Ярослава Гашека",
            "Вулиця Скорини",
            "Вулиця Стрийська-Наукова",
            "Вулиця Академіка Підстригача",
            "Вулиця Тролейбусна",
            "Вулиця Княгині Ольги",
            "Центр зайнятості",
            "Клуб \"Науковий\"",
            "Вулиця Василя Симоненка",
            "Вулиця Щирецька",
            "Скнилівок",
            "Кульпарків",
            "Вулиця Антоновича",
            "Вулиця Максима Залізняка",
            "Вулиця Мельника",
            "Вулиця Степана Бандери",
            "Собор Святого Юра",
            "Вулиця Устияновича",
            "Університет"
        ]


class TrolleybusTwentyThree(PublicTransport):
    def __init__(self):
        super().__init__()
        self.transport_number = 23
        self.forward_way = [
            "Автовокзал",
            "Вулиця Михайла Максимовича",
            "Вулиця Ярослава Гашека",
            "Вулиця Скорини",
            "Вулиця Стрийська-Наукова",
            "Боднарівка",
            "Вулиця Івана Рубчака",
            "Тролейбусне депо",
            "Вулиця Володимира Великого",
            "Універмаг \"Океан\"",
            "Вулиця Боткіна",
            "Скнилівок",
            "Ринок \"Південний\"",
            "Вулиця Кульчицької",
            "Вулиця Любінська-Виговського",
            "Залізнична райадміністрація",
            "Вулиця Патона",
            "Лорта",
            "Вулиця Ряшківська"
        ]
        self.backward_way = list(reversed(self.forward_way.copy()))


class TrolleybusTwentyFour(PublicTransport):
    def __init__(self):
        super().__init__()
        self.transport_number = 24
        self.forward_way = [
            "Вулиця Шота Руставелі",
            "Вулиця Вагилевича",
            "Львівводоканал",
            "Вулиця Водогінна",
            "Вулиця Керченська",
            "Вулиця Липова Алея",
            "Вулиця Дністерська",
            "Фрезерний завод",
            "Автостанція №5",
            "ДБК",
            "Вулиця Зубрівська",
            "Вулиця Сихівська",
            "Вулиця Івана Кавалерідзе",
            "Центр Довженка",
            "Сихівська Райадміністрація",
            "Вулиця Коломийська",
            "Санта Барбара"
        ]
        self.backward_way = [
            "Санта Барбара",
            "Вулиця Коломийська",
            "Поліклініка №4",
            "Центр Дорошенка",
            "Вулиця Івана Кавалерідзе",
            "Вулиця Сихівська",
            "Вулиця Зубрівська",
            "ДБК",
            "Фрезерний завод",
            "Вулиця Бузкова",
            "Вулиця Дністерська",
            "Вулиця Липова алея",
            "Вулиця Керченська",
            "Вулиця Водогінна",
            "Львівводоканал",
            "Вулиця Вагилевича",
            "Вулиця Шота Руставелі"
        ]


class TrolleybusTwentyFive(PublicTransport):
    def __init__(self):
        super().__init__()
        self.transport_number = 25
        self.forward_way = [
            "Автовокзал",
            "Вулиця Михайла Максимовича",
            "Вулиця Ярослава Гашека",
            "Вулиця Скорини",
            "Вулиця Стрийська-Наукова",
            "Автобусний завод",
            "Податкова",
            "Дитяча залізниця",
            "Академія сухопутних військ",
            "Стрийський ринок",
            "Вулиця Шота Руставелі"
        ]
        self.backward_way = list(reversed(self.forward_way.copy()))


class TrolleybusTwentySeven(PublicTransport):
    def __init__(self):
        super().__init__()
        self.transport_number = 27
        self.forward_way = [
            "Університет",
            "Собор Святого Юра",
            "Площа Кропивницького",
            "Привокзальний ринок",
            "ТРЦ \"Скриня\"",
            "Вулиця Кульпарківська",
            "Вулиця Народна",
            "Богданівка",
            "Мотозавод",
            "Вулиця Вівсяна",
            "Вулиця Вільхова",
            "Вулиця Каховська",
            "Станція Скнилів"
        ]
        self.backward_way = [
            "Станція Скнилів",
            "Вулиця Авіаційна",
            "Вулиця Каховська",
            "Вулиця Вільхова",
            "Вулиця Вівсяна",
            "Мотозавод",
            "Богданівка",
            "Вулиця Народна",
            "Вулиця Кульпарківська",
            "ТРЦ \"Скриня\"",
            "Привокзальний Ринок",
            "Вулиця Тобілевича",
            "Площа Кропивницького",
            "Собор Святого Юра",
            "Вулиця Устияновича",
            "Університет"
        ]


class TrolleybusThirty(PublicTransport):
    def __init__(self):
        super().__init__()
        self.transport_number = 30
        self.forward_way = [
            "Університет",
            "Собор Святого Юра",
            "Вулиця Степана Бандери",
            "Вулиця Липнева",
            "Вулиця Смаль-Стоцького",
            "Вулиця Копистинського",
            "Стадіон \"Сільмаш\"",
            "Вулиця Окружна",
            "Будинок Меблів",
            "Вулиця Караджича",
            "Залізнична райадміністрація",
            "Вулиця Патона",
            "Лорта",
            "Вулиця Ряшківська"
        ]
        self.backward_way = [
            "Вулиця Ряшківська",
            "Лорта",
            "Вулиця Патона",
            "Залізнична райадміністрація",
            "Вулиця Любінська-Виговського",
            "Вулиця Караджича",
            "Будинок Меблів",
            "Вулиця Окружна",
            "Вулиця Антоновича",
            "Вулиця Максима Залізняка",
            "Вулиця Мельника",
            "Вулиця Степана Бандери",
            "Собор Святого Юра",
            "Вулиця Устияновича",
            "Університет"
        ]


class TrolleybusThirtyOne(PublicTransport):
    def __init__(self):
        super().__init__()
        self.transport_number = 31
        self.forward_way = [
            "Вулиця Шота Руставелі",
            "Вулиця Вагилевича",
            "Львівводоканал",
            "Вулиця Водогінна",
            "Вулиця Керченська",
            "Вулиця Липова алея",
            "Вулиця Дністерська",
            "Фрезерний завод",
            "Автостанція №5",
            "ДБК",
            "Вулиця Зубрівська",
            "Вулиця Вулецька",
            "м/н Старий Сихів",
            "Село Пасіки-Зубрицькі",
            "Сихівський Цвинтар",
            "Село Пасіки-Зубрицькі",
            "Пульмонологічний центр"
        ]
        self.backward_way = [
            "Пульмонологічний центр",
            "Село Пасіки-Зубрицькі",
            "Станція Сихів",
            "м/н Старий Сихів",
            "Вулиця Вулецька",
            "Вулиця Сихівська",
            "Вулиця Зубрівська",
            "ДБК",
            "Фрезерний завод",
            "Вулиця Бузкова",
            "Вулиця Дністерська",
            "Вулиця Липова алея",
            "Вулиця Керченська",
            "Вулиця Водогінна",
            "Львівводоканал",
            "Вулиця Вагилевича",
            "Вулиця Шота Руставелі"
        ]


class TrolleybusThirtyTwo(PublicTransport):
    def __init__(self):
        super().__init__()
        self.transport_number = 32
        self.forward_way = [
            "Університет",
            "Собор Святого Юра",
            "Площа Кропивницького",
            "Привокзальний ринок",
            "ТРЦ \"Скриня\"",
            "Вулиця Народна",
            "Вулиця Сяйво",
            "Вулиця Широка",
            "Вулиця Низинна",
            "Вулиця Гніздовського",
            "Поліклініка №3",
            "Вулиця Суботівська"
        ]
        self.backward_way = [
            "Вулиця Суботівська",
            "Поліклініка №3",
            "Вулиця Гніздовського",
            "Вулиця Низинна",
            "Вулиця Широка",
            "Вулиця Сяйво",
            "Вулиця Народна",
            "Вулиця Кульпарківська",
            "ТРЦ \"Скриня\"",
            "Привокзальний ринок",
            "Вулиця Тобілевича",
            "Площа Кропивницького",
            "Собор Святого Юра",
            "Вулиця Устияновича",
            "Університет"
        ]


class TrolleybusThirtyThree(PublicTransport):
    def __init__(self):
        super().__init__()
        self.transport_number = 33
        self.forward_way = [
            "Площа Івана Підкови",
            "Проспект В'ячеслава Чорновола",
            "Палац культури імені Гната Хоткевича",
            "Вулиця Хімічна",
            "Шевченківська райадміністрація",
            "Парк 700-річчя Львова",
            "Вулиця Варшавська",
            "Голоско",
            "Вулиця Гетьмана Мазепи",
            "Вулиця Пилипа Орлика",
            "Лікарня швидкої допомоги",
            "Вулиця Плугова",
            "Вулиця Грінченка"
        ]
        self.backward_way = [
            "Вулиця Грінченка",
            "Вулиця Плугова",
            "Лікарня швидкої допомоги",
            "Вулиця Пилипа Орлика",
            "Вулиця Гетьмана Мазепи",
            "Замарстинів",
            "Голоско",
            "Вулиця Варшавська",
            "Парк 700-річчя Львова",
            "Шевченківська райадміністрація",
            "Вулиця Хімічна",
            "Вулиця Пантелеймона Куліша",
            "Проспект В'ячеслава Чорновола",
            "Театр опери та балету",
            "Площа Івана Підкови"
        ]


class TrolleybusThirtyEight(PublicTransport):
    def __init__(self):
        super().__init__()
        self.transport_number = 38
        self.forward_way = [
            "Вулиця Хуторівка",
            "Вулиця Чукаріна",
            "Духовна семінарія",
            "Вулиця Демнянська",
            "Вулиця Стрийська-Наукова",
            "Боднарівка",
            "Вулиця Івана Рубчака",
            "Тролейбусне депо",
            "Вулиця Володимира Великого",
            "Універмаг \"Океан\"",
            "Вулиця Ботніка",
            "Скнилівок",
            "Кульпарків",
            "Кардіологічний центр",
            "ТРЦ \"Скриня\"",
            "Привокзальний ринок",
            "Вулиця Тобілевича",
            "Площа Кропивницького"
        ]

        self.backward_way = [
            "Площа Кропивницького",
            "Привокзальний ринок",
            "ТРЦ \"Скриня\"",
            "Вулиця Кульпарківська",
            "Кардіологічний центр",
            "Вулиця Антоновича",
            "Кульпарків",
            "Скнилівок",
            "Вулиця Ботніка",
            "Універмаг \"Океан\"",
            "Вулиця Володимира Великого",
            "Тролейбусне депо",
            "Вулиця Івана Рубчака",
            "Боднарівка",
            "Вулиця Стрийська-Наукова",
            "Вулиця Демнянська",
            "Духовна семінарія",
            "Вулиця Чукаріна",
            "Вулиця Хуторівка"
        ]


class RouteManager:
    """
    Represents manager of the public transport.
    Provides access to the operations on the available public transport.
    """

    STATION_NOT_FOUND = "Станцію {0} в базі не знайдено!"
    GOES_THROUGH_STATION = "Через станцію {0} проходить {1} транспорт{2}:\n\t{3}"

    ENDINGS = {tuple([1]): "ний засіб", (2, 3, 4): "ні засоби", (5, 6, 7, 8, 9, 0): "их засобів"}

    def __init__(self):
        """
        Initiates RoutManager.

        public_transport - list of the all available public transports.
        all_stations - list of the all stations, based on public_transport list
                     - unique, sorted in alphabetical order.
        all_transport_numbers - list of all the public transports rout numbers.
        station_cross - dictionary of the common stations between all public transports.
        transports - list of the string representations of the public transport list.
        """
        self.public_transport = [
            TramOne(),
            TramTwo(),
            TramThree(),
            TramFour(),
            TramSix(),
            TramEight(),
            TramNine(),
            TrolleybusTwentyTwo(),
            TrolleybusTwentyThree(),
            TrolleybusTwentyFour(),
            TrolleybusTwentyFive(),
            TrolleybusTwentySeven(),
            TrolleybusThirty(),
            TrolleybusThirtyOne(),
            TrolleybusThirtyTwo(),
            TrolleybusThirtyThree(),
            TrolleybusThirtyEight()
        ]
        self.all_stations = sorted(list(set.union(*[transport.all_stations for transport in self.public_transport])),
                                   key=Alphabet.as_position_list)
        self.all_transport_numbers = [transport.transport_number for transport in self.public_transport]
        self.station_cross = [{(self.public_transport[i].transport_number, self.public_transport[j].transport_number):
                                   self.public_transport[i].common_station_with(self.public_transport[j])}
                              for i in range(len(self.public_transport)) for j in range(i, len(self.public_transport))
                              if i != j]
        self.transports = [str(transport) for transport in self.public_transport]

    @classmethod
    def same_transport_route(cls, station_from: str, station_to: str, routes: list[PublicTransport]) -> list[str]:
        """
        Gather information about route through station that connected with one public transport.

        :param station_from: station to find route from.
        :param station_to: station to find route to.
        :param routes: public transport that has route through station_from and station_to.
        :returns: string formats about routes.
        """
        return [route.define_route(station_from, station_to) for route in routes]

    def has_stop_in(self, station: str) -> list[PublicTransport]:
        """
        Finds all public transports that has route through the station.

        :param station: station to find routes going through.
        :returns: list of all public transports.
        """
        return [transport for transport in self.public_transport if station in transport.all_stations]

    def has_stops_in(self, *stations: str) -> list[list[PublicTransport]]:
        """
        Finds all public transports that goes thought stations.

        :param stations: stations to define is any public transport goes thought.
        :returns: list of lists of the public transports
        """
        return [self.has_stop_in(station) for station in stations]

    def find_route(self, station_from: str, station_to: str) -> str | list[str]:
        """
        Finds route from one station to another.

        :param station_from: station to find route from.
        :param station_to: station to find route to.
        """
        transport_at_station_from, transport_at_station_to = map(set, self.has_stops_in(station_from, station_to))
        if not transport_at_station_from:
            return self.STATION_NOT_FOUND.format(station_from)
        if not transport_at_station_to:
            return self.STATION_NOT_FOUND.format(station_to)

        common_public_transport = list(transport_at_station_from & transport_at_station_to)
        if common_public_transport:
            return self.same_transport_route(station_from, station_to, common_public_transport)

    def find_transport(self, transport_name: str) -> PublicTransport | None:
        """
        Finds transport info based on str representation of the PublicTransport.

        :param transport_name: name of the transport to find.
        :returns: PublicTransport - if there is any public transport with str representation as transport_name.
                  None - otherwise.
        """
        return next(filter(lambda transport: str(transport) == transport_name, self.public_transport), None)

    def find_transport_index(self, transport_name: str) -> int:
        """
        Finds index of the transport based on transport name.
        :param transport_name: name of the transport index to find.

        :returns: index of the public transport if it is in list, -1 otherwise.
        """
        return self.transports.index(transport_name) if transport_name in self.transports else -1

    def station_connect(self, station: str, transports: list[PublicTransport]) -> str:
        """
        Format information about amount of the public transport that goes through station.

        :param station: station to get information about.
        :param transports: list of transports that has a stop at the station.
        :returns: formatted information about the station.
        """
        return self.GOES_THROUGH_STATION.format(station,
                                                len(transports),
                                                self.define_ending(len(transports)),
                                                '\n\t'.join([str(transport) for transport in transports]))

    @classmethod
    def define_ending(cls, number: int):
        """
        Defines ending of the word 'транспорт'

        :param number: amount of the public transports that has a stop at the station.
        :returns: string value of the 'транспорт' word ending. "ний засіб" - if number equals 1,
         "ні засоби" - if number is equal to 2, 3 or 4, "их засобів" - otherwise.
        """
        return "ний засіб" if 10 <= number <= 20 else [value for key, value in cls.ENDINGS.items()
                                                       if number % 10 in key][0]


class RouteManagerWindow(Tk):
    """
    Interface of the module.

    WIDTH - window width.
    Height - window height.
    PARAMETER_FRAME_HEIGHT - height of the frame of the current request.
    FONT - font style of the app.
    BACKGROUND - color of the background.
    """
    WIDTH = 1280
    HEIGHT = 815
    PARAMETER_FRAME_HEIGHT = 900
    HALF_WIDTH = int(WIDTH * 0.032)
    FONT = ("Cascadia Code PL SemiLight", 21)
    BACKGROUND = "white"

    ROUTE_NOT_FOUND = "Маршрут між {0} та {1} зупинками не знайдено."

    def __init__(self):
        """
        Initiates window.

        route_manager - access to the information about the routes.
        """
        super(RouteManagerWindow, self).__init__()
        self.route_manager = RouteManager()
        self.title("Інформаційний довідник транспортних засобів")
        self.resizable(height=False, width=False)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.request_selector_frame = Frame(self)
        self.response_provider_frame = Frame(self)
        self.query_selector_combobox = Combobox()
        self.transport_listbox = Listbox()
        self.forward_way_listbox = Listbox()
        self.backward_way_listbox = Listbox()
        self.station_listbox = Listbox()
        self.transport_through_station_listbox = Listbox()
        self.station_from_listbox = Listbox()
        self.station_to_listbox = Listbox()
        self.transport_through_station_label = Label()
        self.route_result_label = Label()
        self.station_from_value = ""
        self.station_to_value = ""
        self.QUERY_FRAMES = {"Маршрут громадського транспорту": self.pack_transport,
                             "Які транспортні засоби зупиняються на станції": self.pack_stations,
                             "Знайти маршрут через зупинки": self.pack_routes}
        self.init_query_selection_frame()

    @staticmethod
    def get_listbox_item(box: Listbox):
        """
        Get information about selected item.

        :param box: Listbox to get information from.
        :returns: item at the selected index from the listbox.
        """
        indexes = box.curselection()
        return box.get(indexes[0]) if indexes else None

    def init_query_selection_frame(self) -> None:
        """
        Sets up combobox of the request selector.
        """
        self.request_selector_frame = Frame(self)
        self.query_selector_combobox = Combobox(self.request_selector_frame,
                                                values=list(self.QUERY_FRAMES.keys()),
                                                width=self.WIDTH,
                                                height=50,
                                                font=self.FONT,
                                                justify="center",
                                                state="readonly")
        self.query_selector_combobox.current(0)
        self.response_provider_frame = self.pack_transport()
        self.query_selector_combobox.bind("<<ComboboxSelected>>", self.on_combobox_selected)
        self.query_selector_combobox.pack()
        self.request_selector_frame.pack()
        self.response_provider_frame.pack()

    def pack_transport(self) -> Frame:
        """
        Generate frame for query 'Маршрут громадського транспорту'.

        :returns: frame of the route visualizers: forward and backward ways for concrete public transport.
        """
        frame = Frame(self,
                      bg=self.BACKGROUND,
                      height=self.PARAMETER_FRAME_HEIGHT,
                      width=self.WIDTH)

        left_frame = Frame(frame,
                           bg=self.BACKGROUND,
                           width=self.HALF_WIDTH)
        right_frame = Frame(frame,
                            bg=self.BACKGROUND,
                            width=self.HALF_WIDTH)

        self.transport_listbox = Listbox(frame,
                                         listvariable=Variable(value=self.route_manager.transports),
                                         font=self.FONT,
                                         bg=self.BACKGROUND,
                                         width=self.WIDTH,
                                         justify="center",
                                         height=7,
                                         selectmode="one")
        self.transport_listbox.bind("<<ListboxSelect>>", self.on_transport_selected)

        forward_way_label = Label(left_frame,
                                  width=self.HALF_WIDTH,
                                  text="Прямий маршрут",
                                  bg=self.BACKGROUND,
                                  font=self.FONT)
        backward_way_label = Label(right_frame,
                                   width=self.HALF_WIDTH,
                                   text="Зворотній маршрут",
                                   bg=self.BACKGROUND,
                                   font=self.FONT)

        self.forward_way_listbox = Listbox(left_frame,
                                           height=20,
                                           width=self.HALF_WIDTH,
                                           font=self.FONT,
                                           bg=self.BACKGROUND,
                                           justify="center")

        self.forward_way_listbox.bind("<<ListboxSelect>>", self.from_transport_to_station)

        self.backward_way_listbox = Listbox(right_frame,
                                            width=self.HALF_WIDTH,
                                            height=20,
                                            font=self.FONT,
                                            bg=self.BACKGROUND,
                                            justify="center")

        self.backward_way_listbox.bind("<<ListboxSelect>>", self.from_transport_to_station)

        self.transport_listbox.pack()
        left_frame.pack(side="left")
        right_frame.pack(side="right")
        forward_way_label.pack()
        backward_way_label.pack()
        self.forward_way_listbox.pack()
        self.backward_way_listbox.pack()

        return frame

    def pack_stations(self) -> Frame:
        """
        Generate frame for query 'Які транспортні засоби зупиняються на станції'.

        :returns: frame to display which public transport has a stop at the concrete station.
        """
        frame = Frame(self,
                      bg=self.BACKGROUND,
                      height=self.PARAMETER_FRAME_HEIGHT,
                      width=self.WIDTH)

        self.station_listbox = Listbox(frame,
                                       listvariable=Variable(value=self.route_manager.all_stations),
                                       width=self.HALF_WIDTH,
                                       height=20,
                                       font=self.FONT,
                                       bg=self.BACKGROUND,
                                       selectmode="one")

        self.transport_through_station_listbox = Listbox(frame,
                                                         width=self.HALF_WIDTH,
                                                         height=5,
                                                         font=self.FONT,
                                                         bg=self.BACKGROUND,
                                                         justify="center",
                                                         selectmode="one")
        self.transport_through_station_listbox.bind("<<ListboxSelect>>", self.from_station_to_transport)

        self.transport_through_station_label = Label(frame,
                                                     font=self.FONT,
                                                     height=15,
                                                     justify="left",
                                                     wraplength=500,
                                                     width=self.HALF_WIDTH,
                                                     bg=self.BACKGROUND)

        self.station_listbox.bind("<<ListboxSelect>>", self.on_station_selected)
        self.station_listbox.pack(side="left", expand=False)
        self.transport_through_station_listbox.pack()
        self.transport_through_station_label.pack(expand=True)
        return frame

    def pack_routes(self) -> Frame:
        """
        Generate frame for query 'Знайти маршрут через зупинки'.

        :returns: frame to display route from one station to another.
        """
        frame = Frame(self,
                      bg=self.BACKGROUND,
                      height=self.PARAMETER_FRAME_HEIGHT,
                      width=self.WIDTH)

        self.station_from_listbox = Listbox(frame,
                                            listvariable=Variable(value=self.route_manager.all_stations),
                                            height=15,
                                            width=self.HALF_WIDTH,
                                            font=self.FONT,
                                            bg=self.BACKGROUND)

        self.station_from_listbox.bind("<<ListboxSelect>>", self.on_station_from_selected)
        self.station_from_listbox.configure(exportselection=False)
        self.station_to_listbox = Listbox(frame,
                                          listvariable=Variable(value=self.route_manager.all_stations),
                                          width=self.HALF_WIDTH,
                                          height=15,
                                          font=self.FONT,
                                          bg=self.BACKGROUND,
                                          justify="right")

        self.station_to_listbox.bind("<<ListboxSelect>>", self.on_station_to_selected)
        self.station_to_listbox.configure(exportselection=False)
        self.route_result_label = Label(frame,
                                        font=self.FONT,
                                        width=self.WIDTH,
                                        wraplength=self.WIDTH)

        self.route_result_label.pack(side="bottom", expand=True)
        self.station_to_listbox.pack(side="right")
        self.station_from_listbox.pack(side="left")

        return frame

    def on_combobox_selected(self, _):
        """
        Combobox selected event handler.
        Changes frame for current query.
        """
        self.response_provider_frame.pack_forget()
        self.response_provider_frame = self.QUERY_FRAMES[self.query_selector_combobox.get()]()
        self.response_provider_frame.pack()

    def on_transport_selected(self, _):
        """
        Transport selected in the listbox event handler.
        Update information about forward and backward ways.
        """
        route = self.route_manager.find_transport(self.get_listbox_item(self.transport_listbox))
        if not route:
            return
        self.forward_way_listbox.delete(0, 'end')
        self.backward_way_listbox.delete(0, 'end')
        for stop in route.forward_way:
            self.forward_way_listbox.insert("end", stop)

        for stop in route.backward_way:
            self.backward_way_listbox.insert("end", stop)

    def on_station_selected(self, _):
        """
        All stations list box selected event handler.
        Displays list of the transport has a stop at the selected station and text representation of the query result.
        """
        station = self.get_listbox_item(self.station_listbox)
        transports = self.route_manager.has_stop_in(station)
        if not transports:
            return

        self.transport_through_station_listbox.delete(0, 'end')
        for transport in transports:
            self.transport_through_station_listbox.insert('end', str(transport))
        self.transport_through_station_label.config(text=self.route_manager.station_connect(station, transports))

    def on_station_to_selected(self, _):
        """
        On selected station to event handler.
        If both station_to and station_from are set - evaluates route.
        """
        self.station_to_value = self.get_listbox_item(self.station_to_listbox)
        if not self.station_to_value:
            return
        if not self.station_from_value:
            return

        self.display_route()

    def on_station_from_selected(self, _):
        """
        On selected station from event handler.
        If both station_to and station_from are set - evaluates route.
        """
        self.station_from_value = self.get_listbox_item(self.station_from_listbox)
        if not self.station_from_value:
            return
        if not self.station_to_value:
            return

        self.display_route()

    def display_route(self):
        """
        Displays route information.
        """
        found_route = self.route_manager.find_route(self.station_from_value, self.station_to_value)
        if not found_route:
            self.route_result_label.configure(text=self.ROUTE_NOT_FOUND.format(self.station_from_value,
                                                                               self.station_to_value))
            return
        if isinstance(found_route, str):
            self.route_result_label.configure(text=found_route)
        else:
            self.route_result_label.configure(text='\n'.join(found_route))

    def from_station_to_transport(self, _):
        """
        Transport selected from query result listbox event handler.
        Changes query frame to 'Маршрут громадського транспорту'
        and display information about selected item at this list.
        """
        transport = self.get_listbox_item(self.transport_through_station_listbox)
        if not transport:
            return
        self.query_selector_combobox.current(0)
        self.on_combobox_selected(_)
        self.transport_listbox.select_set(self.route_manager.find_transport_index(transport))
        self.on_transport_selected(_)

    def from_transport_to_station(self, _):
        """
        Stations selected from query result listbox event handler.
        Changes query frame to 'Які транспортні засоби зупиняються на станції'
        and display information about selected item at this list.
        """
        forward_station = self.get_listbox_item(self.forward_way_listbox)
        backward_station = self.get_listbox_item(self.backward_way_listbox)
        if forward_station:
            return self.change_station(forward_station)

        if backward_station:
            return self.change_station(backward_station)

    def change_station(self, station: str):
        """
        Helping function to find station to display info about.

        :param station: station to find information about.
        """
        self.query_selector_combobox.current(1)
        self.on_combobox_selected(None)
        self.station_listbox.select_set(self.route_manager.all_stations.index(station))
        self.on_station_selected(None)


def main():
    manager = RouteManagerWindow()
    manager.mainloop()


if __name__ == "__main__":
    main()
