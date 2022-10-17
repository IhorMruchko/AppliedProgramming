import random
import string
from dataclasses import dataclass, field
from datetime import date, datetime
from re import compile


class QueueIsEmptyException(BaseException):
    """
    Uses when queue is empty.
    """

    def __init__(self):
        super(QueueIsEmptyException, self).__init__('Queue is empty')


class TruckNumberNotValidException(BaseException):
    def __init__(self, value: str):
        super(TruckNumberNotValidException, self).__init__(f'Truck number: {value} is not valid'
                                                           f'\nMust be 2 letters, 4 digits and 2 letters'
                                                           f'\nFor example: AA1111BB')


class DateNotValidException(BaseException):
    def __init__(self, value: str):
        super(DateNotValidException, self).__init__(f'Date of the customs visiting {value} is not valid.'
                                                    f'\nMust be dd/mm/yyyy'
                                                    f'\nFor example: 16/10/2022')


class ContractNotValidException(BaseException):
    def __init__(self, value: str):
        super(ContractNotValidException, self).__init__(f'Contract information {value} must be boolean value.'
                                                        f'\nMust be one of the values:'
                                                        f'\n[f, false, 0, t, true, 1ъ]')


class PriceNotValidException(BaseException):
    def __init__(self, value: str):
        super(PriceNotValidException, self).__init__(f'Price of the goods is not valid {value}'
                                                     f'\nMust be not negative float values'
                                                     f'\nFor example: [12.5, 15.0, 0.0]')


class Queue:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.__storage = []

    def __str__(self):
        return f'Queue({self.capacity}) <{", ".join([str(item) for item in self.__storage])}>'

    def __bool__(self):
        return not self.is_empty

    @property
    def is_empty(self):
        """
        Defines is queue empty.

        :returns: is queue empty.
        """
        return len(self.__storage) == 0

    @property
    def capacity(self):
        """
        Gets capacity of the queue.

        :returns: queue's capacity.
        """
        return self.__capacity

    @capacity.setter
    def capacity(self, value: int):
        """
        Sets the capacity of the queue.

        :param value: capacity of the queue.
        :exception ValueError: capacity of the queue must be grater than zero.
        """
        if value <= 0:
            raise ValueError("Capacity of the queue can not be less or equal zero")
        self.__capacity = value

    def into(self, value):
        """
        Add element to the queue.

        :param value: element to add the the queue.
        :returns: same queue.
        """
        self.__storage.append(value)
        return self

    def take(self):
        """
        Take element from the queue and remove it.

        :exception QueueIsEmptyException: can not get element from the empty queue.
        :returns: first element from the queue.
        """
        if self.is_empty:
            raise QueueIsEmptyException()
        result = self.__storage[0]
        self.__storage.remove(result)
        return result

    def back(self):
        """
        Gets the last element of the queue.

        :exception QueueIsEmptyException: can not get element from the empty queue.
        :returns: last element of the queue.
        """
        if self.is_empty:
            raise QueueIsEmptyException()
        return self.__storage[-1]

    def front(self):
        """
        Gets the first element from the queue.

        :exception QueueIsEmptyException: can not get element from the empty queue.
        :returns: first element of the queue.
        """
        if self.is_empty:
            raise QueueIsEmptyException()
        return self.__storage[0]


@dataclass(frozen=True)
class Goods:
    title: str
    price: float


@dataclass(frozen=True)
class CustomsDeclaration:
    brand: str
    number: str
    company: str
    date: date
    city_from: str
    destination: str
    carriage_contract: bool
    goods: list[Goods] = field(default_factory=list)


class Customs:
    FILE_SOURCE = "trucks.csv"
    CHARS_TO_REMOVE = '\n '
    FALSE_VALUES = ['f', "false", '0']
    NUMBER_VALIDATOR = compile(r'\D{2}\d{4}\D{2}')
    DATE_VALIDATOR = compile(r'\d{2}/\d{2}/\d{4}')
    CONTRACT_VALIDATOR = compile(r'f|(false)|0|t|(true)|1')
    PRICE_VALIDATOR = compile(r'\d*\.d{0,2}')

    def __init__(self):
        self.trucks: list[CustomsDeclaration] = []
        self.load_trucks()
        self.common_queue = Queue(len(self.trucks))
        self.green_queue = Queue(len(self.trucks))

    def load_trucks(self):
        with open(self.FILE_SOURCE) as source:
            truck_information = [line.strip(self.CHARS_TO_REMOVE)
                                 for line in source.readlines()[1:]
                                 if line.strip(self.CHARS_TO_REMOVE) != '']

        for info in truck_information:
            brand, number, company, customs_date, city_from, destination, contract, *goods = \
                map(lambda x: x.strip(self.CHARS_TO_REMOVE), info.split(','))

            number = self.validate_number(number)
            customs_date = self.validate_date(customs_date)
            contract = self.validate_contract(contract.lower())
            goods = self.parse_goods(goods)
            self.trucks.append(CustomsDeclaration(brand, number, company, customs_date, city_from,
                                                  destination, contract, goods))

    def validate_number(self, number: str):
        if self.NUMBER_VALIDATOR.match(number):
            return number.upper()
        raise TruckNumberNotValidException(number)

    def validate_date(self, validate_date: str):
        if self.DATE_VALIDATOR.match(validate_date):
            return datetime.strptime(validate_date, '%d/%m/%Y').date()
        raise DateNotValidException(validate_date)

    def validate_contract(self, contract: str):
        if self.CONTRACT_VALIDATOR.match(contract):
            return False if contract in self.FALSE_VALUES else True
        raise ContractNotValidException(contract)

    def validate_price(self, price: str):
        if self.PRICE_VALIDATOR.match(price):
            return float(price)
        raise PriceNotValidException(price)

    def parse_goods(self, goods: list[str]):
        return [Goods(g[0], self.validate_price(g[1])) for g in [goods[i: i + 2] for i in range(0, len(goods), 2)]]


