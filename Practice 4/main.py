from abc import ABC, abstractmethod
from inspect import stack
from unittest import TestCase, main

OPENING_PARENTHESIS = '('
CLOSING_PARENTHESIS = ')'
OPERANDS = ['x', 'y', 'z']
OPERATORS = ['+', '-']
OPENING_BRACKETS = ['(', '[', '{']
CLOSING_BRACKETS = [')', ']', '}']
NUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
SEMICOLON = ','


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


class NotationException(BaseException):
    EXCEPTION_MESSAGE = "Expected {0} but was {1} at {2}\n{3}\n{4}^"

    def __init__(self, expected, present, index, line):
        self.expected = expected
        self.present = present
        self.index = index
        self.line = line
        super().__init__(self.EXCEPTION_MESSAGE.format(expected, present, index, line, '-' * index))


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
        return f'Stack: ({self.size}/{self.capacity}) [{", ".join(map(str, self.__storage))}]'

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
        return self.__storage[self.__space_used - 1]

    def try_pop(self, default):
        return default if self.is_empty else self.pop()


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

    def test_compilation(self):
        expected = Compiler().compile(self.current.data)
        self.assertEqual(expected, self.current.expected)


class Compiler:
    """
    Compiles expression in format:
    expression := number | S(expression, expression) | D(expression, expression)
    number := 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0
    """
    def __init__(self):
        self.state = InitialState(self)
        self.previous_state = Stack(100)
        self.stack = Stack(100)
        self.expression = ""
        self.current_index = 0

    def compile(self, expression: str) -> int:
        """
        Evaluates expression with predefined format.

        :param expression: expression to compile and evaluate
        """
        self.expression = expression
        while not isinstance(self.state, FinalState):
            self.state.accept_letter()
        return int(sum([self.stack.try_pop(0) for _ in range(self.stack.size)]))


class State(ABC):
    """
    Base of the state machine to compile the expression.
    Provides access to the compiler data and simplifies its management.

    InitialState    -> (expression was empty) FinalState
                    -> (expression starts with the number) OneNumberState
                    -> (expression starts with letter 'S') SumState
                    -> (expression starts with letter 'D') DivideState

    OneNumberState  -> Final state

    SumState        -> (if '(' provided) FirstSumArgumentState

    FirstArgument   -> (expression starts with letter 'S') SumState
                    -> (expression starts with letter 'D') DivideState
                    -> (',' provided) SecondArgument

    SecondArgument  -> (expression starts with letter 'S') SumState
                    -> (expression starts with letter 'D') DivideState
                    -> (')' provided) Previous state

    FinalState      -> Ends execution

    """
    EXPRESSION_END = 'end of the expression'
    NUMBER = 'number'

    def __init__(self, context: Compiler):
        self.context = context

    @property
    def letter(self):
        return self.context.expression[self.context.current_index] if self.context.current_index < \
                                                                      len(self.context.expression) else ''

    @property
    def index(self):
        return self.context.current_index

    @property
    def is_end_of_expression(self):
        return self.index >= len(self.context.expression)

    def next(self):
        self.context.current_index += 1

    def push(self, value):
        self.context.stack.push(value)

    def pop(self):
        return self.context.stack.try_pop('0')

    def change_state(self, new_state):
        self.context.state = new_state(self.context)
        self.next()

    def change_and_save_state(self, new_state):
        self.context.previous_state.push(self.context.state)
        self.change_state(new_state)

    def rollback_state(self):
        if not self.context.previous_state.is_empty:
            self.context.state = self.context.previous_state.pop()
        self.next()

    def raise_exception(self, expected: str, index=None):
        raise NotationException(expected, self.letter,
                                self.index if index is None else index,
                                self.context.expression)

    @abstractmethod
    def accept_letter(self):
        pass


class InitialState(State):

    def accept_letter(self):
        if self.is_end_of_expression:
            self.change_state(FinalState)
            return

        if self.letter == ' ':
            self.next()
            return

        if self.letter in NUMBERS:
            self.push(int(self.letter))
            self.change_state(OneNumberState)
            return

        if self.letter == 'S':
            self.change_state(SumState)
            return

        if self.letter == 'D':
            self.change_state(DivideState)


class OneNumberState(State):

    def accept_letter(self):
        if self.is_end_of_expression:
            self.change_state(FinalState)
            return

        if self.letter == ' ':
            self.next()
            return

        if self.letter in NUMBERS:
            self.push(self.pop() + self.letter)
            self.next()
            return

        self.raise_exception(self.EXPRESSION_END)


