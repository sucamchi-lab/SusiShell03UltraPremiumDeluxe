#!/usr/bin/env python3


import sys
import os
import ast
import shutil
import subprocess
import tempfile


def _find_function_ranges(source: str) -> list[tuple[int, int]]:
    tree = ast.parse(source)
    ranges: list[tuple[int, int]] = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            ranges.append((node.lineno - 1, node.end_lineno))
    ranges.sort(reverse=True)
    return ranges


def _patch_solution(solution_path: str, work_dir: str) -> str:
    with open(solution_path, "r", encoding="utf-8") as fh:
        source = fh.read()

    lines = source.splitlines(keepends=True)
    ranges = _find_function_ranges(source)

    for start, end in ranges:
        del lines[start:end]

    insert_at = 0
    if lines and lines[0].lstrip().startswith(('"""', "'''")):
        quote = lines[0].lstrip()[:3]
        for i in range(1, len(lines)):
            if quote in lines[i]:
                insert_at = i + 1
                break
        else:
            insert_at = 1
    lines.insert(insert_at, "from _solution import *\n")

    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8", dir=work_dir
    )
    tmp.writelines(lines)
    tmp.close()
    return tmp.name


def main() -> int:
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <solution_file> <user_file> <work_dir>",
              file=sys.stderr)
        return 2

    solution_file = sys.argv[1]
    user_file = sys.argv[2]
    work_dir = sys.argv[3]

    expected = subprocess.run(
        ["python3", os.path.basename(solution_file)],
        capture_output=True, text=True,
        cwd=os.path.dirname(solution_file),
    )

    syntax = subprocess.run(
        ["python3", "-c",
         f"import py_compile; py_compile.compile({user_file!r}, doraise=True)"],
        capture_output=True, text=True,
    )
    if syntax.returncode != 0:
        print("\033[1;31mSYNTAX ERROR in your file:\033[0m")
        print(syntax.stderr)
        return 1

    dest = os.path.join(work_dir, "_solution.py")
    shutil.copy2(user_file, dest)

    patched = _patch_solution(solution_file, work_dir)
    patched_basename = os.path.basename(patched)

    try:
        actual = subprocess.run(
            ["python3", patched_basename],
            capture_output=True, text=True, cwd=work_dir, timeout=10,
        )
    except subprocess.TimeoutExpired:
        print("\033[1;31mTIMEOUT — your code may have an infinite loop.\033[0m")
        os.unlink(patched)
        return 1

    os.unlink(patched)

    if actual.returncode != 0:
        print("\033[1;31mRUNTIME ERROR:\033[0m")
        for line in actual.stderr.splitlines():
            if patched_basename in line:
                continue
            print(line)
        return 1

    exp_lines = expected.stdout.strip().splitlines()
    act_lines = actual.stdout.strip().splitlines()

    failed = [l for l in act_lines if l.startswith("[FAIL]")]
    missing_ok = [l for l in exp_lines
                  if l.startswith("[OK]") and l not in set(act_lines)]

    if not failed and not missing_ok and exp_lines == act_lines:
        print("\033[1;32mALL TESTS PASSED!\033[0m")
        return 0

    for line in failed:
        print(f"\033[1;31m{line}\033[0m")
    for line in missing_ok:
        print(f"\033[1;33mMISSING OK: {line}\033[0m")

    print()
    print("\033[1;33m--- Expected output ---\033[0m")
    print(expected.stdout, end="")
    print("\033[1;31m--- Your output ---\033[0m")
    print(actual.stdout, end="")
    return 1


if __name__ == "__main__":
    sys.exit(main())
