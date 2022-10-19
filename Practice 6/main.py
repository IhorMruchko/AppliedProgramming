import os
import time
from datetime import datetime


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
    def get_time_selector(time: str):
        """
        Gets time selector basing on the input parameter.

        :param time: string value of the time is user interested in. Might be one of the literals:
                    ['c', 'creation', 'create', 'm', 'modification', 'mod', 'a', 'access', 'acs']
        :raise :
        :returns: time selector of the time of the creation or modification or access.
        """
        for key, value in FileManager.TIME_SELECTOR.items():
            if time in key:
                return value
        raise ValueError("Time selector string mus be of of the literals: "
                         "'c', 'creation', 'create', 'm', 'modification', 'mod', 'a', 'access', 'acs'. "
                         f"Instead {time}")

    @staticmethod
    def order_files_by_date(dir_path: str, time: str = "creation", reverse: bool = False) -> list[tuple]:
        """
        Orders the files in the folder by the time.

        :param dir_path: path of the directory to sort file in.
        :param time: value of the time selector. Might be one of the literals:
                    ['c', 'creation', 'create', 'm', 'modification', 'mod', 'a', 'access', 'acs'].
                    Default - creation.
        :param reverse: defines is sorting by descending or ascending. Default - ascending.
        """
        time_selector = FileManager.get_time_selector(time)
        return sorted([(time_selector(os.path.join(dir_path, element)), element)
                                            for element in os.listdir(dir_path)], key=lambda item: item[0],
                                           reverse=reverse)


class TaskSolver:
    """
    Provides access to the task solution.
    """
    FIRST_TASK_RESPONSE_FORMAT = '{0} recent files:\n\t{1}\n{0} older files:\n\t{2}'
    FILE_TIME_FORMAT = '{0} ({1:%d/%m/%Y %H:%m:%S}).'

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
        files = FileManager.order_files_by_date(file_path, time=_time, reverse=True)
        return TaskSolver.FIRST_TASK_RESPONSE_FORMAT.format(
            take,
            '\n\t'.join(TaskSolver.FILE_TIME_FORMAT.format(item[1], datetime.fromtimestamp(
                time.mktime(time.gmtime(item[0])))) for item in files[:take]),
            '\n\t'.join(TaskSolver.FILE_TIME_FORMAT.format(item[1], datetime.fromtimestamp(
                time.mktime(time.gmtime(item[0])))) for item in files[-1:-take-1:-1]))


def main():
    print(TaskSolver.top_bottom_files_date(r'E:\Programming\Prolog\Practice\Homework', take=3, _time='m'))


if __name__ == '__main__':
    main()
