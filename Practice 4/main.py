from inspect import stack
from unittest import TestCase, main

OPENING_PARENTHESIS = '('
CLOSING_PARENTHESIS = ')'
OPERANDS = ['x', 'y', 'z']
OPERATORS = ['+', '-']
OPENING_BRACKETS = ['(', '[', '{']
CLOSING_BRACKETS = [')', ']', '}']


class StackOverflowException(BaseException):
    """
    Represents custom exception for the stack.
    Raised in case using push method and stack is full.
    """
    def __init__(self):
        super(StackOverflowException, self).__init__("Maximum stack size reached.")


class StackIsEmptyException(BaseException):
    """
    Represents custom exception for the stack.
    Raised in case using pop method and stack is empty.
    """
    def __init__(self):
        super(StackIsEmptyException, self).__init__("Stack is empty.")


class ParenthesisMissmatchException(BaseException):
    def __init__(self, opening: int, closing: int):
        self.open = opening
        self.close = closing
        super().__init__(f'Formula contains parenthesis missmatch: {self.open} opening to {self.close} closing.')


class Stack:
    """
    Represents a structure of the LIFO principe.

    CAPACITY_MAXIMUM - value of the maximum possible stack deep.
    """
    CAPACITY_MAXIMUM = 10_000

    def __init__(self, capacity: int):
        """
        Initiates Stack with provided capacity.

        __space_used - indicator of the stack filling.
        __storage - values collector.
        """
        self.capacity = capacity
        self.__space_used = 0
        self.__storage = []

    def __str__(self):
        return f'Stack: ({self.size}/{self.capacity}) [{", ".join(self.__storage)}]'

    @property
    def is_empty(self) -> bool:
        """
        Defines is stack empty.

        :returns: True - if the size of the stack is equal to zero. False - otherwise.
        """
        return self.size == 0

    @property
    def is_full(self) -> bool:
        """
        Defines is stack full.

        :returns: True - if the size of the stack is equal to its capacity. False - otherwise.
        """
        return self.size == self.capacity

    @property
    def size(self) -> int:
        """
        Gets used size of the stack capacity.

        :returns: Amount of the used space of the stack (between 0 and CAPACITY_MAXIMUM).
        """
        return self.__space_used

    @property
    def capacity(self) -> int:
        """
        Gets maximum size of the stack's storage.

        :returns: Total amount that can be used for the stack instance.
        """
        return self.__capacity

    @capacity.setter
    def capacity(self, value: int):
        """
        Sets maximum size of the stack's storage.

        :param value: size of the storage.
        :raises TypeError: Capacity of the stack must be integer value.
        :raises ValueError: Capacity of the stack can not be less than zero and grater than CAPACITY_MAXIMUM.
        """
        if not isinstance(value, int):
            raise TypeError("Capacity of the stack must be integer value.")
        if value <= 0:
            raise ValueError('Capacity of the stack can not be less than zero.')
        if value >= Stack.CAPACITY_MAXIMUM:
            raise ValueError(f'Capacity of the stack can not be grater than {Stack.CAPACITY_MAXIMUM}.')

        self.__capacity = value

    def push(self, value):
        """
        Adds value to the top of the stack.

        :raises StackOverflowException: the size of the stack is equal or grater than stack's capacity.
        :returns: same stack with added value to the top.
        """
        if self.is_full:
            raise StackOverflowException()
        self.__storage.append(value)
        self.__space_used += 1
        return self

    def pop(self):
        """
        Gets value form the top of the stack and removes it from the storage.

        :raises StackIsEmptyException: cannot get value from the empty stack.
        :returns: value at the top of the stack.
        """
        if self.is_empty:
            raise StackIsEmptyException()
        self.__space_used -= 1
        return self.__storage.pop()

    def peek(self):
        """
        Gets value form the top of the stack.

        :raises StackIsEmptyException: cannot get value from the empty stack.
        :returns: value at the top of the stack.
        """
        if self.is_empty:
            raise StackIsEmptyException()
        return self.__storage[self.__space_used-1]


class Case:
    """
    Represents expected and input data for specified target.

    CHARS_TO_REMOVE - value to filter an input string.
    TARGET_LABEL - value to remove from the beginning of the target (test-method name) line.
    DATA_LABEL - value to remove from the beginning of the data line.
    EXPECTED_LABEL - value to remove form the beginning of the expected line.
    """
    CHARS_TO_REMOVE = "\n\t\r "
    TARGET_LABEL = "target:"
    DATA_LABEL = "data:"
    EXPECTED_LABEL = 'expected:'

    def __init__(self, lines):
        self.target = lines
        self.data = lines
        self.expected = lines

    def __str__(self):
        """
        Represents case in default method representation format.
        """
        return f'{self.target}({self.data}) -> {self.expected}'

    @property
    def data(self):
        """
        Gets input data parameter.
        """
        return self.__data

    @property
    def expected(self):
        """
        Gets expected data.
        """
        return self.__expected

    @property
    def target(self):
        """
        Gets target parameter - test method name.
        """
        return self.__target

    @target.setter
    def target(self, value: list[str]):
        """
        Sets target (test method name) value from the list and removes that line.

        :param value: lines to parse target value from.
        """
        self.__target = value.pop(0).removeprefix(self.TARGET_LABEL).strip(self.CHARS_TO_REMOVE)

    @data.setter
    def data(self, value: list[str]):
        """
        Sets data value from the list and removes that line.

        :param value: lines to parse target value from.
        """
        self.__data = eval(value.pop(0).removeprefix(self.DATA_LABEL).strip(self.CHARS_TO_REMOVE))

    @expected.setter
    def expected(self, value: list[str]):
        """
        Sets expected value from the lis and removes that line.

        :param value: lines to parse target value from.
        """
        self.__expected = eval(value.pop(0).removeprefix(self.EXPECTED_LABEL).strip(self.CHARS_TO_REMOVE))


