"""
py_string_permutation_checker.py

Check if two strings are permutations of each other: same characters
with the same multiplicities. Case-sensitive; whitespace and
punctuation count as regular characters. Two empty strings count as
permutations of each other.
"""

from collections import Counter


def string_permutation_checker(s1: str, s2: str) -> bool:
    if len(s1) != len(s2):
        return False

    return Counter(s1) == Counter(s2)


if __name__ == "__main__":
    tests = [
        (("abc", "bca"), True),
        (("abc", "def"), False),
        (("listen", "silent"), True),
        (("hello", "bello"), False),
        (("", ""), True),
        (("a", ""), False),
        (("Abc", "abc"), False),
        (("a gentleman", "elegant man"), True),
    ]

    for (s1, s2), expected in tests:
        result = string_permutation_checker(s1, s2)
        status = "OK" if result == expected else "FAIL"
        print(f"[{status}] string_permutation_checker({s1!r}, {s2!r}) -> {result}")
