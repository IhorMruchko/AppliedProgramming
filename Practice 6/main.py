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
    Common = ('.txt', '.txt')
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
        if isinstance(file_types, tuple):
            return ','.join(file_types)
        if isinstance(file_types, FileType):
            return ','.join(file_types.value)
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
        return {directory: [file_name for file_name in os.listdir(directory)
                            if FileManager.is_type_matches(file_types, os.path.splitext(file_name)[1])]
                for directory in file_path}

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
    def find_by_type(file_types: tuple[str] | str | FileType, *file_path: str):
        dictionary = FileManager.find_by_type(file_types, *file_path)
        return '\n'.join(TaskSolver.THIRD_TASK_RESPONSE_FORMAT.format(FileManager.get_file_type(file_types),
                                                                      directory,
                                                                      '\n\t'.join(dictionary[directory]))
                         for directory in dictionary
                         if len(dictionary[directory]) > 0)


def main():
    print(TaskSolver.find_by_type(FileType.Image,
                                   r'D:\Studying\4 grade\Information security\Практичні',
                                   r'D:\Studying\4 grade\Ukrainian language',
                                   r'C:\Users\Lenovo\Documents',
                                   r'E:\OperaDownload'))
    print(TaskSolver.find_duplicated_file(r'E:\Programming\Python\AppliedProgramming\Practice 1',
                                          r'E:\Programming\Python\AppliedProgramming\Practice 2',
                                          r'E:\Programming\Python\AppliedProgramming\Practice 3',
                                          r'E:\Programming\Python\AppliedProgramming\Practice 4',
                                          r'E:\Programming\Python\AppliedProgramming\Practice 5',
                                          r'E:\Programming\Python\AppliedProgramming\Practice 6'))

    print(TaskSolver.find_duplicated_file(r'E:\Programming\Prolog\Practice',
                                          r'E:\Programming\Prolog\Practice\Homework'))


if __name__ == '__main__':
    main()
