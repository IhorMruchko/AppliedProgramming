import ctypes.wintypes
from http.client import HTTPSConnection, HTTPResponse
from os import startfile, path


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


def main():
    source = PackageLoader.load_package("Newtonsoft.Json", method="GET")
    startfile(source)


if __name__ == '__main__':
    main()
