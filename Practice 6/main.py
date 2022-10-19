import os
import time
from datetime import datetime
from enum import Enum


class FileType(Enum):
    Doc = ('.doc', '.docx')
    PDF = ('.pdf', '.djv')
    Image = ('.jpeg', '.png', '.gif')
    Programs = ('.py', '.dll', '.exe')
    Transfers = ('.json', '.xml')
    Text = ('.txt', '.txt')
    Folders = ('', '')


class FileManager:
    """
    Provides access to the files' management.

    TIME_SELECTOR - provides connection between strings and methods that gets information about the time of the file.
    """
    TIME_SELECTOR = {
        ('c', 'creation', 'create'): os.path.getctime,
        ('m', 'modification', 'mod'): os.path.getmtime,
        ('a', 'access', 'acs'): os.path.getatime
    }

    @staticmethod
    def get_time_selector(_time: str):
        """
        Gets time selector basing on the input parameter.

        :param _time: string value of the time is user interested in. Might be one of the literals:
                    ['c', 'creation', 'create', 'm', 'modification', 'mod', 'a', 'access', 'acs']
        :raise :
        :returns: time selector of the time of the creation or modification or access.
        """
        for key, value in FileManager.TIME_SELECTOR.items():
            if _time in key:
                return value
        raise ValueError("Time selector string mus be of of the literals: "
                         "'c', 'creation', 'create', 'm', 'modification', 'mod', 'a', 'access', 'acs'. "
                         f"Instead {_time}")

    @staticmethod
    def is_type_matches(file_types: tuple[str] | str | FileType, file_type: str):
        """
        Checks is file type is fit finding file types.

        :raises TypeError: file types must be only string-tuple, string or FileType enum.
        :returns: True - if file type is in or equal file_types. False - otherwise.
        """
        if isinstance(file_types, tuple):
            return file_type in file_types
        if isinstance(file_types, FileType):
            return file_type in file_types.value
        if isinstance(file_types, str):
            return file_type == file_types

        raise TypeError(f'file_types can be only string-tuple, string or FileType enum. Instead {type(file_types)}')

    @staticmethod
    def get_file_type(file_types: tuple[str] | str | FileType) -> str:
        """
        Gets proper string representation for the type.

        :raises TypeError: file types must be only string-tuple, string or FileType enum.
        :returns: formatted string of the type(s) to find.
        """
        if isinstance(file_types, tuple):
            return ','.join(set(file_types))
        if isinstance(file_types, FileType):
            return ','.join(set(file_types.value))
        if isinstance(file_types, str):
            return file_types

        raise TypeError(f'file_types can be only string-tuple, string or FileType enum. Instead {type(file_types)}')

    @staticmethod
    def order_files_by_date(dir_path: str, _time: str = "creation", reverse: bool = False) -> list[tuple]:
        """
        Orders the files in the folder by the time.

        :param dir_path: path of the directory to sort file in.
        :param _time: value of the time selector. Might be one of the literals:
                    ['c', 'creation', 'create', 'm', 'modification', 'mod', 'a', 'access', 'acs'].
                    Default - creation.
        :param reverse: defines is sorting by descending or ascending. Default - ascending.
        """
        time_selector = FileManager.get_time_selector(_time)
        return sorted([(time_selector(os.path.join(dir_path, element)), element)
                       for element in os.listdir(dir_path)], key=lambda item: item[0],
                      reverse=reverse)

    @staticmethod
    def find_duplicates(*file_path: str) -> dict:
        """
        Finds file duplicates in the specified directories.

        :param file_path: list of the directories to search file.
        :returns: dictionary in format: [name of the file][file size][path of the file].
        """
        same_named_files = list(set.intersection(*[set(os.listdir(path)) for path in file_path]))
        result = {}
        for file_name in same_named_files:
            if file_name not in result:
                result[file_name] = {}
            for path in file_path:
                size = os.path.getsize(os.path.join(path, file_name))
                if size not in result[file_name]:
                    result[file_name][size] = []
                result[file_name][size].append(path)

        return result

    @staticmethod
    def find_by_type(file_types: tuple[str] | str | FileType, *file_path: str) -> dict:
        """
        Forms dictionary of the directory and file names that match the type.

        :param file_types: type of the file to filter by.
        :param file_path: paths where files are located.
        :returns: dictionary of the directory and the file of the type.
        """
        return {directory: [file_name for file_name in os.listdir(directory)
                            if FileManager.is_type_matches(file_types, os.path.splitext(file_name)[1])]
                for directory in file_path}

    @staticmethod
    def group_by_type(file_path: str) -> dict:
        """
        Groups elements in the selected folder by the file type.

        :param file_path: folder from where files are grouped.
        :returns: dictionary, where format of the file is the key and value is an absolute path to the file.
        """
        files = os.listdir(file_path)
        result = {}
        for file_name in files:
            _, file_type = os.path.splitext(file_name)
            if file_type not in result:
                result[file_type] = []
            result[file_type].append(os.path.join(file_path, file_name))
        return result


