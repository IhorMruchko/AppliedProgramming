=========================ENG=========================
Interpret: Python 3.10

To provide another format of the weather data parsing you should extend WeatherParser abstract class.
Then you can use it to create database based on dictionary and access info from it with WeatherOperator.

To add functionality: extend WeatherOperator class and to use history saving while call - add @trace decorator.

Base functionality to use:

format_city:
    Returns weather data for the city in the set format.

    *parameter* city: city to get info about.
    *parameter* city_format: format to display data.

max_temperature:
    Finds name of the city where the temperature is the highest.

max_temperature:
    Finds name of the city where the temperature is the lowest.

changes:
    Finds all data about temperature changes for the concrete city at the concrete date.

    *parameter* city: city to track changes in.
    *parameter* date: date to track changes when.

domain_wind:
    Defines the domain wind for all cities.

    *parameter* cites: all cities to get wind info from.

filter_temperature:
    Returns all records in the default format for records, where temperature is valid due to the predicate.

    *parameter* predicate: rule to accept the record based on temperature value.

save_session:
    Saves all the request's history if it is not empty.


=========================УКР=========================
Версія інтерпретатора: Python 3.10

Для того, щоб створити інший формат зчитування даних погоди, потрібно розширити абстрактний клас WeatherParser.
Після чого, для використання вбудованих запитів до бази даних, заснованої на словнику, потрібно створити клас
WeatherOperator.

Також цей клас можна розширити. Для того, щоб усі потрібні запити до бази записувались в історію потрібно додати
декоратор @trace.

Базова функціональність:

format_city:
    Повертає інформацію про погоду в місті згідно з заданим форматом.

    *параметр* city: місто, у якому шукати інформацію.
    *параметр* city_format: формат за яким її інформацію про погоду вивести.

max_temperature:
    Знаходить місто, у якому найбільша температура.

max_temperature:
    Знаходить місто, у якому найменша температура.

changes:
    Знаходить усі записи про погоду в певному місті в певну дату.

    *параметр* city: Місто, де простежити погоду.
    *параметр* date: Дата, коли простежити погоду.

domain_wind:
    Визначає панівний напрямок вітру серед усіх заданих міст.

    *параметр* cites: міста вибірки.

filter_temperature:
    Повертає усі записи з бази, у яких температура задовільняє правилу.

    *параметр* predicate: правило вибору запису за температурою.

save_session:
    Зберігає історію запитів, якщо історія не порожня.