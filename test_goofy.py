#!/usr/bin/env python3
"""
Test suite to verify Go and Python implementations produce identical results.
"""

import subprocess
import sys
from typing import List, Tuple
from goofy import six_digit_id


def run_go_implementation(input_str: str) -> str:
    """Run the Go implementation and return its output."""
    result = subprocess.run(
        ["./goofy", input_str],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()


def run_python_implementation(input_str: str) -> str:
    """Run the Python implementation and return its output."""
    id_str = six_digit_id(input_str)
    return f"{id_str[0:2]} {id_str[2:4]} {id_str[4:6]}"


def test_case(input_str: str, expected: str = None) -> Tuple[bool, str, str, str]:
    """
    Test a single input string against both implementations.

    Returns:
        Tuple of (success, go_output, python_output, message)
    """
    go_output = run_go_implementation(input_str)
    python_output = run_python_implementation(input_str)

    if go_output == python_output:
        if expected and go_output != expected:
            return False, go_output, python_output, f"Both match but differ from expected: {expected}"
        return True, go_output, python_output, "✓ Match"
    else:
        return False, go_output, python_output, "✗ Mismatch"


def main():
    print("Testing Go and Python implementations for compatibility\n")
    print("=" * 70)

    # Test cases from README
    test_inputs = [
        ("hello world!", "25 91 44"),
        ("hello world!!", "53 22 67"),
        ("hello world!!!", "09 06 22"),
        ("hello world!!!!", "10 04 61"),
        ("hello world!!!!!", "63 49 80"),
        ("12345678901234567890123456789012", "28 49 45"),
        ("12345678901234567890123456789012!", "28 49 45"),
        ("12345678901234567890123456789012!!", "28 49 45"),
    ]

    # Additional test cases
    additional_tests = [
        ("", None),  # Empty string
        ("a", None),  # Single character
        ("test", None),  # Short string
        ("0123456789", None),  # Numbers
        ("exactly16chars!", None),  # Exactly 16 chars
        ("exactly 32 characters here!!", None),  # Exactly 32 chars
        ("more than 32 characters in this string for testing", None),  # More than 32 chars
        ("more than 32 characters in this string for testing!", None),  # Should match previous (32 byte limit)
        ("UPPERCASE", None),  # Uppercase
        ("MixedCase123", None),  # Mixed case with numbers
        ("special!@#$%^&*", None),  # Special characters
        ("unicode: 你好", None),  # Unicode characters
    ]

    all_tests = test_inputs + additional_tests
    passed = 0
    failed = 0

    for input_str, expected in all_tests:
        try:
            success, go_out, py_out, message = test_case(input_str, expected)

            # Format input string for display
            display_str = repr(input_str)
            if len(display_str) > 30:
                display_str = display_str[:27] + "..."

            print(f"\nInput: {display_str}")
            print(f"  Go:     {go_out}")
            print(f"  Python: {py_out}")
            print(f"  Status: {message}")

            if success:
                passed += 1
            else:
                failed += 1

        except Exception as e:
            print(f"\nInput: {repr(input_str)}")
            print(f"  ERROR: {e}")
            failed += 1

    print("\n" + "=" * 70)
    print(f"\nResults: {passed} passed, {failed} failed out of {len(all_tests)} tests")

    if failed > 0:
        print("\n❌ FAILED: Implementations do not match!")
        sys.exit(1)
    else:
        print("\n✅ SUCCESS: All tests passed! Implementations are compatible.")
        sys.exit(0)


if __name__ == "__main__":
    main()
