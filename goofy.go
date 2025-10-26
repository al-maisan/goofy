// goofy - 6-digit hash ID generator
// Copyright (C) 2025 Muharem Hrnjadovic <m@sky1.vip>
//
// SPDX-License-Identifier: GPL-3.0-or-later
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

package main

import (
	"flag"
	"fmt"
	"os"
	"unicode/utf8"
)

const (
	// MaxBytes is the maximum number of UTF-8 bytes processed
	MaxBytes = 32
)

// sixDigitID generates a 6-digit ID from a string using FNV-1a hash.
// It processes up to the first MaxBytes (32) bytes of UTF-8 encoding,
// ensuring multibyte sequences are not split.
//
// Returns a 6-digit string (000000-999999).
// Collisions are expected and acceptable.
func sixDigitID(s string) string {
	const (
		offset64 = 1469598103934665603
		prime64  = 1099511628211
	)

	// Truncate to MaxBytes without splitting UTF-8 sequences
	truncated := truncateUTF8(s, MaxBytes)

	var h uint64 = offset64
	for i := 0; i < len(truncated); i++ {
		h ^= uint64(truncated[i])
		h *= prime64
	}
	return fmt.Sprintf("%06d", h%1_000_000)
}

// truncateUTF8 truncates s to at most maxBytes bytes,
// ensuring we don't split a multibyte UTF-8 sequence.
func truncateUTF8(s string, maxBytes int) string {
	if len(s) <= maxBytes {
		return s
	}

	// Find the last valid rune boundary at or before maxBytes
	for i := maxBytes; i > 0; i-- {
		if utf8.RuneStart(s[i]) {
			return s[:i]
		}
	}

	// If we can't find a valid boundary, return empty
	return ""
}

// formatSpaced formats a 6-digit ID as "XX XX XX"
func formatSpaced(id string) string {
	if len(id) != 6 {
		return id
	}
	return fmt.Sprintf("%s %s %s", id[0:2], id[2:4], id[4:6])
}

func main() {
	plain := flag.Bool("plain", false, "output as plain 6-digit string")
	help := flag.Bool("h", false, "show help")

	flag.Usage = func() {
		fmt.Fprintf(os.Stderr, "Usage: %s [options] <string>\n\n", os.Args[0])
		fmt.Fprintf(os.Stderr, "Generate a 6-digit hash ID from a string.\n\n")
		fmt.Fprintf(os.Stderr, "Options:\n")
		flag.PrintDefaults()
		fmt.Fprintf(os.Stderr, "\nExamples:\n")
		fmt.Fprintf(os.Stderr, "  %s \"hello world\"        # outputs: 25 91 44\n", os.Args[0])
		fmt.Fprintf(os.Stderr, "  %s -plain \"hello world\" # outputs: 259144\n", os.Args[0])
		fmt.Fprintf(os.Stderr, "\nExit codes:\n")
		fmt.Fprintf(os.Stderr, "  0 - success\n")
		fmt.Fprintf(os.Stderr, "  1 - invalid usage\n")
	}

	flag.Parse()

	if *help {
		flag.Usage()
		os.Exit(0)
	}

	if flag.NArg() < 1 {
		fmt.Fprintf(os.Stderr, "Error: missing required argument <string>\n\n")
		flag.Usage()
		os.Exit(1)
	}

	word := flag.Arg(0)
	id := sixDigitID(word)

	// -plain overrides -spaced
	if *plain {
		fmt.Println(id)
	} else {
		fmt.Println(formatSpaced(id))
	}
}
