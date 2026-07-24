"""
py_shadow_merge.py

Merge two already-sorted lists of ints into a single sorted list,
using the classic two-pointer merge (as in merge sort) rather than
concatenating and re-sorting.
"""


def shadow_merge(list1: list[int], list2: list[int]) -> list[int]:
    merged = []
    i, j = 0, 0

    while i < len(list1) and j < len(list2):
        if list1[i] <= list2[j]:
            merged.append(list1[i])
            i += 1
        else:
            merged.append(list2[j])
            j += 1

    merged.extend(list1[i:])
    merged.extend(list2[j:])

    return merged


if __name__ == "__main__":
    tests = [
        (([1, 3, 5], [2, 4, 6]), [1, 2, 3, 4, 5, 6]),
        (([1, 2, 3], [4, 5, 6]), [1, 2, 3, 4, 5, 6]),
        (([1], [2, 3, 4]), [1, 2, 3, 4]),
        (([], [1, 2, 3]), [1, 2, 3]),
        (([1, 1, 2], [1, 3, 3]), [1, 1, 1, 2, 3, 3]),
    ]

    for (list1, list2), expected in tests:
        result = shadow_merge(list1, list2)
        status = "OK" if result == expected else "FAIL"
        print(f"[{status}] shadow_merge({list1!r}, {list2!r}) -> {result}")
