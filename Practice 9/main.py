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
    KEY_VALUE = '{0}={1}'
    SEPARATOR = '\n' + '=' * 100 + '\n'
    HISTORY = ''

    def __init__(self):
        self.json_data = None
        self.load()

    @staticmethod
    def trace(func):
        """
        Decorator to store and save all invocation data and print it.

        :param func: function to decorate.
        """

        def inner(*args, **kwargs):
            """
            Invokes function and save needed data about it.

            :params args: argument of the func.
            :param kwargs: optional arguments of the func.
            """

            result = func(*args, **kwargs)
            kwargs_response = f", {','.join([JSONWorker.KEY_VALUE.format(key, value) for key, value in kwargs.items()])}" \
                if kwargs else ""
            response = f"Response for: {func.__name__}({','.join([str(arg) for arg in args[1:]])}" \
                       f"{kwargs_response})\n" \
                       + str(result) \
                       + JSONWorker.SEPARATOR
            print(response)
            JSONWorker.HISTORY += response
            return result

        return inner

    @abstractmethod
    def source(self):
        """
        Gets directory of the source file of the JSON worker.
        """
        pass

    @abstractmethod
    def data(self):
        """
        Gets formatted data based on structure.
        """
        pass

    def load(self):
        """
        Loads data to the program's memory.
        """
        with open(self.source(), "r") as json_source:
            self.json_data = eval(json.load(json_source))

    def save(self):
        """
        Saves all the request's history if it is not empty.
        """
        if not self.HISTORY:
            return
        file_to_save = f"{getcwd()}\\json_report_from" + \
                       f"_{datetime.now().strftime('%Y_%d_%m_%H_%M_%S')}.txt"
        with open(file_to_save, 'w+', encoding="utf-8") as file:
            file.write(self.HISTORY)


class CryptoJsonWorker(JSONWorker):
    """
    Provides access to the binance file.
    """
    ROOT = 'markets'
    SUB_ROOT = 'quote'
    EXCHANGE_ID = 'exchange_id'
    SYMBOL = 'symbol'
    BASE_ASSET = 'base_asset'
    QUOTE_ASSET = 'quote_asset'
    UNCONVERTED_PRICE = 'price_unconverted'
    CHANGE_PER_DAY = 'change_24h'
    PRICE = 'price'
    SPREAD = 'spread'
    VOLUME_PER_DAY = 'volume_24h'
    STATUS = 'status'
    CREATED = 'created_at'
    UPDATED = 'updated_at'
    KEY_VALUE_DISPLAY = '\t{0} : {1}\n'
    QUOTES_DISPLAY = '\n{0}\n' + '-' * 50

    @property
    def data(self) -> list[dict]:
        return self.json_data[self.ROOT]

    def source(self):
        return f'{getcwd()}/crypto.json'

    @JSONWorker.trace
    def get_quote(self, name: str) -> dict:
        """
        Gets value of the quote.

        :param name: name of the quote.
        :returns: dict with quote's info or None.
        """
        return next(filter(lambda quote: quote[self.SYMBOL] == name, self.data), None)

    @JSONWorker.trace
    def get_sum(self, quote: dict) -> float:
        """
        Evaluates sum of quote's data.
        :param quote: quote to get sum from.
        :returns: sum of the crypto-money of the quote.
        """
        return sum(item[self.PRICE] for item in quote[CryptoJsonWorker.SUB_ROOT].values())

    @JSONWorker.trace
    def get_total_volume(self, quote: dict) -> float:
        """
         Evaluates total volume of quote's data.
        :param quote: quote to get sum from.
        :returns: total amount of the volume of the crypto-money of the quote.
        """
        if not quote:
            raise ValueError('Quote is None')
        return sum(item[self.VOLUME_PER_DAY] for item in quote[CryptoJsonWorker.SUB_ROOT].values())

    @JSONWorker.trace
    def order_by(self, key: str, descending=False) -> list[dict]:
        """
        Sort quotes by quotes field.
        :param key: key to sort by.
        :param descending: is descending sorting order.
        :returns: sorted by key list on ascending or descending order.
        """
        return sorted(self.data, key=lambda quote: quote[key], reverse=descending)

    def display_quote(self, quote: dict, *keys: str):
        """
        Gets string representation of the quotes by keys. Make projection on the quote.
        :param quote: quote to display.
        :param keys: keys to display from quote.
        :raise ValueError: At least one key must be provided.
        """
        if not keys:
            raise ValueError('Provide at least one key to display')

        return ''.join([self.KEY_VALUE_DISPLAY.format(key, value)
                        for value, key in zip([quote[key] for key in keys if key in quote.keys()], keys)])

    @JSONWorker.trace
    def display_list(self, quotes: list[dict], *keys: str):
        """
        Displays list of quotes.
        :param quotes: list of quotes to display.
        :param keys: keys to display from quote.
        """
        return ''.join([self.QUOTES_DISPLAY.format(self.display_quote(quote, *keys)) for quote in quotes])


