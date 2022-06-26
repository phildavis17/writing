import fizzbuzzes

from typing import Callable


def driver_function(fb_function: Callable, limit: int) -> list:
    return [fb_function(n) for n in range(1, limit + 1)]


FIRST_15 = [
    "1",
    "2",
    "Fizz",
    "4",
    "Buzz",
    "Fizz",
    "7",
    "8",
    "Fizz",
    "Buzz",
    "11",
    "Fizz",
    "13",
    "14",
    "FizzBuzz",
]

FIRST_100 = list(map(fizzbuzzes.fb_if, range(1, 101)))


def get_first_fifteen(func: Callable):
    return driver_function(func, 15)


def test_if():
    assert get_first_fifteen(fizzbuzzes.fb_if) == FIRST_15


def test_if_flags():
    assert get_first_fifteen(fizzbuzzes.fb_if_flags) == FIRST_15


def test_if_flag_functions():
    assert get_first_fifteen(fizzbuzzes.fb_if_flag_functions) == FIRST_15


def test_constructed_long():
    assert get_first_fifteen(fizzbuzzes.fb_factor_dict_longhand) == FIRST_15


def test_constructed_short():
    assert get_first_fifteen(fizzbuzzes.fb_factor_dict_shorthand) == FIRST_15


def test_cycle_big():
    assert fizzbuzzes.fb_cycle(15) == FIRST_15


def test_sub_cycles():
    assert fizzbuzzes.fb_sub_cycles(15) == FIRST_15


def test_constructed_cycles():
    assert fizzbuzzes.fb_constructed_cycles(100) == FIRST_100


def test_generator():
    assert fizzbuzzes.fb_generator(100) == FIRST_100
