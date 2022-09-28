import sys
from datetime import datetime
from enum import Enum
from os import getcwd, path


# region Testing


class Case:
    """
    Represents the smallest piece of the test.
    """

    SUCCESS = "✔"
    FAIL = "❌ (Expected {0}, but was {1})."
    EXCEPTION = "Unhandled exception {0}."

    def __init__(self, target):
        """
        Initiates case.

        :param target: function to test.
        """
        self.expected = None
        self.target = target

    def run(self, input_data) -> str:
        """
        Executes target of the case with input_data.

        :param input_data: data to test target with.
        :return: data log of the test passing.
        """
        data_log = ""
        try:
            result = self.target(input_data)
            data_log += self.SUCCESS if result == self.expected else self.FAIL.format(self.expected, result)
        except Exception as e:
            data_log += self.SUCCESS if type(self.expected) == type(e) and self.expected.args == e.args \
                else self.EXCEPTION.format(e)
        return data_log


class Test:
    """
    Represents pies of the test with common input for different cases.
    """

    def __init__(self, title: str):
        """
        Initiates Test with the title.

        :param title: title of the test
        """
        self.title = title
        self.input_data = None
        self.cases: list[Case] = []

    def add(self, case: Case):
        """
        Adds case to the test cases.

        :param case: case to add.
        :return: this test.
        """
        self.cases.append(case)
        return self

    def run(self):
        """
        Executes each case with input_data.

        :return: data log of the execution.
        """
        data_log = self.title
        for case in self.cases:
            data_log += '\n\t' + case.run(self.input_data)
        return data_log


class Tester:
    """
    Represents tests container that perform testing.

    Requirements:
    All === signs must have closing one signs.
    Amount of the tests (data between ===) must be equal to predefined tests amount. (amount of used add_test()).
    Amount of the test's cases must be equal to predefined test's cases amount (amount of used add_case()).

    Acceptable file format:
    ===
    Input: [value in python declaration way].
    Case: expected result for case 1.
    Case: expected result for case 2.
    ...
    ===
    Input:
    Case:
    ...
    ===
    """
    
    TEST_DELIMITER = "==="
    INPUT_TAG = "Input:"
    CASE_TAG = "Case:"

    def __init__(self, filepath: str):
        """
        Initiate tests container with filepath.

        :param filepath: path to the input data file.
        :exception FileExistsError: File is not exists.
        """
        if not path.exists(filepath):
            raise FileExistsError(f"File {filepath} does not exists")
        self.__filepath = filepath
        self.__tests: list[Test] = []

    def add_test(self, title: str = None):
        """
        Adds test to the container.

        :param title: Title of the test. If None - generates title as Test [number of the test].
        :return: Updated test container.
        """
        self.__tests.append(Test(f"Test {len(self.__tests) + 1}" if title is None else title))
        return self

    def add_case(self, target):
        """
        Add to the last test in the container new case.

        :param target: Function to test.
        :return: Updated test container.
        :exception IndexError: Adding case to empty test container.
        """
        if not self.__tests:
            raise IndexError("Cannot add case, because there is no any test!")
        self.__tests[-1].add(Case(target))
        return self

    def run(self):
        """
        Execute all tests and saves the data log.
        """
        self.parse_test()
        data_log = "=" * 50 + '\n'
        for test in self.__tests:
            data_log += test.run() + '\n' + "=" * 50 + '\n'

        self.save(data_log)

    @staticmethod
    def save(data_log) -> None:
        """
        Saves data log to the file.

        :param data_log: data log to save.
        """
        file_to_save = f"{getcwd()}\\testing" + \
                       f"_{datetime.now().strftime('%Y_%d_%m_%H_%M_%S')}.txt"
        with open(file_to_save, 'w+', encoding="utf-8") as file:
            file.write(data_log)

    def parse_test(self) -> None:
        """
        Reads all test from the file and validate formatting.

        :exception EOFError: Cannot find closing test delimiter.
        """
        with open(self.__filepath, 'r', encoding="utf-8") as file:
            lines = [line.strip() for line in file.readlines() if len(line.strip()) > 0]

        if lines[-1] != self.TEST_DELIMITER:
            raise EOFError(f"Cannot find closing {self.TEST_DELIMITER}")

        tests = self.parse_tests(lines)
        self.format_tests(tests)

    def parse_tests(self, lines: list[str]) -> list[list[str]]:
        """
        Get test information about input and cases.

        :param lines: Text read from the file.
        :return: list of the data for each test.
        """
        delimiter_indexes = [i for i in range(len(lines)) if lines[i].strip() == self.TEST_DELIMITER]
        if len(delimiter_indexes) - 1 != len(self.__tests):
            raise ReferenceError(f"Tests cannot be bind with data in {self.__filepath}. "
                                 f"Expected tests: {len(self.__tests)} but was {len(delimiter_indexes) - 1}.")
        return [lines[delimiter_indexes[i] + 1: delimiter_indexes[i + 1]] for i in range(len(delimiter_indexes) - 1)]

    def format_tests(self, tests: list[list[str]]):
        """
        Formats input lines as needed test components (case, input).

        :param tests: list of the data for each test.
        :exception SyntaxError: One input per test.
        :exception ReferenceError: Mismatch case amount in the file and predefined in the test.
        """
        for i, test in enumerate(tests):
            inputs_amount = len([sw for sw in test if sw.startswith(self.INPUT_TAG)])
            cases = [sw.strip(self.CASE_TAG) for sw in test if sw.startswith(self.CASE_TAG)]
            case_amount = len(cases)

            if inputs_amount != 1:
                raise SyntaxError(f"One test should contain one input row. {inputs_amount}.")

            if len(self.__tests[i].cases) != case_amount:
                raise ReferenceError(f"Test must contains {len(self.__tests[i].cases)}. Instead {case_amount}")

            self.__tests[i].input_data = eval(test[0].strip(self.INPUT_TAG))
            for index, case in enumerate(self.__tests[i].cases):
                case.expected = eval(cases[index])


