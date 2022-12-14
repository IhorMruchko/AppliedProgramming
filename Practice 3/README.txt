=========================ENG=========================
Interpret: Python 3.10

App provides information about the Lviv`s city routes.
You can switch request with dropdown menu at the top of the window.
Press 's' to load file with all stations.
First Tab (Маршрут громадського транспорту):
    You can select one of the available public transport number and see his forward and backward route.
    By clicking on the station from the lists, you can switch to the second tab.

    For example:
        Press "Трамвай №6"
        See on the left all stations of the forward way and on the right - backward way.
        Click on the "Вулиця Якова Остряниці" and switch tab to the second one.
        On that tab you will see "Трамвай №6" and text "Через станцію Вулиця Якова Остряниці проходить 1 транспортний
        засіб: Трамвай №6"

Second Tab (Які транспортні засоби зупиняються на станції):
    You can select one of the station from the list on the left.
    After you select - you may see list of the public transports that have a stop at this station.
    You may click on the one element from that list to see forward and backward ways of this transport.
    At the right bottom you might see text, that represents detailed information about the request.

    For example:
        Press "Собор Святого Юра" on the left side.
        See on the top-right list of all public transports: Тролейбус №22, Тролейбус №27, Тролейбус №30, Тролейбус №32
        Under that list you will see text: "Через станцію Собор Святого Юра проходить 4 транспортні засоби:
        Тролейбус №22, Тролейбус №27, Тролейбус №30, Тролейбус №32"
        You may click on the "Тролейбус 30" on the top-left of the screen. That will open first tab with information
        about forward and backward ways of the "Тролейбус 30"

Third Tab (Знайти маршрут через зупинки)
    On the left side of the screen will be list of all possible stations - it is station from selector.
    On the right side of the screen will be list of all possible stations - it is station to selector.
    Select from one list and from second list stations and get a result at the bottom of the screen.

    For example:
        Press "Автовокзал" from the left and "Будинок Аркаса" from the right than see
        "Маршрут між Автовокзал та Будинок Аркаса зупинками не знайдено"
        Than select from the list right "Автобусний завод" and see "Сідайте на зупинці Автовокзал на Тролейбус №25.
        Проїдьте 5 зупинок та виходіть на станції "Автобусний завод""
        Than change station from the left list to "Вулиця Академіка Підстригача" and see the response:
        "Сідайте на зупинці Вулиця Академіка Підстригача на Тролейбус 22. Проїдьте 5 зупинок та на зупинці Автовокзал
        пересядьте на тролейбус 25 та проїдьте 5 зупинок до станції Автобусний завод"

=========================УКР=========================
Версія: Python 3.10

Додаток надає інформацію про маршрути міста Львова.
Зміна запиту виконується за допомогою випадаючого списку зверху екрану.
Натисніть "s", щоб зберегти список усіх станцій.

Перша вкладка (Маршрут громадського транспорту):
    Ви можете вибрати один із маршрутів у наявному списку, щоб отримати інформацію про прямий та зворотній маршрути.
    Натиснувши на результат, який появляється у двох списках нижче, можна перейти на другу вкладку запиту та отримати
    інформацію про станцію.

    Наприклад:
        Натисніть "Трамвай №6"
        Зліва ви побачите список зупинок прямого маршруту, справа - зворотного.
        Натисніть на "Вулиця Якова Остряниці" та змініть вкладку на другу.
        На цій вкладці ви побачите "Трамвай №6" та текст: "Через станцію Вулиця Якова Остряниці проходить 1 транспортний
        засіб: Трамвай №6"

Друга вкладка (Які транспортні засоби зупиняються на станції):
    Ви можете обрати станцію на вкладці зліва.
    Після того, яки ви її оберете, появиться список всіх ТЗ, які мають зупинку на цій станції та текстову відповідь.
    Також ви можете натиснути на елемент списку усіх ТЗ та перейти на першу вкладку.
    Знизу-справа розміщується більш детальна відповідь на запит.

    Наприклад:
        Оберіть "Собор Святого Юра" із списку зліва.
        Тоді ви побачите список справа-зверху: Тролейбус №22, Тролейбус №27, Тролейбус №30, Тролейбус №32
        Під цим текстом розташовано текст-відповідь: "Через станцію Собор Святого Юра проходить 4 транспортні засоби:
        Тролейбус №22, Тролейбус №27, Тролейбус №30, Тролейбус №32"
        Ви можете натиснути на "Тролейбус 30" зі списку зверху. Це відкриє першу вкладку з детальною інформацією про
        прямий та зворотний маршрути "Тролейбус 30".

Третя вкладка (Знайти маршрут через зупинки)
    Зліва знаходиться список усіх зупинок. При виборі певної - вибирається зупинка, звідки шукати маршрути.
    Справа знаходиться список усіх зупинок. При виборі певної - обирається зупинка, куди шукати маршрут.
    Оберіть з двох списків по зупинці та отримайте результат, як добратись від однієї зупинки до іншої.

    Наприклад:
        Оберіть "Автовокзал" зі списку зліва та "Будинок Аркаса" зі списку справа та отримайте відповідь:
        "Маршрут між Автовокзал та Будинок Аркаса зупинками не знайдено"
        Пізніше оберіть зі списку справа "Автобусний завод" та отримайте відповідь:
        "Сідайте на зупинці Автовокзал на Тролейбус №25. Проїдьте 5 зупинок та виходіть на станції "Автобусний завод""
        Після чого можете змінити станцію зі списку зліва "Вулиця Академіка Підстригача" та отримати таку відповідь:
        "Сідайте на зупинці Вулиця Академіка Підстригача на Тролейбус 22. Проїдьте 5 зупинок та на зупинці Автовокзал
        пересядьте на тролейбус 25 та проїдьте 5 зупинок до станції Автобусний завод"