class OperatorState(State):

    def accept_letter(self):
        if self.letter == ' ':
            self.next()
            return

        if self.letter != '(':
            self.raise_exception('(')


class SumState(OperatorState):

    def accept_letter(self):
        super(SumState, self).accept_letter()
        self.change_state(FirstSumArgumentState)


class DivideState(OperatorState):
    def accept_letter(self):
        super(DivideState, self).accept_letter()
        self.change_state(FirstDivideArgumentState)


class ArgumentInputState(State, ABC):

    def handle_argument_input(self):
        if self.letter == ' ':
            self.next()
            return True

        if self.letter == 'S':
            self.change_and_save_state(SumState)
            return True

        if self.letter == 'D':
            self.change_and_save_state(DivideState)
            return True

        return False


class FirstSumArgumentState(ArgumentInputState):
    def accept_letter(self):
        if super(FirstSumArgumentState, self).handle_argument_input():
            return

        if self.letter == ',':
            self.change_state(SecondSumArgumentInputState)
            return

        if self.is_end_of_expression or self.letter == ')':
            self.raise_exception(',')

        if self.letter not in NUMBERS:
            self.raise_exception(self.NUMBER)

        self.push(int(self.letter))
        self.next()


class SecondSumArgumentInputState(ArgumentInputState):

    def accept_letter(self):
        if super(SecondSumArgumentInputState, self).handle_argument_input():
            return

        if self.is_end_of_expression:
            self.change_state(FinalState)
            return

        if self.letter == ')':
            second, first = self.pop(), self.pop()
            self.push(first+second)
            self.rollback_state()
            return

        if self.letter not in NUMBERS:
            self.raise_exception(self.NUMBER)

        self.push(int(self.letter))
        self.next()


class FirstDivideArgumentState(ArgumentInputState):

    def accept_letter(self):
        if super(FirstDivideArgumentState, self).handle_argument_input():
            return

        if self.is_end_of_expression or self.letter == ')':
            self.raise_exception(',')
            
        if self.letter == ',':
            self.change_state(SecondDivideArgumentInputState)
            return

        if self.letter not in NUMBERS:
            self.raise_exception(self.NUMBER)

        self.push(int(self.letter))
        self.next()


class SecondDivideArgumentInputState(ArgumentInputState):

    def accept_letter(self):
        if super(SecondDivideArgumentInputState, self).handle_argument_input():
            return

        if self.is_end_of_expression:
            self.change_state(FinalState)
            return

        if self.letter == ')':
            second, first = self.pop(), self.pop()
            if second == 0:
                self.raise_exception('number from 1 to 9', self.index - self.context.previous_state.size * 2)
            self.push(first / second)
            self.rollback_state()
            return

        if self.letter not in NUMBERS:
            self.raise_exception(self.NUMBER)

        if self.letter == '0':
            self.raise_exception('number from 1 to 9')

        self.push(int(self.letter))
        self.next()


class FinalState(State):
    def accept_letter(self):
        return


def get_parenthesis(line: str, sort_by: int = -1) -> list[tuple]:
    """
    Gather information about indexes of the parenthesis.

    :param line: line to parse indexes of the parenthesis from.
    :param sort_by: sorting order of the indexes:   -1 -not sorted,
                                                    0 sorted by opening parenthesis,
                                                    1 or grater sorted by closing parenthesis.
    :raise ParenthesisMissmatchException: amount of the closing parenthesis is not equal to opening ones.
    :returns: list of the tuples of the parenthesis.
    """
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
    operands_stack = Stack(len(line))
    operators_stack = Stack(len(line))
    is_letter_can_be_next = True

    for letter in line.replace(' ', ''):
        if letter in OPERANDS:
            operands_stack.push(letter)
            if is_letter_can_be_next:
                is_letter_can_be_next = False
            else:
                return False

        if letter in OPERATORS:
            is_letter_can_be_next = True
            operators_stack.push(letter)

        if letter in OPENING_BRACKETS:
            operators_stack.push(letter)

        if letter in CLOSING_BRACKETS:
            while not operators_stack.is_empty:
                if letter == get_closing_bracket(operators_stack.pop()):
                    break
                if operands_stack.size < 2:
                    return False
                operands_stack.pop()
            else:
                return False

    while not operators_stack.is_empty:
        if operators_stack.pop() not in OPERATORS or operands_stack.size < 2:
            return False
        operands_stack.pop()

    return operands_stack.size <= 1 and operators_stack.is_empty


def run():
    c = Compiler()
    print(c.compile("D(S(9, S(2, 9)), D(4, 2))"))


if __name__ == '__main__':
    main()
