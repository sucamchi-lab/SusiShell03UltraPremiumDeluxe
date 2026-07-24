"""
py_hidenp.py

Check whether `small` is a subsequence of `big`: every character of
`small` must appear in `big`, in the same order, though not necessarily
consecutively. Case-sensitive.
"""


def hidenp(small: str, big: str) -> bool:
    it = iter(big)
    return all(char in it for char in small)


if __name__ == "__main__":
    tests = [
        (("abc", "a1b2c3"), True),
        (("ace", "abcde"), True),
        (("aec", "abcde"), False),
        (("", "abc"), True),
        (("abc", "ab"), False),
        (("aaaa", "aaa"), False),
        (("sing", "subsequence testing"), True),
    ]

    for (small, big), expected in tests:
        result = hidenp(small, big)
        status = "OK" if result == expected else "FAIL"
        print(f"[{status}] hidenp({small!r}, {big!r}) -> {result}")