class CustomsDataGenerator:
    CAR_BRANDS = [
        'Daf', 'Iveco', 'Maz', 'Man', 'Scania', 'Ford', 'Volvo', 'Kraz', 'Camaz', 'Gaz', 'Freightliner Cascadia',
        'Peterbilt', 'Kenworth', 'Western Star', 'Lonestar', 'Mack Titan'
    ]

    FIRMS = [
        'Sevenprort', 'Cargo', 'NX Logistics', 'Partner trade', 'VIVA+', 'Almaida group', 'Hegelman transport',
        'Legende Logic', 'Graymar', 'You be I logistic', 'Soloviy trans', 'A7 trans', 'Avtotrans brocker',
        'Imecs credy', 'MIK', 'Mortrans AGC'
    ]

    CITIES = ['Aalborg', 'Aberdeen', 'A Coruña', 'Ajaccio', 'Albacete', 'Algeciras', 'Almaraz', 'Almería', 'Amsterdam',
              'Ancona', 'Bacău', 'Badajoz', 'Bailén', 'Banská Bystrica', 'Barcelona', 'Bari', 'Bastia', 'Bayonne',
              'Beja', 'Bergen', 'Berlin', 'Bern', 'Białystok', 'Bilbao', 'Birmingham', 'Bologna', 'Bonifacio',
              'Bordeaux', 'Bourges', 'Brașov', 'Bratislava', 'Bremen', 'Brest', 'Brussel', 'Brno', 'București',
              'Budapest', 'Burgas', 'Burgos', 'Cagliari', 'Calais', 'Călărași', 'Calvi', 'Cambridge', 'Cardiff',
              'Carlisle', 'Cassino', 'Catania', 'Catanzaro', 'Cernavodă', 'Ciudad Real', 'Civaux', 'Clermont-Ferrand',
              'Cluj-Napoca', 'Coimbra', 'Constanța', 'Córdoba', 'Cortiçadas de Lavre', 'Craiova', 'Daugavpils',
              'Debrecen', 'Dijon', 'Dortmund', 'Dover', 'Dresden', 'Duisburg', 'Düsseldorf', 'Edinburgh', 'Edirne',
              'El Ejido', 'Erfurt', 'Esbjerg', 'Évora', 'Faro', 'Felixstowe', 'Firenze', 'Frankfurt am Main',
              'Frederikshavn', 'Galați', 'Gdańsk', 'Gedser', 'Genève', 'Genova', 'Gijón', 'Glasgow', 'Golfech',
              'Göteborg', 'Granada', 'Graz', 'Grimsby', 'Groningen', 'Guarda', 'Hamburg', 'Hannover', 'Helsingborg',
              'Helsinki', 'Hirtshals', 'Huelva', 'Hunedoara', 'Iași', 'Innsbruck', 'İstanbul', 'Jönköping',
              'Kalmar', 'Kapellskär', 'Karlovo', 'Karlskrona', 'Kaunas', 'Kassel', 'Katowice', 'Kiel',
              'Klagenfurt am Wörthersee', 'Klaipėda', 'København', 'Köln', 'Košice', 'Kotka', 'Kouvola', 'Kozloduy',
              'Kraków', 'Kristiansand', 'Kunda', 'Lacq', 'Lahti', 'La Rochelle', 'Leipzig', 'Le Havre', 'Le Mans',
              'León', 'Liège', 'Liepāja', "L'Île-Rousse", 'Lille', 'Limoges', 'Linköping', 'Linz', 'Lisboa',
              'Liverpool', 'Livorno', 'Lleida', 'Łódź', 'London', 'Loviisa', 'Lublin', 'Luxembourg', 'Lyon',
              'Madrid', 'Magdeburg', 'Málaga', 'Malmö', 'Manchester', 'Mangalia', 'Mannheim', 'Marseille', 'Mažeikiai',
              'Mengíbar', 'Messina', 'Metz', 'Milano', 'Montpellier', 'München', 'Murcia', 'Naantali', 'Nantes',
              'Napoli', 'Narva', 'Navia', 'Newcastle-upon-Tyne', 'Nice', 'Nürnberg', 'Nynäshamn', 'O Barco', 'Odense',
              'Olbia', 'Olhão', 'Olkiluoto', 'Olsztyn', 'Örebro', 'Oslo', 'Osnabrück', 'Ostrava', 'Paldiski', 'Palermo',
              'Paluel', 'Pamplona', 'Panevėžys', 'Paris', 'Parma', 'Pärnu', 'Pécs', 'Pernik', 'Pescara', 'Pirdop',
              'Pitești', 'Pleven', 'Plovdiv', 'Plymouth', 'Ponte de Sor', 'Pori', 'Port de Sagunt', 'Porto',
              'Porto-Vecchio', 'Poznań', 'Praha', 'Puertollano', 'Reims', 'Rennes', 'Reșița', 'Rēzekne',
              'Rīga', 'Roma', 'Roscoff', 'Rostock', 'Rotterdam', 'Ruse', 'Saint-Alban-du-Rhône', 'Saint-Laurent',
              'Salamanca', 'Salzburg', 'Santander', 'Sassari', 'Setúbal', 'Sevilla', 'Sheffield', 'Šiauliai', 'Sines',
              'Södertälje', 'Sofia', 'Soria', 'Southampton', 'Stavanger', 'Strasbourg', 'Stockholm',
              'Stuttgart', 'Suzzara', 'Swansea', 'Szeged', 'Szczecin', 'Tallinn', 'Tampere', 'Taranto', 'Târgu Mureș',
              'Tarragona', 'Tartu', 'Tekirdağ', 'Terni', 'Teruel', 'Timișoara', 'Torino', 'Toulouse', 'Travemünde',
              'Trelleborg', 'Turku', 'Uppsala', 'Utena', 'València', 'Valladolid', 'Valmiera', 'Vandellòs', 'Varna',
              'Västerås', 'Växjö', 'Veliko Tarnovo', 'Venezia', 'Ventspils', 'Verona', 'Vigo', 'Vila-real',
              'Villa San Giovanni', 'Vilnius', 'Warszawa', 'Werlte', 'Wien', 'Wrocław', 'Zaragoza', 'Zürich',
              'Lviv', 'Odessa', 'Kiyv', 'Dnipro', 'Ivano-Frankivsk', 'Ternopil', 'Chernivcy', 'Kharkiv', 'Mycolaiv',
              'Vinnicia', 'Zydachiv', 'Rivne', 'Stryi'
              ]

    BOOLEAN = ['f', 'false', 't', 'true', '0', '1']
    PRODUCTS = ['Salt', 'Peper', 'Oranges', 'Apples', 'Gas', 'Fuel', 'Skin care', 'Watches', 'Milk', 'Cookies',
                'Olive oil', 'Honey', 'Candies', 'Maple syrup', 'Wine', 'Cheese', 'Cherries', 'Pasta', 'Baby care']

    @classmethod
    def brand(cls):
        return random.choice(cls.CAR_BRANDS)

    @classmethod
    def number(cls):
        return "".join(random.choices(string.ascii_uppercase, k=2)) + \
               "".join(random.choices(string.digits, k=4)) + \
               "".join(random.choices(string.ascii_uppercase, k=2))

    @classmethod
    def company(cls):
        return random.choice(cls.FIRMS)

    @classmethod
    def date(cls):
        return f'{random.randint(1, 28):02d}/{random.randint(1, 12):02d}/{random.randint(2022, 2023)}'

    @classmethod
    def city(cls):
        return random.choice(cls.CITIES)

    @classmethod
    def contract(cls):
        return random.choice(cls.BOOLEAN)

    @classmethod
    def goods(cls):
        return ','.join([f'{cls.title()}, {cls.price()}' for _ in range(random.randint(1, 10))])

    @classmethod
    def title(cls):
        return random.choice(cls.PRODUCTS)

    @classmethod
    def price(cls):
        return f'{random.randint(0, 10_000)}.{random.randint(0, 100)}'

    @classmethod
    def generate(cls, amount: int, source: str):
        lines = [f'{cls.brand()}, {cls.number()}, {cls.company()}, {cls.date()}, {cls.city()}, '
                 f'{cls.city()}, {cls.contract()}, {cls.goods()}' for _ in range(amount)]
        
        with open(source, 'a+', encoding='utf-8') as file:
            file.write('\n'.join(lines))


def main():
    # CustomsDataGenerator.generate(50, Customs.FILE_SOURCE)
    c = Customs()
    print(c.trucks)


if __name__ == '__main__':
    main()
