#!/usr/bin/env python3
"""
Python implementation of the goofy 6-digit hash ID generator.
Generates the same 6-digit codes as the Go implementation.
"""

import sys


def six_digit_id(s: str) -> str:
    """
    Generate a 6-digit ID from a string using FNV-1a hash.

    Args:
        s: Input string (only first 16 bytes of UTF-8 encoding are used)

    Returns:
        6-digit string (000000-999999)
    """
    # FNV-1a 64-bit constants
    OFFSET64 = 1469598103934665603
    PRIME64 = 1099511628211
    MASK64 = 0xFFFFFFFFFFFFFFFF  # 64-bit mask

    h = OFFSET64
    # Convert string to UTF-8 bytes and process only first 16 bytes
    bytes_data = s.encode('utf-8')
    for i in range(min(len(bytes_data), 16)):
        # XOR with byte value
        h ^= bytes_data[i]
        # Multiply by prime and mask to 64 bits
        h = (h * PRIME64) & MASK64

    # Return 6-digit string
    return f"{h % 1_000_000:06d}"


def main():
    if len(sys.argv) < 2:
        print("Usage: goofy.py <string>")
        sys.exit(1)

    word = sys.argv[1]
    id_str = six_digit_id(word)
    # Format as "XX XX XX"
    print(f"{id_str[0:2]} {id_str[2:4]} {id_str[4:6]}")


if __name__ == "__main__":
    main()
