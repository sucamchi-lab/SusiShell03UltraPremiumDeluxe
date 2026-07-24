"""
py_whisper_cipher.py

Caesar cipher: shift alphabetic characters by `shift` positions,
wrapping around within their own case (a-z / A-Z), and leaving any
non-alphabetic character unchanged. The shift may be negative.
"""


def _shift_char(char: str, shift: int) -> str:
    base = ord('a') if char.islower() else ord('A')
    return chr((ord(char) - base + shift) % 26 + base)


def whisper_cipher(text: str, shift: int) -> str:
    return "".join(
        _shift_char(char, shift) if char.isalpha() else char
        for char in text
    )


if __name__ == "__main__":
    tests = [
        (("hello", 3), "khoor"),
        (("Hello World!", 1), "Ifmmp Xpsme!"),
        (("xyz", 3), "abc"),
        (("ABC123def", 5), "FGH123ijk"),
        (("", 10), ""),
        (("abc", -3), "xyz"),
    ]

    for (text, shift), expected in tests:
        result = whisper_cipher(text, shift)
        status = "OK" if result == expected else "FAIL"
        print(f"[{status}] whisper_cipher({text!r}, {shift}) -> {result!r}")
