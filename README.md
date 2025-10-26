# goofy

Generates a 6-digit hash ID from a string — max 32 bytes (UTF-8), collisions are fine

Available in both Go and Python implementations that produce identical results.

## ⚠️ Important Limitations

**NOT suitable for:**
- Security or authentication
- Cryptographic purposes
- Stable unique identifiers
- Access control or authorization
- Cases where uniqueness is critical

**Collisions are expected and acceptable.** This is a lossy hash for human-friendly short IDs only.

## Go Implementation

### Installation

```bash
go build -o goofy goofy.go
```

### Usage

```bash
# Default: spaced format
$ ./goofy "hello world!"
25 91 44

# Plain format (6 digits, no spaces)
$ ./goofy -plain "hello world!"
259144

# Help
$ ./goofy -h
```

### Examples

```bash
$ ./goofy "hello world!"
25 91 44
$ ./goofy "hello world!!"
53 22 67
$ ./goofy "hello world!!!"
09 06 22
$ ./goofy "hello world!!!!"
10 04 61
$ ./goofy "hello world!!!!!"
63 49 80

# Demonstrates 32-byte truncation (same hash for >32 bytes)
$ ./goofy "12345678901234567890123456789012"
28 49 45
$ ./goofy "12345678901234567890123456789012!"
28 49 45
$ ./goofy "12345678901234567890123456789012!!"
28 49 45
```

### Exit Codes

- `0` - Success
- `1` - Invalid usage (missing argument)

## Python Implementation

### Requirements

Python 3.6+ (uses only standard library, no additional packages needed)

### CLI Usage

```bash
# Default: spaced format
$ python3 goofy.py "hello world!"
25 91 44

# Plain format
$ python3 goofy.py -plain "hello world!"
259144

# Help
$ python3 goofy.py -h

# Make executable (optional)
$ chmod +x goofy.py
$ ./goofy.py "hello world!"
25 91 44
```

### Library Usage

```python
from goofy import six_digit_id

# Default format (plain)
code = six_digit_id("hello world!")
print(code)  # Output: "259144"

# Spaced format
code = six_digit_id("hello world!", spaced=True)
print(code)  # Output: "25 91 44"
```

### Exit Codes

- `0` - Success
- `1` - Invalid usage

## Testing

Run the test suite to verify both implementations produce identical results:

```bash
$ python3 test_goofy.py
```

The test suite includes:
- All examples from this README
- Edge cases (empty strings, Unicode, special characters)
- UTF-8 multibyte boundary tests (verifies 32-byte limit without splitting sequences)
- Cross-language compatibility verification
- 20+ comprehensive test cases

## How It Works

Both implementations use the FNV-1a 64-bit hash algorithm:

1. **Input processing:**
   - Takes input string and encodes as UTF-8
   - Truncates to first 32 bytes **without splitting multibyte sequences**
   - Example: If byte 32 falls in the middle of a 3-byte character, truncates at byte 30

2. **Hashing:**
   - Applies FNV-1a 64-bit hash over the truncated bytes
   - Constants: `offset = 1469598103934665603`, `prime = 1099511628211`

3. **Output:**
   - Takes hash modulo 1,000,000 to get range `000000-999999`
   - Always zero-padded to 6 digits
   - CLI default: spaced format `"XX XX XX"`
   - Library default: plain format `"XXXXXX"`

### FNV-1a Algorithm

```
hash = offset_basis (64-bit)
for each byte:
    hash = hash XOR byte
    hash = hash * FNV_prime
return (hash mod 1,000,000) formatted as 6 digits
```

## API Reference

### Go

**Note:** The Go implementation is in `package main` (CLI tool). Functions are not exported for library use. If you need a Go library, copy the implementation into your own package.

Internal implementation (for reference):
```go
// sixDigitID generates a 6-digit ID from a string
func sixDigitID(s string) string

// formatSpaced formats a 6-digit ID as "XX XX XX"
func formatSpaced(id string) string

// truncateUTF8 safely truncates to max bytes without splitting UTF-8
func truncateUTF8(s string, maxBytes int) string
```

### Python

```python
def six_digit_id(s: str, *, spaced: bool = False) -> str:
    """
    Generate a 6-digit ID from a string.

    Args:
        s: Input string
        spaced: If True, format as "XX XX XX", otherwise "XXXXXX"

    Returns:
        6-digit string (000000-999999)
    """

def truncate_utf8(s: str, max_bytes: int) -> bytes:
    """
    Truncate string to max_bytes without splitting UTF-8 sequences.
    """
```

## Development

### Module Structure

```
goofy/
├── goofy.go           # Go implementation (library + CLI)
├── goofy.py           # Python implementation (library + CLI)
├── test_goofy.py      # Test suite
├── go.mod             # Go module file
├── README.md          # This file
└── LICENSE            # License file
```

### Adding Tests

Both implementations include:
- UTF-8 safe truncation
- Consistent output formatting
- Proper error handling
- Comprehensive documentation

When adding tests, ensure:
1. Both Go and Python produce identical output
2. Test cases include UTF-8 edge cases
3. Document expected behavior for edge cases

## License

This project is licensed under the GNU General Public License v3.0 or later (GPL-3.0-or-later).

**Copyright (C) 2025 Muharem Hrnjadovic <m@sky1.vip>**

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the [LICENSE](LICENSE) file for more details.
