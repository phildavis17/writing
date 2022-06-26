from collections import defaultdict
from itertools import count, cycle, islice
from typing import Generator, Tuple


##### ---=== SINGLE NUMBER RETURNS ===--- #####


def fb_if(n: int) -> str:
    if n % 15 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    else:
        return str(n)


def fb_if_flags(n: int) -> str:
    should_fizz = n % 3 == 0
    should_buzz = n % 5 == 0
    if should_fizz and should_buzz:
        return "FizzBuzz"
    elif should_fizz:
        return "Fizz"
    elif should_buzz:
        return "Buzz"
    else:
        return str(n)


def fb_if_flag_functions(n: int) -> str:
    should_fizz = _is_fizzable(n)
    should_buzz = _is_buzzable(n)
    if should_fizz and should_buzz:
        return "FizzBuzz"
    elif should_fizz:
        return "Fizz"
    elif should_buzz:
        return "Buzz"
    else:
        return str(n)


def fb_f_strings(n: int) -> str:
    fizz = "Fizz" if _is_fizzable(n) else ""
    buzz = "Buzz" if _is_buzzable(n) else ""
    return f"{fizz}{buzz}" or str(n)


def _is_fizzable(n: int) -> bool:
    while len(str(n)) > 1:
        n = sum(int(c) for c in str(n))
    return n in {3, 6, 9}


def _is_buzzable(n: int) -> bool:
    return str(n)[-1] in {"0", "5"}


"""
def fb_SPM_brute_force(n: int) -> str:
    match n:
        case _ if n % 15 == 0:
            return "FizzBuzz"
        case _ if n % 3 == 0:
            return "Fizz"
        case _ if n % 5 == 0:
            return "Buzz"
        case _:
            return str(n)


def fb_SPM_mod(n: int) -> str:
    match n % 15:
        case 0:
            return "FizzBuzz"
        case 3 | 6 | 9 | 12:
            return "Fizz"
        case 5 | 10:
            return "Buzz"
        case _:
            return str(n)


def fb_SPM_tuple(n: int) -> str:
    match (n % 3, n % 5):
        case (0, 0):
            return "FizzBuzz"
        case (0, _):
            return "Fizz"
        case (_, 0):
            return "Buzz"
        case _:
            return str(n)
"""


def fb_factor_dict_longhand(n: int) -> str:
    factor_dict = {
        3: "Fizz",
        5: "Buzz",
    }
    output = ""
    for factor, text in factor_dict.items():
        if n % factor == 0:
            output += text
    if not output:
        output = str(n)
    return output


def fb_factor_dict_shorthand(n: int) -> str:
    factor_dict = {
        3: "Fizz",
        5: "Buzz",
    }
    return "".join(
        text for factor, text in factor_dict.items() if n % factor == 0
    ) or str(n)


def fb_cycle(limit: int) -> list:
    fb_pattern = (
        "",
        "",
        "Fizz",
        "",
        "Buzz",
        "Fizz",
        "",
        "",
        "Fizz",
        "Buzz",
        "",
        "Fizz",
        "",
        "",
        "FizzBuzz",
    )
    fb_cycle = cycle(fb_pattern)
    output = []
    for i, fb in enumerate(fb_cycle, 1):
        if i > limit:
            break
        output.append(fb or str(i))
    return output
    nums = range(1, limit + 1)
    output = [fb or str(num) for fb, num in zip(fb_cycle, nums)]
    return output


def fb_sub_cycles(limit: int) -> list:
    pattern_3 = cycle(("", "", "Fizz"))
    pattern_5 = cycle(("", "", "", "", "Buzz"))
    combined_pattern = (fizz + buzz for fizz, buzz in zip(pattern_3, pattern_5))
    nums = range(1, limit + 1)
    return [fb or str(n) for fb, n in zip(combined_pattern, nums)]


def fb_constructed_cycles(limit: int) -> list:
    factor_dict = {
        3: "Fizz",
        5: "Buzz",
    }
    cycles = (
        cycle(_construct_pattern(factor, text)) for factor, text in factor_dict.items()
    )
    combined_pattern = ("".join(text) for text in zip(*cycles))
    nums = range(1, limit + 1)
    return [fb or str(n) for fb, n in zip(combined_pattern, nums)]


def _construct_pattern(factor: int, text: str) -> tuple:
    pattern = [""] * factor
    pattern[-1] = text
    return tuple(pattern)


def fb_generator(limit: int) -> list:
    factor_dict = {
        3: "Fizz",
        5: "Buzz",
    }
    return list(islice(_fb_generator(factor_dict), limit))


def _fb_generator(factor_dict: dict) -> Generator:
    cycles = (
        cycle(_construct_pattern(factor, text)) for factor, text in factor_dict.items()
    )
    combined_pattern = ("".join(text) for text in zip(*cycles))
    nums = count(1)
    for fb, n in zip(combined_pattern, nums):
        yield fb or str(n)


# Let's do a goofy one


def _factor_signature(n: int, factors: Tuple[int, ...]) -> int:
    signature = [str(int(n % factor == 0)) for factor in factors]
    signature.reverse()
    return int("".join(signature), 2)


signature_dict = {
    0: "",
    1: "Buzz",
    2: "Fizz",
    3: "FizzBuzz",
}


def _decode_factor_signature(signature: int, signature_dict: dict) -> str:
    pass


print(_factor_signature(15, (3, 5)))
print(_factor_signature(10, (3, 5)))
print(_factor_signature(9, (3, 5)))
print(_factor_signature(8, (3, 5)))
