import ctypes.wintypes
import json
import os
import sys
from enum import Enum
from json import JSONDecodeError
from os import path


class Mode(Enum):
    DEBUG = 'debug'
    RELEASE = 'release'


class PathManager:
    FOLDER_TO_SAVE_FILES = 5
    CURRENT_FOLDER = 0
    STORAGE = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(0, 5, 0, 0, STORAGE)
    STORAGE = STORAGE.value

    @classmethod
    def save_object(cls, file_name: str, obj):
        with open(path.join(cls.STORAGE, file_name), 'w+') as storage:
            storage.write(json.dumps(obj, indent=4))

    @classmethod
    def load_object(cls, file_name: str, default=None):
        try:
            with open(path.join(cls.STORAGE, file_name), 'r') as storage:
                return json.load(storage)
        except FileNotFoundError:
            with open(path.join(cls.STORAGE, file_name), 'w'):
                return default
        except JSONDecodeError:
            return default


class FileEditor:
    FILES_TO_EDIT_FILE_NAME = 'editable.json'
    SCENARIO_ONLY_CREATED = 'Edit scenario is created.'
    SCENARIO_REMOVED = 'Scenario {0} was removed.'
    ADDED_NEW_FILE_TO_EDIT = 'To {0} was added {1}.'
    SCENARIO_NOT_FOUND = 'Cannot find a scenario with name {0}.'
    VALUE_ALREADY_IN_LIST = 'Value [{0}] is already in scenario {1}.'
    FILE_IS_NOT_EXISTS = 'File can not be located with path [{0}].'
    FILE_REMOVED = 'File [{0}] was removed from {1}.'
    FILE_NOT_IN_LIST = 'File [{0}] is not in {1}.'
    RUN_IS_FAILED = 'Exception ({0}) was thrown while running [{1}].'
    RUN_IS_SUCCESS = '[{0}] was run.'

    CONNECTOR = '\n\t'

    def __init__(self):
        self.files_to_open: dict = PathManager.load_object(self.FILES_TO_EDIT_FILE_NAME, {})

    def add(self, name: str, value: str = None) -> str:
        key = name.lower()
        if key not in self.files_to_open:
            self.files_to_open[key] = []

        if value is None:
            PathManager.save_object(self.FILES_TO_EDIT_FILE_NAME, self.files_to_open)
            return self.SCENARIO_ONLY_CREATED

        if not path.exists(value):
            return self.FILE_IS_NOT_EXISTS.format(value)

        if value in self.files_to_open[key]:
            PathManager.save_object(self.FILES_TO_EDIT_FILE_NAME, self.files_to_open)
            return self.VALUE_ALREADY_IN_LIST.format(value, key)

        self.files_to_open[key].append(value)
        PathManager.save_object(self.FILES_TO_EDIT_FILE_NAME, self.files_to_open)
        return self.ADDED_NEW_FILE_TO_EDIT.format(key, value)

    def run(self, name: str) -> str:
        key = name.lower()
        response = ""
        if key not in self.files_to_open:
            return self.SCENARIO_NOT_FOUND.format(key)

        for editable in self.files_to_open[key]:
            try:
                os.startfile(editable)
            except Exception as e:
                response += self.RUN_IS_FAILED.format(e, editable)
            else:
                response += self.RUN_IS_SUCCESS.format(editable)
        return response

    def remove(self, name: str, rem: str | int | None) -> str:
        key = name.lower()
        if key not in self.files_to_open:
            return self.SCENARIO_NOT_FOUND.format(key)

        if rem is None:
            self.files_to_open.pop(key)
            PathManager.save_object(self.FILES_TO_EDIT_FILE_NAME, self.files_to_open)
            return self.SCENARIO_REMOVED.format(key)

        if all(str.isnumeric(item) for item in rem) and len(self.files_to_open[key]) > 0:
            removed = self.files_to_open[key][(abs(int(rem)) - 1) % len(self.files_to_open[key])]
            self.files_to_open[key].remove(removed)
            PathManager.save_object(self.FILES_TO_EDIT_FILE_NAME, self.files_to_open)
            return self.FILE_REMOVED.format(removed, key)

        if isinstance(rem, str) and rem in self.files_to_open[key]:
            self.files_to_open[key].remove(rem)
            PathManager.save_object(self.FILES_TO_EDIT_FILE_NAME, self.files_to_open)
            return self.FILE_REMOVED.format(rem, key)

        return self.FILE_NOT_IN_LIST.format(rem, key)

    def show(self, name: str | None) -> str:
        return '\n'.join(f'{key}:\n\t{self.CONNECTOR.join(value)}' for key, value in self.files_to_open.items()) \
            if name is None else f'{name}:\n\t{self.CONNECTOR.join(self.files_to_open[name.lower()])}' \
            if name.lower() in self.files_to_open \
            else self.SCENARIO_NOT_FOUND.format(name)


class ScenarioRunner:
    """
    file add (name) [source]
    file remove (name) [source]
    file open (name)
    file list [name]
    """

    @staticmethod
    def execute(*args: str) -> str:
        if len(args) == 0:
            return 'Something went wrong \\_^^_/'
        if args[0] == 'file':
            return ScenarioRunner.run_file(*args[1:])
        return 'Something went wrong \\_^^_/'

    @staticmethod
    def run_file(*args: str) -> str:
        file_runner = FileEditor()
        if len(args) == 0:
            return 'Something went wrong \\_^^_/'
        if args[0] == 'add' and 2 <= len(args) <= 3:
            return file_runner.add(args[1], args[2] if len(args) == 3 else None)
        if args[0] == 'remove' and 2 <= len(args) <= 3:
            return file_runner.remove(args[1], args[2] if len(args) == 3 else None)
        if args[0] == 'open' and len(args) == 2:
            return file_runner.run(args[1])
        if args[0] == 'list' and 1 <= len(args) <= 2:
            return file_runner.show(args[1] if len(args) == 2 else None)

        return 'Command not found.'


def main():
    mode = Mode.RELEASE
    arguments = input('>>>').split() if mode == Mode.DEBUG else sys.argv[1:]
    print(ScenarioRunner.execute(*arguments))


if __name__ == '__main__':
    main()
