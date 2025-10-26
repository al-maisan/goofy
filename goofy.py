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
Python implementation of the goofy 6-digit hash ID generator.
Generates the same 6-digit codes as the Go implementation.
"""

import argparse
import sys
from typing import Optional


# Maximum number of UTF-8 bytes to process
MAX_BYTES = 32


def truncate_utf8(s: str, max_bytes: int) -> bytes:
    """
    Truncate string to at most max_bytes UTF-8 bytes,
    ensuring we don't split a multibyte UTF-8 sequence.

    Args:
        s: Input string
        max_bytes: Maximum number of bytes

    Returns:
        Truncated UTF-8 bytes (valid sequence)
    """
    encoded = s.encode('utf-8')
    if len(encoded) <= max_bytes:
        return encoded

    # Truncate and ensure we don't split a multibyte sequence
    # UTF-8 continuation bytes start with 0b10xxxxxx
    truncated = encoded[:max_bytes]

    # Walk backwards to find a valid UTF-8 boundary
    for i in range(len(truncated) - 1, -1, -1):
        # Check if this is NOT a continuation byte (0b10xxxxxx)
        if (truncated[i] & 0b11000000) != 0b10000000:
            # This is a start byte or ASCII, check if valid
            try:
                # Try to decode from this point to verify it's valid
                truncated[:i+1].decode('utf-8')
                return truncated[:i+1]
            except UnicodeDecodeError:
                # This start byte is incomplete, continue backwards
                continue

    # If we can't find a valid boundary, return empty
    return b''


def six_digit_id(s: str, *, spaced: bool = False) -> str:
    """
    Generate a 6-digit ID from a string using FNV-1a hash.

    Processes up to the first MAX_BYTES (32) bytes of UTF-8 encoding,
    ensuring multibyte sequences are not split.

    Args:
        s: Input string
        spaced: If True, format as "XX XX XX", otherwise "XXXXXX"

    Returns:
        6-digit string (000000-999999), optionally spaced

    Example:
        >>> six_digit_id("hello world!")
        '259144'
        >>> six_digit_id("hello world!", spaced=True)
        '25 91 44'

    Note:
        Collisions are expected and acceptable.
        NOT suitable for security, authentication, or stable unique IDs.
    """
    # FNV-1a 64-bit constants
    OFFSET64 = 1469598103934665603
    PRIME64 = 1099511628211
    MASK64 = 0xFFFFFFFFFFFFFFFF  # 64-bit mask

    # Truncate to MAX_BYTES without splitting UTF-8 sequences
    bytes_data = truncate_utf8(s, MAX_BYTES)

    h = OFFSET64
    for byte in bytes_data:
        # XOR with byte value
        h ^= byte
        # Multiply by prime and mask to 64 bits
        h = (h * PRIME64) & MASK64

    # Format as 6-digit string
    result = f"{h % 1_000_000:06d}"

    if spaced:
        return f"{result[0:2]} {result[2:4]} {result[4:6]}"
    return result


def main() -> int:
    """
    CLI entry point.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        description='Generate a 6-digit hash ID from a string.',
        epilog='''
Examples:
  %(prog)s "hello world"          # outputs: 25 91 44
  %(prog)s -plain "hello world"   # outputs: 259144

Exit codes:
  0 - success
  1 - invalid usage
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'string',
        help='input string to hash'
    )
    parser.add_argument(
        '-plain',
        action='store_true',
        help='output as plain 6-digit string (default: spaced format)'
    )

    args = parser.parse_args()

    # Generate and output the ID
    id_str = six_digit_id(args.string, spaced=not args.plain)
    print(id_str)

    return 0


if __name__ == "__main__":
    sys.exit(main())
