import sys
from datetime import datetime
from os import getcwd
from random import randint
from enum import Enum


# region List task


def is_positive(value: int) -> bool:
    """
    Defines is value is positive.

    :param value: value to define is positive.
    :return: True if value is positive; False - otherwise.
    """
    return value > 0


def is_negative(value: int) -> bool:
    """
    Defines is value is negative.

    :param value: value to define is negative.
    :return: True if value is negative; False - otherwise.
    """
    return value < 0


def average(data: list) -> float:
    """
    Return average of the list.

    :param data: list to find average.
    :return: average value of the list.
    """
    return sum(data) / len(data)


def filter_list(data: list, predicate=is_positive):
    """
    Filters given data based on predicate

    :param data: list to filter.
    :param predicate: filtering rule.
    :return: list with elements from @param:data
    """
    return [value for value in data if predicate(value)]


def filter_and_operate_list(data: list, predicate=is_positive, operator=average) -> float:
    """
    Returns result of the operation on the filtered list.

    :param data: list to filter and operate on.
    :param predicate: filtering rule
    :param operator: function to operate on list.
    :raise ValueError: last element has to be zero.
    :return:
    """
    if data[-1] != 0:
        raise ValueError(f"Last value of the list must be zero, instead {data[-1]}")

    return operator(filter_list(data, predicate))


# endregion List operations

# region Triangle task

class TriangleType(Enum):
    """
    Represents types of the triangles based on sides equality.
    """
    Equilateral = "Рівносторонній"
    Isosceles = "Рівнобедрений"
    Scalene = "Довільний"
    NotATriangle = "Не трикутник"


def is_segments(a: float, b: float, c: float) -> bool:
    """
    Defines are lengths segments.

    :param a: first possible segment.
    :param b: second possible segment.
    :param c: third possible segment.
    :return: True - if all parameters are greater than zero. False - otherwise.
    """
    return len([segment for segment in [a, b, c]]) == 3


def is_triangle(a: float, b: float, c: float) -> bool:
    """
    Defines are lengths can create a triangle.

    :param a: first possible triangle side.
    :param b: second possible triangle side.
    :param c: third possible triangle side.
    :return: True - if all parameters are segments and the greater side is less or equal than sum of two other sides.
    """
    sort = sorted([a, b, c], reverse=True)
    return is_segments(a, b, c) and sort[0] <= sort[1] + sort[2]


def define_triangle_type(a: float, b: float, c: float) -> TriangleType:
    """
    Defines type of the triangle based on the sides' equality.

    :param a: first triangle side.
    :param b: second triangle side.
    :param c: third triangle side.
    :return: type of the triangle.
    """
    return TriangleType.Equilateral if a == b == c \
        else TriangleType.Isosceles if a == b or a == c or c == b \
        else TriangleType.Scalene


def triangle_solution(a: float, b: float, c: float) -> TriangleType:
    """
    Defines are sides segments of the triangle, and it's type.

    :param a: first triangle side.
    :param b: second triangle side.
    :param c: third triangle side.
    :return: type of the triangle.
    """
    return define_triangle_type(a, b, c) if is_triangle(a, b, c) else TriangleType.NotATriangle


# endregion

# region Sentence task


def split_sentence(sentence: str) -> list[str]:
    """
    Splits sentence by spaces, removing all punctuation chars.

    :param sentence: sentence to split.
    :return: separated sentence.
    """
    return sentence.translate(str.maketrans('', '', '!"#$%&()*+,-./:;<=>?@[\\]^_{|}~')).split(' ')


def connect_sentence(sentence: str, connector='\n') -> str:
    """
    Splits and reconnects sentence with connector.

    :param sentence: sentence to split and reconnect.
    :param connector: value to connect sentence with.
    :return: reconnected sentence.
    """
    return connector.join(split_sentence(sentence))


# endregion

# region Matrix task


def to_string(matrix: list[list[int]]) -> str:
    """
    Represents matrix in the more readable form.

    :param matrix: matrix to represent.
    :return: string representation of the matrix.
    """
    return '\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in matrix])


