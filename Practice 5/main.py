import random
import string
from dataclasses import dataclass, field
from datetime import date, datetime
from os import getcwd
from re import compile


class QueueIsEmptyException(BaseException):
    """
    Uses when queue is empty.
    """

    def __init__(self):
        super(QueueIsEmptyException, self).__init__('Queue is empty')


class TruckNumberNotValidException(BaseException):
    """
    Raises if the truck number value does not match the pattern 'LLDDDDLL':
    where  L - letter,
           D - digit.
    """

    def __init__(self, value: str):
        super(TruckNumberNotValidException, self).__init__(f'Truck number: {value} is not valid'
                                                           f'\nMust be 2 letters, 4 digits and 2 letters'
                                                           f'\nFor example: AA1111BB')


class DateNotValidException(BaseException):
    """
    Raises if the data value is not in the format dd/mm/yyyy.
    """

    def __init__(self, value: str):
        super(DateNotValidException, self).__init__(f'Date of the customs visiting {value} is not valid.'
                                                    f'\nMust be dd/mm/yyyy'
                                                    f'\nFor example: 16/10/2022')


class ContractNotValidException(BaseException):
    def __init__(self, value: str):
        """
        Raises when contract is not one of the values [f, false, 0, t, true, 1].
        """
        super(ContractNotValidException, self).__init__(f'Contract information {value} must be boolean value.'
                                                        f'\nMust be one of the values:'
                                                        f'\n[f, false, 0, t, true, 1]')


class PriceNotValidException(BaseException):
    """
    Raises when price of the product is not positive float value.
    """

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

    @property
    def source(self):
        """
        Get storage data copy.

        :returns: copy of the queue.
        """
        return self.__storage.copy()

    def filter(self, selector=lambda x: True) -> list:
        """
        Gets all elements from the queue that match the selector.

        :returns: list of the values that match the selector.
        """
        return [item for item in self.__storage if selector(item)]


@dataclass(frozen=True)
class Goods:
    """
    Readonly representation of the product that truck is delivering.
    """
    title: str
    price: float


@dataclass(frozen=True)
class CustomsDeclaration:
    """
    Readonly representation of the customs declaration with information about truck, company, products and route.
    """
    brand: str
    number: str
    company: str
    date: date
    city_from: str
    destination: str
    carriage_contract: bool
    goods: list[Goods] = field(default_factory=list)


class Customs:
    """
    Provides access to the customs management.
    """
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

    def __iter__(self):
        return CustomsDispatcher(self)

    def load_trucks(self):
        """
        Loads trucks from file (trucks.csv).
        """
        with open(self.FILE_SOURCE, encoding='utf-8') as source:
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
        """
        Validates and format truck number.

        :param number: string value to validate and convert.
        :raise TruckNumberNotValidException: number does not match the format LLDDDDLL.
        :returns: Validated and upper string of the valid number.
        """
        if self.NUMBER_VALIDATOR.match(number):
            return number.upper()
        raise TruckNumberNotValidException(number)

    def validate_date(self, validate_date: str):
        """
        Validates and converts date.

        :param validate_date: string value of the date to validate and convert.
        :raises DateNotValidException: date does not match the format %d/%m/%Y.
        :returns: date converted from the string in %d/%m/%Y format.
        """
        if self.DATE_VALIDATOR.match(validate_date):
            return datetime.strptime(validate_date, '%d/%m/%Y').date()
        raise DateNotValidException(validate_date)

    def validate_contract(self, contract: str):
        """
        Validates and converts to bool contract value.

        :param contract: boolean value of the contract containing.
        :raises ContractNotValidException: contract value must be one of the strings: [f, false, 0, t, true, 1].
        :returns: True - if contact is t, true or 1. False - otherwise.
        """
        if self.CONTRACT_VALIDATOR.match(contract):
            return False if contract in self.FALSE_VALUES else True
        raise ContractNotValidException(contract)

    def validate_price(self, price: str):
        """
        Validates and converts price value.

        :param price: string value of the price.
        :returns: float value of the price.
        :raises PriceNotValidException: price must be positive floating point value like 0.0, 12.0, 15000.31
        """
        if self.PRICE_VALIDATOR.match(price):
            return float(price)
        raise PriceNotValidException(price)

    def parse_goods(self, goods: list[str]):
        """
        Parses information about products that are delivering.

        :param goods: list of the values of the products.
        :returns: list of goods.
        """
        return [Goods(g[0], self.validate_price(g[1])) for g in [goods[i: i + 2] for i in range(0, len(goods), 2)]]


