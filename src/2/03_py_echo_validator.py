"""
py_echo_validator.py

Check if a string is a palindrome, considering only alphabetic characters
and ignoring case. A string with no alphabetic characters at all (including
an empty string) is not considered a palindrome.
"""


def echo_validator(text: str) -> bool:
    letters = [char.lower() for char in text if char.isalpha()]

    if not letters:
        return False

    return letters == letters[::-1]


if __name__ == "__main__":
    tests = [
        ("racecar", True),
        ("A man a plan a canal Panama", True),
        ("race a car", False),
        ("Was it a car or a cat I saw", True),
        ("hello", False),
        ("Madam Im Adam", True),
        ("", False),
    ]

    for value, expected in tests:
        result = echo_validator(value)
        status = "OK" if result == expected else "FAIL"
        print(f"[{status}] echo_validator({value!r}) -> {result}")
