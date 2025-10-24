# goofy
reads a word from the command line and prints its 6-digit hash ID — max 16 bytes (UTF-8), collisions are fine

Available in both Go and Python implementations that produce identical results.

## Go Implementation

Build and run:
```bash
$ go build -o goofy goofy.go
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
$ ./goofy "hello world!!!!!!"
63 49 80
$ ./goofy "hello world!!!!!!!"
63 49 80
```

## Python Implementation

The Python implementation (`goofy.py`) produces identical output to the Go version.

**Requirements:** Python 3.6+ (uses only standard library, no additional packages needed)

**Usage:**
```bash
$ python3 goofy.py "hello world!"
25 91 44
$ python3 goofy.py "hello world!!"
53 22 67

# Or make it executable and run directly:
$ chmod +x goofy.py
$ ./goofy.py "hello world!"
25 91 44
```

**Use as a library:**
```python
from goofy import six_digit_id

code = six_digit_id("hello world!")
print(code)  # Output: "259144"
```

## Testing

Run the test suite to verify both implementations produce identical results:

```bash
$ python3 test_goofy.py
```

The test suite includes:
- All examples from this README
- Edge cases (empty strings, Unicode, special characters)
- Long strings (verifies 16-byte limit)
- 17 comprehensive test cases

## How It Works

Both implementations use the FNV-1a 64-bit hash algorithm:
- Processes the first 16 bytes of the UTF-8 encoded input
- Returns the hash modulo 1,000,000 as a 6-digit string (000000-999999)
- Collisions are expected and acceptable for this use case

