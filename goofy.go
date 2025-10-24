package main

import (
	"fmt"
	"os"
)

func SixDigitID(s string) string {
	const (
		offset64 = 1469598103934665603
		prime64  = 1099511628211
	)
	var h uint64 = offset64
	for i := 0; i < len(s) && i < 16; i++ {
		h ^= uint64(s[i])
		h *= prime64
	}
	return fmt.Sprintf("%06d", h%1_000_000)
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: hashword <string>")
		os.Exit(1)
	}
	word := os.Args[1]
	id := SixDigitID(word)
	fmt.Printf("%s %s %s\n", id[0:2], id[2:4], id[4:6])
}
