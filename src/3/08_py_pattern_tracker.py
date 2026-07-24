"""
py_pattern_tracker.py

Count adjacent character pairs in a string where both characters are
digits and the second digit is exactly one greater than the first.
(9 -> 0 does not count, since 0 is not "one greater" than 9.)
"""


def pattern_tracker(text: str) -> int:
    count = 0

    for first, second in zip(text, text[1:]):
        if first.isdigit() and second.isdigit() and int(second) - int(first) == 1:
            count += 1

    return count


if __name__ == "__main__":
    tests = [
        ("123", 2),
        ("12a34", 2),
        ("987654321", 0),
        ("01234567", 7),
        ("abc", 0),
        ("1a2b3c4", 0),
        ("112233", 2),
    ]

    for value, expected in tests:
        result = pattern_tracker(value)
        status = "OK" if result == expected else "FAIL"
        print(f"[{status}] pattern_tracker({value!r}) -> {result}")
