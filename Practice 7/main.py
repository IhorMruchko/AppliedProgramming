import json
import os
import sys
from json import JSONDecodeError
from os import path
from sys import argv, orig_argv
import ctypes.wintypes
from time import sleep


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

    def __init__(self):
        self.files_to_open: dict = PathManager.load_object(self.FILES_TO_EDIT_FILE_NAME, {})

    def add(self, name: str, value: str = None) -> str:
        key = name.lower()
        if key not in self.files_to_open:
            print(self.files_to_open)
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
        if key not in self.files_to_open:
            return self.SCENARIO_NOT_FOUND.format(key)

        for editable in self.files_to_open[key]:
            os.startfile(editable)

    def remove(self, name: str, rem: str | int | None) -> str:
        key = name.lower()
        if key not in self.files_to_open[key]:
            return self.SCENARIO_NOT_FOUND.format(key)

        if rem is None:
            self.files_to_open.pop(key)
            return self.SCENARIO_REMOVED.format(key)

        if isinstance(rem, str) and rem in self.files_to_open[key]:
            self.files_to_open[key].remove(rem)
            PathManager.save_object(self.FILES_TO_EDIT_FILE_NAME, self.files_to_open)
            return self.FILE_REMOVED.format(rem, key)

        if isinstance(rem, int):
            removed = self.files_to_open[key][rem % len(self.files_to_open[key])]
            self.files_to_open[key].remove(removed)
            return self.FILE_REMOVED.format(removed, key)

        return self.FILE_NOT_IN_LIST.format(rem, key)


class ScenarioRunner:
    """
    file add (name) [source]
    file remove (name) [source]
    file run (name)
    """

    @staticmethod
    def execute(*args: str) -> str:
        print(*args)
        if len(args) == 0:
            return 'Something went wrong \\_^^_/'
        if args[0] == 'file':
            return ScenarioRunner.run_file(*args[1:])

    @staticmethod
    def run_file(*args: str) -> str:
        file_runner = FileEditor()
        if len(args) == 0:
            return 'Something went wrong \\_^^_/'
        if args[0] == 'add' and 2 <= len(args) <= 3:
            return file_runner.add(args[1], args[2] if len(args) == 3 else None)
        if args[0] == 'remove' and 2 <= len(args) <= 3:
            return file_runner.remove(args[1], args[2] if len(args) == 3 else None)
        if args[0] == 'run' and len(args) == 2:
            return file_runner.run(args[1])

        return 'Command not found.'


def main():
    print(ScenarioRunner.execute(*sys.argv))


if __name__ == '__main__':
    main()
