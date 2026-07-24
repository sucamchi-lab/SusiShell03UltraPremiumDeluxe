"""
py_cryptic_sorter.py

Sort a list of strings by:
  1. Length (shortest first)
  2. Case-insensitive ASCII order (for equal length)
  3. Number of vowels, ascending
Ties keep their original relative order (stable).

sorted() and list.sort() are forbidden,
so a stable insertion sort is implemented.
"""


def vowel_count(s: str) -> int:
    return sum(1 for c in s.lower() if c in "aeiou")


def cryptic_sorter(strings: list[str]) -> list[str]:
    # Precompute keys: each key computed exactly once
    keys = [(len(s), s.lower(), vowel_count(s)) for s in strings]

    result = list(strings)
    for i in range(1, len(result)):
        current_val = result[i]
        current_key = keys[i]
        j = i - 1
        while j >= 0 and keys[j] > current_key:
            result[j + 1] = result[j]
            keys[j + 1] = keys[j]
            j -= 1
        result[j + 1] = current_val
        keys[j + 1] = current_key

    return result


if __name__ == "__main__":
    tests = [
        (["apple", "cat", "banana", "dog", "elephant"],
         ["cat", "dog", "apple", "banana", "elephant"]),
        (["aaa", "bbb", "AAA", "BBB"],
         ["aaa", "AAA", "bbb", "BBB"]),
        (["hello", "world", "hi", "test"],
         ["hi", "test", "hello", "world"]),
        ([], []),
        ([""], [""]),
    ]

    for value, expected in tests:
        result = cryptic_sorter(value)
        status = "OK" if result == expected else "FAIL"
        print(f"[{status}] cryptic_sorter({value!r}) -> {result}")
