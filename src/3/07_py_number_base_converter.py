"""
py_number_base_converter.py

Convert a number (given as a string) from one base to another.
Supported bases: 2 to 36 inclusive, using 0-9 then A-Z for digit
values 10-35. Returns "ERROR" for any invalid input: out-of-range
bases, an empty number, or digits that aren't valid in from_base.
"""

DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def number_base_converter(number: str, from_base: int, to_base: int) -> str:
    if not (2 <= from_base <= 36) or not (2 <= to_base <= 36):
        return "ERROR"
    if not number:
        return "ERROR"

    valid_digits = DIGITS[:from_base]
    value = 0
    for char in number.upper():
        if char not in valid_digits:
            return "ERROR"
        value = value * from_base + valid_digits.index(char)

    if value == 0:
        return "0"

    digits = []
    while value:
        value, remainder = divmod(value, to_base)
        digits.append(DIGITS[remainder])

    return "".join(reversed(digits))


if __name__ == "__main__":
    tests = [
        (("1010", 2, 10), "10"),
        (("FF", 16, 10), "255"),
        (("255", 10, 16), "FF"),
        (("123", 10, 2), "1111011"),
        (("Z", 36, 10), "35"),
        (("35", 10, 36), "Z"),
        (("123", 1, 10), "ERROR"),
        (("G", 16, 10), "ERROR"),
    ]

    for (number, from_base, to_base), expected in tests:
        result = number_base_converter(number, from_base, to_base)
        status = "OK" if result == expected else "FAIL"
        print(f"[{status}] number_base_converter({number!r}, {from_base}, "
              f"{to_base}) -> {result!r}")
