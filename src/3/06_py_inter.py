"""
py_inter.py

Return a string with the characters that appear in both s1 and s2,
without repetitions, in the order they first appear in s1.
"""


def inter(s1: str, s2: str) -> str:
    seen = set()
    common = set(s1) & set(s2)
    result = []

    for char in s1:
        if char in common and char not in seen:
            result.append(char)
            seen.add(char)

    return "".join(result)


if __name__ == "__main__":
    tests = [
        (("hello", "world"), "lo"),
        (("banana", "band"), "ban"),
        (("abcabc", "bc"), "bc"),
        (("abc", "xyz"), ""),
        (("", "abc"), ""),
    ]

    for (s1, s2), expected in tests:
        result = inter(s1, s2)
        status = "OK" if result == expected else "FAIL"
        print(f"[{status}] inter({s1!r}, {s2!r}) -> {result!r}")
