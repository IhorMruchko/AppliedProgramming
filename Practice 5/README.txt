=========================ENG=========================
Program provides access to the customs management.
To add record to the customs queue you may use 'trucks.csv' file.
You may add data by your own or use CustomsDataGenerator class to generate specified amount of records and saves it
to the file you need.

To use customs database create class CustomsDispatcher with Customs class parameter in the context manager
(directive with) and use dispatchers methods.

Dispatcher methods:
    find_maximum_transported_price: finds truck with the maximum price.
    transported(product title): finds trucks that transported product with specified title.
    end(destination city): finds trucks that have destination at the specified city.
    start(start city): finds trucks that have start point at the specified city.
    price_table: prints table of the all transported products.

=========================УКР=========================
Програма надає доступ до бази даних митного контролю.
Щоб додати запис до бази використовуйте файл 'trucks.csv'.
Ви можете самостійно додати дані або використати клас CustomsDataGenerator для створення потрібної кількості записів
та збереження їх у потрібному файлі (файл дописується).

Для використання бази даних митного контролю створіть клас CustomsDispatcher з параметром - об'єктом класу Customs
в менеджері контексту (структура with) та використати методи диспетчера.

Методи диспетчера:
    find_maximum_transported_price: знаходить запис про машину із найбільшою ціною.
    transported(product title): знаходить усі машини, які перевозили вказаний товар.
    end(destination city): знаходить усі вантажівки, які прямують до вказаного міста.
    start(start city): знаходить усі вантажівки, які прямують із вказаного міста.
    price_table: виводить таблицю загальної ціни по усім товарам.