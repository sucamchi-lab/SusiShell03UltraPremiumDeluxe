"""
py_twist_sequence.py

Rotate an array to the right by k positions: the last k elements move
to the front. k can be larger than the array length (wraps around) and
the array can be empty.
"""


def twist_sequence(arr: list[int], k: int) -> list[int]:
    if not arr:
        return []

    k %= len(arr)
    if k == 0:
        return list(arr)

    return arr[-k:] + arr[:-k]


if __name__ == "__main__":
    tests = [
        (([1, 2, 3, 4, 5], 2), [4, 5, 1, 2, 3]),
        (([1, 2, 3], 1), [3, 1, 2]),
        (([1, 2, 3, 4], 0), [1, 2, 3, 4]),
        (([1, 2, 3], 5), [2, 3, 1]),
        (([], 3), []),
    ]

    for (arr, k), expected in tests:
        result = twist_sequence(arr, k)
        status = "OK" if result == expected else "FAIL"
        print(f"[{status}] twist_sequence({arr!r}, {k}) -> {result}")