class TaskSolver:
    """
    Provides access to the task solution.
    """
    FIRST_TASK_RESPONSE_FORMAT = '{0} recent files:\n\t{1}\n{0} older files:\n\t{2}'
    FILE_TIME_FORMAT = '{0} ({1:%d/%m/%Y %H:%m:%S}).'
    SECOND_TASK_RESPONSE_FORMAT = '{0} ({1}) are in:\n\t{2}'
    THIRD_TASK_RESPONSE_FORMAT = 'Files of type {0} in {1} are:\n\t{2}'

    @staticmethod
    def top_bottom_files_date(file_path: str, _time: str = 'creation', take: int = 2):
        """
        Gets information about concrete amount of the file from the bottom and the top of the sorted files by date.

        :param file_path: path of the directory to sort file in.
        :param _time: value of the time selector. Might be one of the literals:
                    ['c', 'creation', 'create', 'm', 'modification', 'mod', 'a', 'access', 'acs'].
                    Default - creation.
        :param take: amount to take from the top and list bottom. Default - 2.
        :returns: formatted string for the information about concrete amount of the recent and oldest file.
        """
        files = FileManager.order_files_by_date(file_path, _time=_time, reverse=True)
        return TaskSolver.FIRST_TASK_RESPONSE_FORMAT.format(
            take,
            '\n\t'.join(TaskSolver.FILE_TIME_FORMAT.format(item[1], datetime.fromtimestamp(
                time.mktime(time.gmtime(item[0])))) for item in files[:take]),
            '\n\t'.join(TaskSolver.FILE_TIME_FORMAT.format(item[1], datetime.fromtimestamp(
                time.mktime(time.gmtime(item[0])))) for item in files[-1:-take - 1:-1]))

    @staticmethod
    def find_duplicated_file(*file_path: str):
        """
        Gets information of the duplicated files from the file paths.

        :param file_path: file directories to find duplicates from.
        :returns: formatted response for the query in format file_name(size): list of the paths.
        """
        parsed_data = FileManager.find_duplicates(*file_path)
        return '\n'.join(TaskSolver.SECOND_TASK_RESPONSE_FORMAT.format(name, size, '\n\t'.join(parsed_data[name][size]))
                         for name in parsed_data.keys()
                         for size in parsed_data[name].keys()
                         if len(parsed_data[name][size]) > 1)

    @staticmethod
    def find_by_type(file_types: tuple | str | FileType, *file_path: str):
        """
        Gets information about files of the specified type.

        :param file_types: types of the file should filter. May be string-tuple, string or FileType enum.
        :param file_path: all file paths to search in.
        :returns: formatted information about type to found and full path to the files that matches this type.
        """
        dictionary = FileManager.find_by_type(file_types, *file_path)
        return '\n'.join(TaskSolver.THIRD_TASK_RESPONSE_FORMAT.format(FileManager.get_file_type(file_types),
                                                                      directory,
                                                                      '\n\t'.join(dictionary[directory]))
                         for directory in dictionary
                         if len(dictionary[directory]) > 0)

    @staticmethod
    def sort_by_type(*file_path: str):
        """
        Sorts file for all directories.

        :param file_path: list of the directories to sort files by type.
        """
        for path in file_path:
            group = FileManager.group_by_type(path)
            for key, value in group.items():
                if key == '':
                    continue
                folder = os.path.join(path, key[1:].upper())
                os.mkdir(folder)
                for file in value:
                    os.replace(file, os.path.join(folder, os.path.split(file)[1]))


def main():
    print(TaskSolver.sort_by_type(r'E:\Programming\Prolog\Practice\Homework',
                                  r'E:\Programming',
                                  r'C:\Users\Lenovo\Documents'))


if __name__ == '__main__':
    main()