class CustomsDispatcher:
    """
    Provides access to the customs management.
    """
    GREEN_QUEUE_UPDATE = "Declaration of truck {0} with number {1} was added to the green queue."
    COMMON_QUEUE_UPDATE = "Declaration of truck {0} with number {1} was added to the common queue."
    CHANGED_QUEUE_DUE_TO_PRICE = "Declaration of truck {0} with number {1} was added to common queue " \
                                 "due to price limit oversizing ({2:.2f})"
    TRUCK_PASSED = "Truck {0} with number {1} has passed the customs at {2:%d/%m/%Y}"
    TRUCK_REMOVED_DATE_EXPIRED = "Truck {0} with number {1} can not pass the customs due date expiration:" \
                                 "\nToday: {2:%d/%m/%Y}\nDate: {3:%d/%m/%Y}"
    MAX_SUM_RESPONSE = "Truck {0} with number {1} has transported goods for sum {2:.2f}."
    TRANSPORTED_GOODS = "Trucks:\n{0}\nhave transported '{1}'."
    NO_ONE_TRANSPORTED = "There is no truck that transported {0}."
    GOES_TO = "Trucks going to {0}:\n{1}."
    NO_ONE_GOES_TO = "There is no truck that goes to the {0}."
    GOES_FROM = "Trucks going from {0}:\n{1}."
    NO_ONE_GOES_FROM = "There is no truck that goes from the {0}."
    TRUCK_TRANSPORTED_GOODS = "{0} with number {1}"
    TITLE_FORMAT = '|{0:^20}|{1:^20}|'
    TABLE_FORMAT = '|{0:^20}|{1:^20.2f}|'
    PRICE_BOUND = 15_000
    RESPONSE_SEPARATOR = f"\n{'=' * 100}\n"
    HISTORY = ""

    def __init__(self, customs: Customs):
        self.source = customs
        self.passed_trucks = Queue(self.trucks)
        self.current = -1

    def __enter__(self):
        self.form_queues()
        self.handle_green_queue()
        self.handle_common_queue()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save_session()

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.trucks:
            raise StopIteration()
        result = self.source.trucks[self.current]
        self.current += 1
        return result

    @staticmethod
    def trace(func):
        """
        Decorator to store and save all invocation data and print it.

        :param func: function to decorate.
        """

        def inner(*args):
            """
            Invokes function and save needed data about it.

            :params args: argument of the func.
            """

            response = f"Response for: {func.__name__}({','.join([str(arg) for arg in args[1:]])})\n" \
                       + str(func(*args)) \
                       + CustomsDispatcher.RESPONSE_SEPARATOR
            print(response)
            CustomsDispatcher.HISTORY += response

        return inner

    @property
    def trucks(self):
        """
        Gets amount of the trucks.

        :returns: amount of the trucks records.
        """
        return len(self.source.trucks)

    def save_session(self):
        """
        Saves all the request's history if it is not empty.
        """
        if not self.HISTORY:
            return
        file_to_save = f"{getcwd()}\\customs_report_from" + \
                       f"_{datetime.now().strftime('%Y_%d_%m_%H_%M_%S')}.txt"
        with open(file_to_save, 'w+', encoding="utf-8") as file:
            file.write(self.HISTORY)

    def form_queues(self):
        """
        Split trucks declarations to common queue and green queue.
        If declaration has carriage contract - get to the green queue. Otherwise - to the common.
        """
        for declaration in self.source:
            self.add_to_queue(declaration)

    def handle_green_queue(self):
        """
        Passes truck through the customs or move from the green queue to the common.
        """
        while not self.source.green_queue.is_empty:
            item = self.source.green_queue.take()
            self.manage_green_queue(item)

    def handle_common_queue(self):
        """
        Passes truck through the customs or move from the queue.
        """
        while not self.source.common_queue.is_empty:
            item = self.source.common_queue.take()
            self.manage_common_queue(item)

    @trace
    def add_to_queue(self, declaration: CustomsDeclaration):
        """
        Moves truck to the one of the queue.
        If declaration has carriage contract - moves to the green queue.
        Otherwise - common queue.

        :param declaration: data for the customs transportations.
        :returns: action response.
        """
        if declaration.carriage_contract:
            self.source.green_queue.into(declaration)
            return self.GREEN_QUEUE_UPDATE.format(declaration.brand, declaration.number)
        else:
            self.source.common_queue.into(declaration)
            return self.COMMON_QUEUE_UPDATE.format(declaration.brand, declaration.number)

    @trace
    def manage_green_queue(self, declaration: CustomsDeclaration):
        """
        Moves from the one queue to the common queue or removes from the list at all.
        If total sum of the all products is grater than PRICE_BOUND - moves to the common queue.
        If date is expired - removes at all.
        Otherwise - passes through the customs.

        :param declaration: data for the customs transportations.
        :returns: action response.
        """
        total_sum = sum([product.price for product in declaration.goods])
        if total_sum >= self.PRICE_BOUND:
            self.source.common_queue.into(declaration)
            return self.CHANGED_QUEUE_DUE_TO_PRICE.format(declaration.brand, declaration.number, total_sum)
        if declaration.date < datetime.now().date():
            return self.TRUCK_REMOVED_DATE_EXPIRED.format(declaration.brand, declaration.number, datetime.now().date(),
                                                          declaration.date)
        self.passed_trucks.into(declaration)
        return self.TRUCK_PASSED.format(declaration.brand, declaration.number, datetime.now().date())

    @trace
    def manage_common_queue(self, declaration: CustomsDeclaration):
        """
        Passes truck or removes it from the list at all.
        If date is expired - removes at all.
        Otherwise - passes through the customs.

        :param declaration: data for the customs transportations.
        :returns: action response.
        """
        if declaration.date < datetime.now().date():
            return self.TRUCK_REMOVED_DATE_EXPIRED.format(declaration.brand, declaration.number, datetime.now().date(),
                                                          declaration.date)
        self.passed_trucks.into(declaration)
        return self.TRUCK_PASSED.format(declaration.brand, declaration.number, datetime.now().date())

    @trace
    def find_maximum_transported_price(self):
        """
        Finds truck with the product for the maximum price.

        :returns: Formatted result.
        """
        max_sum, result = 0, None
        for truck in self.passed_trucks.source:
            current_sum = sum([product.price for product in truck.goods])
            if current_sum > max_sum:
                max_sum, result = current_sum, truck
        return self.MAX_SUM_RESPONSE.format(result.brand, result.number, max_sum)

    @trace
    def transported(self, product: str):
        """
        Finds all trucks that had passed the customs and delivered set product.

        :param product: name of the product to transport.
        :returns: Formatted response, including 'not found' case.
        """
        filtered = self.passed_trucks.filter(lambda x: product in [p.title for p in x.goods])
        return self.TRANSPORTED_GOODS.format('\n'.join(self.TRUCK_TRANSPORTED_GOODS.format(truck.brand, truck.number)
                                                       for truck in filtered), product) if filtered \
            else self.NO_ONE_TRANSPORTED.format(product)

    @trace
    def end(self, city_to: str):
        """
        Finds all truck that have destination equal to 'city_to'.

        :param city_to: city of the truck destination.
        :returns: Formatted response, including 'not found' case.
        """
        filtered = self.passed_trucks.filter(lambda x: x.destination.lower() == city_to.lower())
        return self.GOES_TO.format(city_to, '\n'.join(self.TRUCK_TRANSPORTED_GOODS.format(truck.brand,
                                                                                          truck.number)
                                                      for truck in filtered)) if filtered \
            else self.NO_ONE_GOES_TO.format(city_to)

    @trace
    def start(self, city_from):
        """
        Finds all truck that have start point at 'city_from'.

        :param city_from: city of the truck start point.
        :returns: Formatted response, including 'not found' case.
        """
        filtered = self.passed_trucks.filter(lambda x: x.city_from.lower() == city_from.lower())
        return self.GOES_FROM.format(city_from, '\n'.join(self.TRUCK_TRANSPORTED_GOODS.format(truck.brand,
                                                                                              truck.number)
                                                          for truck in filtered)) if filtered \
            else self.NO_ONE_GOES_FROM.format(city_from)

    @trace
    def price_table(self):
        """
        Calculate sum of the products, that were delivered through the customs.

        :returns: Formatted table with name of the product and its price.
        """
        table = {}
        for truck in self.passed_trucks.source:
            for goods in truck.goods:
                if goods.title not in table:
                    table[goods.title] = 0
                table[goods.title] += goods.price
        return self.TITLE_FORMAT.format('Title', 'Price') + '\n' + '\n'.join(self.TABLE_FORMAT.format(key, value)
                                                                             for key, value in table.items())


