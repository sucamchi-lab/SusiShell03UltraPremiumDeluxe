"""
py_whisper_cipher.py

Caesar cipher: shift alphabetic characters by `shift` positions,
wrapping around within their own case (a-z / A-Z), and leaving any
non-alphabetic character unchanged. The shift may be negative.
"""


def shift_char(c: str, shift: int) -> str:
    o = ord(c)
    if 'a' <= c <= 'z':
        return chr((o - 97 + shift) % 26 + 97)
    if 'A' <= c <= 'Z':
        return chr((o - 65 + shift) % 26 + 65)
    return c


def whisper_cipher(text: str, shift: int) -> str:
    return "".join(shift_char(c, shift) for c in text)


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
