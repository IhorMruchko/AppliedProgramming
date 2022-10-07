from abc import ABC


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
        return self.TRAM_TRANSPORT_TYPE if "Tram" in str(self) else self.TROLLEYBUS_TRANSPORT_TYPE


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
            "Вулиця Академіка Підстригала",
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
            "Бондарівка",
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
        self.backward_way = reversed(self.forward_way.copy())


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
        self.backward_way = reversed(self.forward_way.copy())


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
            "Вулиця Каховська"
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
            "Вулиця Народна"
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
            "Бондарівка",
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


class RoutManager:
    """
    Represents manager of the public transport.
    Provides access to the operations on the available public transport.
    """
    # todo: find transports that has a stop at the station(s).
    # todo: define amount of stops between stations.
    # todo: define routs to get to one station from another.
    # todo check is it possible to get to some station from another.

    def __init__(self):
        """
        Initiates RoutManager.

        public_transport - list of the all available public transports.
        all_stations - list of the all stations, based on public_transport list
                     - unique, sorted in alphabetical order.
        all_transport_numbers - list of all the public transports rout numbers.
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


def main():
    manager = RoutManager()
    print('\n'.join(manager.all_stations))


if __name__ == "__main__":
    main()