class CustomsDataGenerator:
    """
    Generates information based on real data.
    """

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
              'Lviv', 'Odessa', 'Kyiv', 'Dnipro', 'Ivano-Frankivsk', 'Ternopil', 'Chernivcy', 'Kharkiv', 'Mycolaiv',
              'Vinnicia', 'Zydachiv', 'Rivne', 'Stryi']

    BOOLEAN = ['f', 'false', 't', 'true', '0', '1']
    PRODUCTS = ['Salt', 'Peper', 'Oranges', 'Apples', 'Gas', 'Fuel', 'Skin care', 'Watches', 'Milk', 'Cookies',
                'Olive oil', 'Honey', 'Candies', 'Maple syrup', 'Wine', 'Cheese', 'Cherries', 'Pasta', 'Baby care']

    @classmethod
    def brand(cls):
        """
        Randomize car brand.

        :return: randomly selected car brand.
        """
        return random.choice(cls.CAR_BRANDS)

    @classmethod
    def number(cls):
        """
        Generates random transport number in format LLDDDDLL.

        :returns: randomly created value of the transport number.
        """
        return "".join(random.choices(string.ascii_uppercase, k=2)) + \
               "".join(random.choices(string.digits, k=4)) + \
               "".join(random.choices(string.ascii_uppercase, k=2))

    @classmethod
    def company(cls):
        """
        Randomize company value.

        :returns: randomly selected company.
        """
        return random.choice(cls.FIRMS)

    @classmethod
    def date(cls):
        """
        Generates random date in format d/m/y, where:
            d - int value from 1 to 28.
            m - int value from 1 to 12.
            y - int value from 2022, 2023.

        :returns: formatted date value.
        """
        return f'{random.randint(1, 28):02d}/{random.randint(1, 12):02d}/{random.randint(2022, 2023)}'

    @classmethod
    def city(cls):
        """
        Randomize city value.

        :returns: randomly selected city.
        """
        return random.choice(cls.CITIES)

    @classmethod
    def contract(cls):
        """
        Randomize contract value.

        :returns: randomly selected contract.
        """
        return random.choice(cls.BOOLEAN)

    @classmethod
    def goods(cls):
        """
        Randomize amount of the goods and generate string representation of it.

        :returns: line of the product title and price.
        """
        return ','.join([f'{cls.title()}, {cls.price()}' for _ in range(random.randint(1, 10))])

    @classmethod
    def title(cls):
        """
        Randomize title value.

        :return: randomly selected title.
        """
        return random.choice(cls.PRODUCTS)

    @classmethod
    def price(cls):
        """
        Generates floating point value in format (1-10000).(0-99).

        :returns: floating point price value.
        """
        return f'{random.randint(0, 10_000)}.{random.randint(0, 99)}'

    @classmethod
    def generate(cls, amount: int, source: str):
        """
        Generates records in set amount and saves it to the source.

        :param amount: amount of the records to generate.
        :param source: source file to save value. Appends generated data to the end of the file.
        """
        lines = [f'{cls.brand()}, {cls.number()}, {cls.company()}, {cls.date()}, {cls.city()}, '
                 f'{cls.city()}, {cls.contract()}, {cls.goods()}' for _ in range(amount)]

        with open(source, 'a+', encoding='utf-8') as file:
            file.write('\n' + '\n'.join(lines))


def main():
    # CustomsDataGenerator.generate(20, Customs.FILE_SOURCE)
    with CustomsDispatcher(Customs()) as dispatcher:
        dispatcher.find_maximum_transported_price()
        dispatcher.transported('Candies')
        dispatcher.transported('Ramps')
        dispatcher.end('Kyiv')
        dispatcher.start('Lviv')
        dispatcher.start('Graz')
        dispatcher.end('Graz')
        dispatcher.price_table()


if __name__ == '__main__':
    main()
