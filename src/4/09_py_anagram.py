"""
py_anagram.py

Check if two strings are anagrams of each other: same letters with the
same multiplicities, ignoring case and spaces.
"""

from collections import Counter


def _normalize(s: str) -> Counter:
    return Counter(char.lower() for char in s if char != " ")


def anagram(s1: str, s2: str) -> bool:
    return _normalize(s1) == _normalize(s2)


if __name__ == "__main__":
    tests = [
        (("listen", "silent"), True),
        (("Triangle", "Integral"), True),
        (("Dormitory", "Dirty Room"), True),
        (("hello", "world"), False),
        (("", ""), True),
        (("abc", "abcc"), False),
    ]

    for (s1, s2), expected in tests:
        result = anagram(s1, s2)
        status = "OK" if result == expected else "FAIL"
        print(f"[{status}] anagram({s1!r}, {s2!r}) -> {result}")
