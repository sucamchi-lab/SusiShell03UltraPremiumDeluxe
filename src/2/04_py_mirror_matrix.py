"""
py_mirror_matrix.py

Given a 2D matrix (list of lists), return a new matrix where each row
is reversed. The original matrix is left untouched.
"""


def mirror_matrix(matrix: list[list[int]]) -> list[list[int]]:
    return [row[::-1] for row in matrix]


if __name__ == "__main__":
    tests = [
        ([[1, 2, 3], [4, 5, 6]], [[3, 2, 1], [6, 5, 4]]),
        ([[1, 2], [3, 4], [5, 6]], [[2, 1], [4, 3], [6, 5]]),
        ([[7]], [[7]]),
        ([[1, 2, 3, 4]], [[4, 3, 2, 1]]),
        ([[-1, -2], [-3, -4]], [[-2, -1], [-4, -3]]),
    ]

    for value, expected in tests:
        result = mirror_matrix(value)
        status = "OK" if result == expected else "FAIL"
        print(f"[{status}] mirror_matrix({value!r}) -> {result}")