class TestCases:
    """
    Loads and creates list of the Cases.
    """
    def __init__(self, ):
        self.__cases: list[Case] = []

    def __getitem__(self, target: str) -> Case | None:
        """
        Get needed test case based on target (test-method name) value.

        :param target: name of the test-method.
        :returns: Case that has method name as target.
        """
        return next(filter(lambda transport: transport.target == target, self.__cases), None)

    def load(self, lines: list[str]):
        """
        Creates cases based on lines

        :param lines: list of the lines to create cases with.
        """
        while lines:
            self.__cases.append(Case(lines))


class Test(TestCase):
    """
    Test class to run test cases.

    CASES - TestCases manager.
    STACK_DEEP - stack call deep to get name of the function that is test method.
    STACK_FUNC_NAME_INFO - index of the
    """
    CASES = TestCases()
    STACK_DEEP = 1
    STACK_FUNC_NAME_INFO = 3
    TEST_FILE_SOURCE = 'testInput.txt'

    @classmethod
    def setUpClass(cls) -> None:
        with open(cls.TEST_FILE_SOURCE, encoding='utf-8') as tests:
            cls.CASES.load([line for line in tests.readlines() if line.strip(Case.CHARS_TO_REMOVE) != ''])

    @property
    def current(self) -> Case:
        return self.CASES[stack()[self.STACK_DEEP][self.STACK_FUNC_NAME_INFO]]

    def test_stackCreation_CapacityNotInt_TypeError(self):
        for capacity in self.current.data:
            with self.subTest(f"Capacity = {capacity}"):
                self.assertRaises(self.current.expected, lambda: Stack(capacity))

    def test_stackCreation_CapacityLessOrEqualZero_ValueError(self):
        for capacity in self.current.data:
            with self.subTest(f'Capacity = {capacity}'):
                self.assertRaises(self.current.expected, lambda: Stack(capacity))

    def test_stackCreation_CapacityGraterThanMaximum_ValueError(self):
        for capacity in self.current.data:
            with self.subTest(f'Capacity = {capacity}'):
                self.assertRaises(self.current.expected, lambda: Stack(capacity))

    def test_stackPush_CapacityLessThanSize_StackOverflowException(self):
        self.assertRaises(self.current.expected, self.current.data)

    def test_stackPop_CapacityLessThanSize_StackOverflowException(self):
        self.assertRaises(self.current.expected, self.current.data)

    def test_stackPeek_CapacityLessThanSize_StackOverflowException(self):
        self.assertRaises(self.current.expected, self.current.data)

    def test_get_parenthesis_DefaultOutput(self):
        expected = get_parenthesis(self.current.data)
        self.assertEqual(expected, self.current.expected)

    def test_get_parenthesis_SortByOpening(self):
        expected = get_parenthesis(self.current.data, 0)
        self.assertEqual(expected, self.current.expected)

    def test_get_parenthesis_SortByClosing(self):
        expected = get_parenthesis(self.current.data, 1)
        self.assertEqual(expected, self.current.expected)

    def test_is_valid_formula(self):
        expected = is_valid_formula(self.current.data)
        self.assertEqual(expected, self.current.expected)


def get_parenthesis(line: str, sort_by: int = -1) -> list[tuple]:
    open_parenthesis_amount = line.count(OPENING_PARENTHESIS)
    close_parenthesis_amount = line.count(CLOSING_PARENTHESIS)
    if open_parenthesis_amount != close_parenthesis_amount:
        raise ParenthesisMissmatchException(open_parenthesis_amount, close_parenthesis_amount)

    result = Stack(open_parenthesis_amount + close_parenthesis_amount)
    container = Stack(open_parenthesis_amount + close_parenthesis_amount)

    for index, item in enumerate(line):
        if item == OPENING_PARENTHESIS:
            container.push(index)
        if item == CLOSING_PARENTHESIS:
            result.push((container.pop(), index))

    return sorted([result.pop() for _ in range(result.size)], key=lambda t: t[sort_by]) if 0 <= sort_by < 2 \
        else list(reversed([result.pop() for _ in range(result.size)]))


def get_closing_bracket(opening: str) -> str:
    """
    Finds proper closing bracket for opening one.

    :param opening: bracket to find closing pair.
    :returns: proper closing pair or "}" by default.
    """
    return ')' if opening == '(' else ']' if opening == '[' else '}'


def is_valid_formula(line: str) -> bool:
    """
    Defines is line is valid formula rule.

    :param line: line to validate as formula
    :returns: True - if line is satisfying formula requirements. False - otherwise.
    """
    s1 = Stack(len(line))
    s2 = Stack(len(line))
    is_letter_can_be_next = True

    for letter in line.replace(' ', ''):
        if letter in OPERANDS:
            s1.push(letter)
            if is_letter_can_be_next:
                is_letter_can_be_next = False
            else:
                return False

        if letter in OPERATORS:
            is_letter_can_be_next = True
            s2.push(letter)

        if letter in OPENING_BRACKETS:
            s2.push(letter)

        if letter in CLOSING_BRACKETS:
            while not s2.is_empty:
                if letter == get_closing_bracket(s2.pop()):
                    break
                if s1.size < 2:
                    return False
                s1.pop()
            else:
                return False

    while not s2.is_empty:
        if s2.pop() not in OPERATORS or s1.size < 2:
            return False
        s1.pop()

    return s1.size <= 1 and s2.is_empty


def evaluate_formula(line: str) -> float:
    pass


def run():
    line = "x - (y - z - (x + x))"
    print(is_valid_formula(line))


if __name__ == '__main__':
    main()
