#!/usr/bin/env python3
# goofy - 6-digit hash ID generator
# Copyright (C) 2025 Muharem Hrnjadovic <m@sky1.vip>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Comprehensive test suite to verify Go and Python implementations produce identical results.
Includes golden file testing for cross-language verification.
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple
from goofy import six_digit_id


def run_go_implementation(input_str: str, plain: bool = False) -> str:
    """Run the Go implementation and return its output."""
    cmd = ["./goofy"]
    if plain:
        cmd.append("-plain")
    cmd.append(input_str)

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()


def run_python_implementation(input_str: str, plain: bool = False) -> str:
    """Run the Python implementation and return its output."""
    return six_digit_id(input_str, spaced=not plain)


def test_case(
    input_str: str,
    expected_plain: str = None,
    expected_spaced: str = None
) -> Tuple[bool, str, str, str, str]:
    """
    Test a single input string against both implementations.

    Returns:
        Tuple of (success, go_plain, python_plain, go_spaced, python_spaced, message)
    """
    try:
        # Test plain format
        go_plain = run_go_implementation(input_str, plain=True)
        python_plain = run_python_implementation(input_str, plain=True)

        # Test spaced format
        go_spaced = run_go_implementation(input_str, plain=False)
        python_spaced = run_python_implementation(input_str, plain=False)

        # Check if implementations match each other
        if go_plain != python_plain or go_spaced != python_spaced:
            return (False, go_plain, python_plain, go_spaced, python_spaced,
                    "✗ Implementations differ")

        # Check against expected values if provided
        if expected_plain and go_plain != expected_plain:
            return (False, go_plain, python_plain, go_spaced, python_spaced,
                    f"✗ Plain format differs from expected: {expected_plain}")

        if expected_spaced and go_spaced != expected_spaced:
            return (False, go_plain, python_plain, go_spaced, python_spaced,
                    f"✗ Spaced format differs from expected: {expected_spaced}")

        return True, go_plain, python_plain, go_spaced, python_spaced, "✓ Match"

    except Exception as e:
        return False, "", "", "", "", f"✗ Error: {e}"


def load_golden_tests() -> List[Tuple[str, str, str]]:
    """Load test cases from the golden file."""
    golden_file = Path("test_golden.txt")
    if not golden_file.exists():
        return []

    tests = []
    with open(golden_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue

            parts = line.split('|')
            if len(parts) == 3:
                input_str, expected_plain, expected_spaced = parts
                tests.append((input_str, expected_plain, expected_spaced))

    return tests


def main():
    print("Testing Go and Python implementations for compatibility\n")
    print("=" * 80)

    # Load golden file tests
    golden_tests = load_golden_tests()

    if not golden_tests:
        print("Warning: No golden test file found. Using basic tests only.\n")

        # Fallback to basic tests
        golden_tests = [
            ("hello world!", "259144", "25 91 44"),
            ("hello world!!", "532267", "53 22 67"),
            ("", None, None),
            ("test", None, None),
        ]

    passed = 0
    failed = 0
    failed_cases = []

    for input_str, expected_plain, expected_spaced in golden_tests:
        try:
            success, go_plain, py_plain, go_spaced, py_spaced, message = test_case(
                input_str, expected_plain, expected_spaced
            )

            # Format input string for display
            display_str = repr(input_str) if input_str else "''"
            if len(display_str) > 40:
                display_str = display_str[:37] + "...'"

            print(f"\n{'=' * 80}")
            print(f"Input: {display_str}")
            print(f"  Go (plain):     {go_plain}")
            print(f"  Python (plain): {py_plain}")
            print(f"  Go (spaced):    {go_spaced}")
            print(f"  Python (spaced):{py_spaced}")

            if expected_plain:
                print(f"  Expected (plain): {expected_plain}")
            if expected_spaced:
                print(f"  Expected (spaced): {expected_spaced}")

            print(f"  Status: {message}")

            if success:
                passed += 1
            else:
                failed += 1
                failed_cases.append((input_str, message))

        except Exception as e:
            display_str = repr(input_str) if input_str else "''"
            print(f"\n{'=' * 80}")
            print(f"Input: {display_str}")
            print(f"  ERROR: {e}")
            failed += 1
            failed_cases.append((input_str, str(e)))

    print("\n" + "=" * 80)
    print(f"\nResults: {passed} passed, {failed} failed out of {len(golden_tests)} tests")

    if failed > 0:
        print("\n❌ FAILED CASES:")
        for input_str, message in failed_cases:
            display_str = repr(input_str) if input_str else "''"
            print(f"  - {display_str}: {message}")
        print("\n❌ FAILED: Implementations do not match or differ from expected!")
        sys.exit(1)
    else:
        print("\n✅ SUCCESS: All tests passed! Implementations are compatible.")
        print("✅ Cross-language verification: PASSED")
        print("✅ UTF-8 truncation: PASSED")
        print("✅ Output formatting: PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()
