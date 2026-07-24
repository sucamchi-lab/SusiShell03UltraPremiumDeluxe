"""
py_string_sculptor.py

Alternate the case of alphabetic characters: the 1st alpha char (index 0)
becomes lowercase, the 2nd (index 1) becomes uppercase, and so on.
Non-alphabetic characters pass through unchanged and don't consume an
index -- except spaces, which additionally reset the alternation counter
back to 0 for the next alphabetic character.
"""


def string_sculptor(text: str) -> str:
    result = []
    index = 0

    for char in text:
        if char.isalpha():
            result.append(char.lower() if index % 2 == 0 else char.upper())
            index += 1
        else:
            result.append(char)
            if char == " ":
                index = 0

    return "".join(result)


if __name__ == "__main__":
    tests = [
        ("hello", "hElLo"),
        ("Hello World", "hElLo wOrLd"),
        ("abc123def", "aBc123DeF"),
        ("Python3.9!", "pYtHoN3.9!"),
        ("", ""),
    ]

    for value, expected in tests:
        result = string_sculptor(value)
        status = "OK" if result == expected else "FAIL"
        print(f"[{status}] string_sculptor({value!r}) -> {result!r}")
