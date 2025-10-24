# goofy
reads a word from the command line and prints its 6-digit hash ID — max 16 chars, collisions are fine

```
$ go build -o goofy goofy.go
./goofy 'hello world!'
25 91 44
./goofy 'hello world!!'
53 22 67
./goofy 'hello world!!!'
09 06 22
./goofy 'hello world!!!!'
10 04 61
./goofy 'hello world!!!!!'
63 49 80
./goofy 'hello world!!!!!!'
63 49 80
./goofy 'hello world!!!!!!!'
63 49 80
```