class PhotoJsonWorker(JSONWorker):
    """
    Provides access to the photo file.
    """
    ALBUM_ID = 'albumId'
    SONG_ID = 'id'
    ALBUM_FORMAT = "AlbumId = {0}:\n{1}"
    SONG_FORMAT = "\ttitle = {0}\n\turl = {1}\n\tthumbnailUrl = {2}\n" + '-' * 50
    SONG_NOT_FOUND = 'There is no song with id {0} in album {1}.'
    TITLE = 'title'
    URL = 'url'
    THUMBNAIL_URL = 'thumbnailUrl'

    def data(self):
        return self.json_data

    def source(self):
        return f'{getcwd()}/photos.json'

    @JSONWorker.trace
    def get_albums_info(self, album_id: int) -> str:
        """
        Gets all song from the album, found by id.
        :param album_id: id of the album.
        :returns: string representation of the album.
        """
        return self.ALBUM_FORMAT.format(album_id, ''.join(self.SONG_FORMAT.format(song[self.TITLE],
                                                                                  song[self.URL],
                                                                                  song[self.THUMBNAIL_URL])
                                                          for song in self.get_albums(album_id)))

    def get_albums(self, album_id: int) -> list[dict]:
        """
        Gets all albums by id.
        :param album_id: id of the album.
        :returns: list of albums with specified id.
        """
        return [album for album in self.json_data if album[self.ALBUM_ID] == album_id]

    def get_song(self, album_id: int, song_id: int):
        """
        Gets song from the album by id.
        :param album_id: id of the album.
        :param song_id: id of the song.
        :returns: song from the specified album.
        """
        return next(filter(lambda song: song[self.SONG_ID] == song_id, self.get_albums(album_id)), None)

    @JSONWorker.trace
    def get_song_info(self, album_id: int, song_id: int):
        """
        Gets information about the song.
        :param album_id: id of the album.
        :param song_id: id of the song.
        :returns: string representation of the song.
        """
        song = self.get_song(album_id, song_id)
        return self.SONG_FORMAT.format(song[self.TITLE], song[self.URL], song[self.THUMBNAIL_URL]) \
            if song else self.SONG_NOT_FOUND.format(song_id, album_id)


def scrap():
    scrapper_crypto = JsonFileScrapper()
    scrapper_photo = JsonFileScrapper()

    scrapper_crypto.save("https://www.cryptingup.com/api/markets", f"{getcwd()}\\crypto")
    scrapper_photo.save("https://jsonplaceholder.typicode.com/photos", f"{getcwd()}\\photos")


IS_SCRAPPED = False


def main():
    if IS_SCRAPPED:
        scrap()

    crypto_worker = CryptoJsonWorker()
    crypto_worker.display_list(crypto_worker.order_by(crypto_worker.CREATED, descending=True),
                               crypto_worker.SYMBOL, crypto_worker.CREATED)
    crypto_worker.get_total_volume(crypto_worker.get_quote('USDT-USD'))

    photo_worker = PhotoJsonWorker()
    photo_worker.get_albums_info(1)
    photo_worker.get_song_info(1, 10)
    photo_worker.save()


if __name__ == "__main__":
    main()