# endregion

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


def is_odd(value: int) -> bool:
    """
    Defines is value is odd.

    :param value: value to define/
    :return: True - if value is odd. False - otherwise.
    """
    return value % 2 == 1


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


def define_triangle_type(a: float, b: float, c: float) -> str:
    """
    Defines type of the triangle based on the sides' equality.

    :param a: first triangle side.
    :param b: second triangle side.
    :param c: third triangle side.
    :return: type of the triangle.
    """
    return TriangleType.Equilateral.value if a == b == c \
        else TriangleType.Isosceles.value if a == b or a == c or c == b \
        else TriangleType.Scalene.value


def triangle_solution(a: float, b: float, c: float) -> TriangleType:
    """
    Defines are sides segments of the triangle, and it's type.

    :param a: first triangle side.
    :param b: second triangle side.
    :param c: third triangle side.
    :return: type of the triangle.
    """
    return define_triangle_type(a, b, c) if is_triangle(a, b, c) else TriangleType.NotATriangle.value


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
    if len(matrix) == 0 or len([item for item in matrix if len(item) != len(matrix)]) != 0:
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
            for j in range(rectangle_size[2], rectangle_size[3] + 1)]
            for i in range(rectangle_size[0], rectangle_size[1] + 1)]


# endregion


def main():
    tester = \
        Tester("testCases.txt") \
        .add_test("List filtering testing") \
        .add_case(lambda case: filter_and_operate_list(case, operator=len, predicate=is_positive)) \
        .add_case(lambda case: filter_and_operate_list(case, operator=len, predicate=is_negative)) \
        .add_case(lambda case: filter_and_operate_list(case, operator=average, predicate=is_negative)) \
        .add_test("List filtering testing with exception") \
        .add_case(lambda case: filter_and_operate_list(case, operator=len, predicate=is_positive)) \
        .add_case(lambda case: filter_and_operate_list(case, operator=len, predicate=is_negative)) \
        .add_case(lambda case: filter_and_operate_list(case, operator=average, predicate=is_negative)) \
        .add_test("Rectangle") \
        .add_case(lambda case: triangle_solution(case[0], case[1], case[2])) \
        .add_test() \
        .add_case(lambda case: triangle_solution(case[0], case[1], case[2])) \
        .add_test() \
        .add_case(lambda case: triangle_solution(case[0], case[1], case[2])) \
        .add_test() \
        .add_case(lambda case: triangle_solution(case[0], case[1], case[2])) \
        .add_test("Sentence rebuilding test") \
        .add_case(lambda case: connect_sentence(case)) \
        .add_test() \
        .add_case(lambda case: find_max_sum_subrectangle(case)) \
        .add_test() \
        .add_case(lambda case: find_max_sum_subrectangle(case)) \
        .add_test() \
        .add_case(lambda case: find_max_sum_subrectangle(case)) \

    tester.run()


if __name__ == '__main__':
    main()
