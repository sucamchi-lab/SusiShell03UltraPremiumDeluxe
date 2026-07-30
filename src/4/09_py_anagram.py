"""
py_anagram.py

Check if two strings are anagrams of each other: same letters with the
same multiplicities, ignoring case and spaces.
"""


def anagram(s1: str, s2: str) -> bool:
    def norm(s: str) -> str:
        return "".join(ch.lower() for ch in s if ch != " ")
    return sorted(norm(s1)) == sorted(norm(s2))


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
