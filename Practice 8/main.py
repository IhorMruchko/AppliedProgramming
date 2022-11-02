import ctypes.wintypes
from http.client import HTTPSConnection, HTTPResponse
from os import path, startfile
from sys import float_info, maxsize
from xml.etree.ElementTree import parse, Element, ElementTree, indent


def avg(source: list[int | float]) -> float:
    """
    Finds average of the source.

    :param source: list of int or float values.
    :returns: average of the list.
    """
    return sum(source) / len(source)


class PackageLoader:
    """
    Loads and saves the page of the nuget package.

    FOLDER_TO_SAVE_FILES - user document file at the computer.
    STORAGE - path to the user's documents folder.
    """
    FOLDER_TO_SAVE_FILES = 5
    CURRENT_FOLDER = 0
    STORAGE = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(0, FOLDER_TO_SAVE_FILES, 0, 0, STORAGE)
    STORAGE = STORAGE.value

    ACCEPTABLE_METHODS = "GET POST"
    HTML_FORMAT = '.html'
    SERVER_NAME = "www.nuget.org"
    PACKAGE_SOURCE = "/packages/{0}"
    FILE_TO_SAVE = "{0}\\nuget-parse-{1}.html"
    GETTING_RESPONSE = "Getting response for {0} with method {1}."
    RESPONSE_NOT_GET = "For {0} with method {1} exception was risen: [{2}]."
    BAD_RESPONSE = "For {0} with method {1} response is [{2} ({3})]"
    RESPONSE_GOT = "For {0} with method {1} response successful."
    SUCCESS = 200

    @classmethod
    def load_package(cls, package: str, method: str = "GET", save_file_to: str = None) -> str:
        """
        Gets and saves the page of the nuget package.

        :param package: name of the package to find in the nuget database.
        :param method: request method. [GET POST]
        :param save_file_to: file path to save loaded .html file.
        :raise ValueError: method must be GET or POST. Default - Get
        :raise NotADirectoryError: save_file_to directory must exist. Default - User documents folder.
        :returns: File path to the saved page.
        """
        if method not in cls.ACCEPTABLE_METHODS:
            raise ValueError(f"{method} must be one of the values: {cls.ACCEPTABLE_METHODS}.")
        if save_file_to and not path.exists(path.dirname(save_file_to)):
            raise NotADirectoryError(f"There is no such a directory. ({path.splitext(save_file_to)[0]})")
        if save_file_to and not save_file_to.endswith(cls.HTML_FORMAT):
            save_file_to += cls.HTML_FORMAT
        response = cls.get_response(package, method)
        if response.status == cls.SUCCESS:
            print(cls.RESPONSE_GOT.format(package, method))
            file_source = save_file_to if save_file_to else cls.FILE_TO_SAVE.format(cls.STORAGE, package)
            with open(file_source, 'wb+') as saver:
                saver.write(response.read())
            response.close()
            return file_source
        print(cls.BAD_RESPONSE.format(package, method, response.reason, response.status))
        exit(-1)

    @classmethod
    def get_response(cls, package: str, method: str) -> HTTPResponse:
        """
        Gets response from the www.nuget.org with specified method for specified package.

        :param package: name of the package to find in the nuget database.
        :param method: request method. [GET POST]
        :returns: HTTPResponse for the request. Or exits the program if failed.
        """
        try:
            print(cls.GETTING_RESPONSE.format(package, method))
            server = HTTPSConnection(PackageLoader.SERVER_NAME)
            server.request(method, PackageLoader.PACKAGE_SOURCE.format(package))
            return server.getresponse()
        except Exception as e:
            print(cls.RESPONSE_NOT_GET.format(package, method, e))
            exit(-1)


