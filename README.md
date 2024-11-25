# Nono archive to Sqlite

I always wanted to try out sqlite, now I have an opportunity to use it for something cool !

## 📖 Usage
1. Get / Generate an archive from the [nonograms-archive](https://github.com/Dorifor/nonograms-archive) repo
2. Use the python script to create and populate an sqlite database
3. Profit

## 🧙‍♂️ Trivia
It's actually very fast, since it was quite a lot of lines I had to parse and insert I thought it'd be slow. For the record it only takes about 6 secondes to completely insert all 70000 nonograms of the archive, quite impressive !

## ⚠️ Warnings
I used a [fairly new](https://docs.python.org/3.13/library/array.html#array.array.clear) method from Python 3.13, it may break down if you have an earlier version.