def possible_rectangle_sizes(size: int) -> list[(int, int, int, int)]:
    """
    Generates possible rectangle sizes.

    :param size: size of the parent matrix.
    :return: list of the tuples (start of the row, end of the row, start of the column, end of the column)
    """
    return [(row_start, row_end, column_start, column_end)
            for row_start in range(size)
            for row_end in range(row_start, size)
            for column_start in range(size)
            for column_end in range(column_start, size)
            if row_end - row_start != column_end - column_start]


def generate_sums(matrix: list[list[int]]) -> list[list[int]]:
    """
    Generates helping matrix, where sum of the element in the matrix from (0, 0) to (i-1, j-1) are stored.

    :param matrix: matrix to preprocess.
    :return: matrix, with dim = dim(matrix) + 1 and contains proper sum.
    """
    sum_size = len(matrix) + 1
    sum_sub_matrix = [[0 for _ in range(sum_size)] for _ in range(sum_size)]

    for i in range(1, sum_size):
        for j in range(1, sum_size):
            sum_sub_matrix[i][j] = sum_sub_matrix[i - 1][j] + \
                                   sum_sub_matrix[i][j - 1] - \
                                   sum_sub_matrix[i - 1][j - 1] + \
                                   matrix[i - 1][j - 1]

    return sum_sub_matrix


def find_max_sum_subrectangle(matrix: list[list[int]]) -> list[list[int]]:
    """
    Finds subrectangle of the matrix with the largest sum.

    :param matrix: matrix to find in.
    :return: subrectangle with the largest sum.
    """
    if not (matrix and len(matrix)):
        return []

    size, sum_size, result_sum, rectangle_size = len(matrix), len(matrix) + 1, -sys.maxsize, (-1, -1, -1, -1)
    sum_of_sub_rectangles = generate_sums(matrix)

    for possible_size in possible_rectangle_sizes(size):
        subrectangle_sum = sum_of_sub_rectangles[possible_size[1] + 1][possible_size[3] + 1] - \
                           sum_of_sub_rectangles[possible_size[1] + 1][possible_size[2]] - \
                           sum_of_sub_rectangles[possible_size[0]][possible_size[3] + 1] + \
                           sum_of_sub_rectangles[possible_size[0]][possible_size[2]]

        if subrectangle_sum > result_sum:
            result_sum, rectangle_size = subrectangle_sum, possible_size

    return [[matrix[i][j]
             for j in range(rectangle_size[2], rectangle_size[3] + 1)
             for i in range(rectangle_size[0], rectangle_size[1] + 1)]]
# endregion


def testing(filepath: str, parser, function, title=""):
    testing_results = f"{title}:\n"
    testing_results += "\n" + "=" * 40 + "\n\n"
    with open(filepath, 'r') as file:
        test_cases = parser(file.readlines())

    for test_case in test_cases:
        testing_results += f"\tinputs: {test_case}\n"
        try:
            result = function(test_case)
            testing_results += f"\toutput: {result}\n"
        except Exception as ex:
            testing_results += f"\toutput: {ex}\n"
        testing_results += "\n" + "=" * 40 + "\n\n"

    file_to_save = f"{getcwd()}\\testing_{title.replace(' ', '_')}" + \
                   f"_{datetime.now().strftime('%Y_%d_%m_%H_%M_%S')}.txt"
    with open(file_to_save, 'w+') as file:
        file.write(testing_results)


def list_parser(data: list[str]) -> list[list[int]]:
    return [[int(value) for value in line.split(' ')] for line in data]


def main():
    testing("testCases.txt",
            list_parser,
            lambda test_case: filter_and_operate_list(test_case,
                                                      is_positive,
                                                      sum),
            title="Positive sum in the list")

    testing("testCases.txt",
            list_parser,
            lambda test_case: filter_and_operate_list(test_case,
                                                      is_negative,
                                                      sum),
            title="Negative sum in the list")

    testing("testCases.txt",
            list_parser,
            lambda test_case: filter_and_operate_list(test_case,
                                                      is_negative,
                                                      average),
            title="Negative average in the list")


if __name__ == '__main__':
    N = 3
    m = [[randint(-10, 10) for _ in range(N)] for _ in range(N)]
    print(to_string(m))
    print()
    print(to_string(find_max_sum_subrectangle(m)))