class XMLManager:
    FILE_SOURCE = "sample.xml"
    FOOD_TAG = 'food'
    FOOD_NAME_TAG = 'name'
    PRICE_TAG = 'price'
    PRICE = "${0}"
    DESCRIPTION_TAG = 'description'
    CALORIES_TAG = 'calories'
    DOLLAR_SIGN = '$'

    DESCRIPTION_FOR = "'{0}' [{1}]."
    ELEMENT_NOT_FOUND = "Cannot find food with name '{0}'."

    def __init__(self):
        self.__root = parse(self.FILE_SOURCE).getroot()

    def add(self, name: str, price: float, description: str, calories: int) -> None:
        """
        Adds new element to the root.

        :param name: name of the food.
        :param price: price of the food.
        :param description: food's description.
        :param calories: calories of the food.
        """
        self.__root.append(self.create_food(name, price, description, calories))
        self.save_file()

    def find_max_calories(self):
        """
        Gets name of the food with max calories.

        :return: Name of the food with the greatest calories.
        """
        max_value, result = 0, None
        for name, calories in zip(self.__root.iter(self.FOOD_NAME_TAG), self.__root.iter(self.CALORIES_TAG)):
            if int(calories.text) > max_value:
                max_value, result = int(calories.text), name
        return result.text

    def find_min_calories(self):
        """
        Gets name of the food with min calories.

        :return: Name of the food with the lowest calories.
        """
        max_value, result = maxsize, None
        for name, calories in zip(self.__root.iter(self.FOOD_NAME_TAG), self.__root.iter(self.CALORIES_TAG)):
            if int(calories.text) < max_value:
                max_value, result = int(calories.text), name
        return result.text

    def find_max_price(self):
        """
        Gets name of the food by greatest price.

        :return: Name of the most expensive food.
        """
        max_value, result = 0, None
        for name, price in zip(self.__root.iter(self.FOOD_NAME_TAG), self.__root.iter(self.PRICE_TAG)):
            if float(price.text.removeprefix(self.DOLLAR_SIGN)) > max_value:
                max_value, result = float(price.text.removeprefix(self.DOLLAR_SIGN)), name
        return result.text

    def find_min_price(self):
        """
        Gets name of the cheapest food.

        :return: Name of the cheapest food.
        """
        max_value, result = float_info.max, None
        for name, price in zip(self.__root.iter(self.FOOD_NAME_TAG), self.__root.iter(self.PRICE_TAG)):
            if float(price.text.removeprefix(self.DOLLAR_SIGN)) < max_value:
                max_value, result = float(price.text.removeprefix(self.DOLLAR_SIGN)), name
        return result.text

    def find_average_calories(self) -> float:
        """
        Finds average calories value for all foods.

        :returns: average calories for all food.
        """
        return avg([int(element.text) for element in self.__root.iter(self.CALORIES_TAG)])

    def find_average_price(self) -> float:
        """
        Finds average price for all foods.

        :returns: average price for all food.
        """
        return round(avg([float(element.text.removeprefix(self.DOLLAR_SIGN))
                          for element in self.__root.iter(self.PRICE_TAG)]),
                     2)

    def get_description_of(self, name: str) -> str:
        """
        Finds description of the food with specified name.

        :param name: name of the food.
        :return: description of the food.
        """
        for food_name, desc in zip(self.__root.iter(self.FOOD_NAME_TAG), self.__root.iter(self.DESCRIPTION_TAG)):
            if food_name.text == name:
                return self.DESCRIPTION_FOR.format(name, desc.text)
        return self.ELEMENT_NOT_FOUND.format(name)

    @staticmethod
    def create_element(tag: str, value: str) -> Element:
        """
        Creates new tree element with specified tag and value.

        :param tag: element's tag.
        :param value: value to set to the element.
        :returns: new element of the tree with set value.
        """
        result = Element(tag)
        result.text = value
        return result

    def create_food(self, name: str, price: float, description: str, calories: int) -> Element:
        """
        Creates food node of the tree.

        :param name: name of the food.
        :param price: price of the food.
        :param description: food's description.
        :param calories: calories of the food.
        :returns: food node with all inner nodes.
        """
        food = Element(self.FOOD_TAG)
        food.append(self.create_element(self.FOOD_NAME_TAG, name))
        food.append(self.create_element(self.PRICE_TAG, self.PRICE.format(price)))
        food.append(self.create_element(self.DESCRIPTION_TAG, description))
        food.append(self.create_element(self.CALORIES_TAG, str(calories)))
        return food

    def save_file(self):
        """
        Saves changes to the root object.
        """
        to_save = ElementTree(self.__root)
        indent(to_save, '  ', level=0)
        to_save.write(self.FILE_SOURCE)


def main():
    # source_to_file = PackageLoader.load_package("CommandPrng")
    # startfile(source_to_file)

    manager = XMLManager()
    # manager.add("Borsch", 30.12, "National ukrainian dish", 900)
    print(manager.find_min_price())
    print(manager.find_min_calories())
    print(manager.find_max_price())
    print(manager.find_max_calories())
    print(manager.find_average_calories())
    print(manager.find_average_price())
    print(manager.get_description_of("Strawberry Belgian Waffles"))
    print(manager.get_description_of("No in list"))


if __name__ == '__main__':
    main()
