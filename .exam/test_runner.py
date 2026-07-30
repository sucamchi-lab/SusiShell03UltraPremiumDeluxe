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


def _patch_solution(solution_path: str, output_dir: str) -> str:
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

    solution_stem = os.path.splitext(os.path.basename(solution_path))[0]
    safe_stem = "".join(
        ch if ch.isalnum() or ch in ("_", "-") else "_" for ch in solution_stem
    )
    patched_filename = f"_patched_{safe_stem}.py"
    patched_path = os.path.join(output_dir, patched_filename)
    with open(patched_path, "w", encoding="utf-8") as fh:
        fh.writelines(lines)
    return patched_path


def _check_syntax(user_file: str) -> str | None:
    try:
        with open(user_file, "r", encoding="utf-8") as fh:
            ast.parse(fh.read(), filename=user_file)
    except SyntaxError as exc:
        message = exc.msg
        line = exc.lineno or 0
        col = exc.offset or 0
        return f'  File "{user_file}", line {line}\n    {message} (column {col})'
    return None


def main() -> int:
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <solution_file> <user_file> <work_dir>",
              file=sys.stderr)
        return 2

    solution_file = sys.argv[1]
    user_file = sys.argv[2]
    work_dir = sys.argv[3]

    subprocess_env = os.environ.copy()
    subprocess_env["PYTHONDONTWRITEBYTECODE"] = "1"

    expected = subprocess.run(
        ["python3", os.path.basename(solution_file)],
        capture_output=True, text=True,
        cwd=os.path.dirname(solution_file), env=subprocess_env,
    )

    syntax_error = _check_syntax(user_file)
    if syntax_error is not None:
        print("\033[1;31mSYNTAX ERROR in your file:\033[0m")
        print(syntax_error)
        return 1

    with tempfile.TemporaryDirectory(prefix="exam_runner_") as run_dir:
        dest = os.path.join(run_dir, "_solution.py")
        shutil.copy2(user_file, dest)

        patched = _patch_solution(solution_file, run_dir)
        patched_basename = os.path.basename(patched)

        try:
            actual = subprocess.run(
                ["python3", patched_basename],
                capture_output=True,
                text=True,
                cwd=run_dir,
                timeout=10,
                env=subprocess_env,
            )
        except subprocess.TimeoutExpired:
            print(
                "\033[1;31mTIMEOUT — your code may have an infinite loop.\033[0m")
            return 1

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
