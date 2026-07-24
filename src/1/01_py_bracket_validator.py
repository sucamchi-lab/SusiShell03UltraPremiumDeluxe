"""
py_bracket_validator.py

Check whether the brackets in a string are valid: every opening bracket
must be closed by the same type of bracket, in the correct order.

Allowed brackets: (), [], {}
"""

PAIRS = {')': '(', ']': '[', '}': '{'}
OPENERS = set(PAIRS.values())
CLOSERS = set(PAIRS.keys())


def bracket_validator(s: str) -> bool:
    stack = []

    for char in s:
        if char in OPENERS:
            stack.append(char)
        elif char in CLOSERS:
            if not stack or stack.pop() != PAIRS[char]:
                return False         # any other character is ignored

    # check if there are any unclosed brackets left
    return not stack


if __name__ == "__main__":
    tests = [
        ("()", True),
        ("()[]{}", True),
        ("(]", False),
        ("([)]", False),
        ("{[]}", True),
        ("hello(world)", True),
        ("((())", False),
        ("", True),
    ]

    for value, expected in tests:
        result = bracket_validator(value)
        status = "OK" if result == expected else "FAIL"
        print(f"[{status}] bracket_validator({value!r}) -> {result}")
