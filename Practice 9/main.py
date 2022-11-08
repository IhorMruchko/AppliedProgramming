import json
import requests
from abc import ABC, abstractmethod
from datetime import datetime
from os import path, getcwd


class JsonFileScrapper:
    JSON_FORMAT = ".json"
    SUCCESS = 200

    @staticmethod
    def load(url: str):
        return requests.get(url)

    def save(self, url: str, save_file_to: str = None):
        if save_file_to and not path.exists(path.dirname(save_file_to)):
            raise NotADirectoryError(f"There is no such a directory. ({path.dirname(save_file_to)})")
        if save_file_to and not save_file_to.endswith(self.JSON_FORMAT):
            save_file_to += self.JSON_FORMAT
        response = self.load(url)
        file_source = save_file_to if save_file_to else self.get_file_path()
        with open(file_source, 'w+') as saver:
            saver.write(json.dumps(response.text, indent=4))
        response.close()

    def get_file_path(self):
        return f"{getcwd()}\\loaded_json" + \
                f"_{datetime.now().strftime('%Y_%d_%m_%H_%M_%S')}{self.JSON_FORMAT}"


class JSONWorker(ABC):
    def __init__(self):
        self.json_data = None

    @abstractmethod
    def source(self):
        pass

    def load(self):
        with open(self.source(), "r") as json_source:
            self.json_data = json.load(json_source)


class CryptoJsonWorker(JSONWorker):
    def source(self):
        return f'{getcwd()}/crypto.json'


def main():
    scrapper_crypto = JsonFileScrapper()
    scrapper_photo = JsonFileScrapper()

    scrapper_crypto.save("https://jsonplaceholder.typicode.com/photos", f"{getcwd()}\\crypto")
    scrapper_photo.save("https://www.cryptingup.com/api/markets", f"{getcwd()}\\photos")
    crypto_worker = CryptoJsonWorker()
    crypto_worker.load()
    print(crypto_worker.json_data)


if __name__ == "__main__":
    main()
