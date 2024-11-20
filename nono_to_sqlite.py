import sqlite3
from datetime import timedelta
import time

def create_database():
    con = sqlite3.connect("test.db")
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS "authors" (
            "author_id"	int NOT NULL,
            "name"	varchar(50),
            PRIMARY KEY("author_id")
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS "nonograms" (
            "nonogram_id"	int NOT NULL,
            "title"	varchar(100),
            "is_adult"	boolean,
            "column_count"	int,
            "row_count"	int,
            "colors_count"	int,
            "colors"	varchar(255),
            "column_cells"	varchar(255),
            "column_colors"	varchar(255),
            "row_cells"	varchar(255),
            "row_colors"	varchar(255),
            "author_id"	int,
            PRIMARY KEY("nonogram_id"),
            FOREIGN KEY("author_id") REFERENCES "authors"("author_id")
        );
    """)

    con.commit()
    con.close()


def insert_data():
    start_time = time.time()
    con = sqlite3.connect("test.db")
    cur = con.cursor()

    nonograms_batch = []
    authors_batch = []

    with open('archive.nono', 'r', encoding="utf8", errors="ignore") as file:
        for line in file:
            if line[0] == "#":
                continue

            elements = line.split(';')

            nonogram_id = elements.pop(0)
            author_id = elements.pop(0)
            nonogram_title = elements.pop(0)
            author_name = elements.pop(0)
            is_adult = elements.pop(0) == "1"
            column_count = int(elements.pop(0))
            row_count = int(elements.pop(0))
            color_count = int(elements.pop(0))
            colors = elements.pop(0)

            column_cells = []
            column_colors = []

            for _ in range(column_count):
                column_cells.append(elements.pop(0))

            if color_count == 1:
                elements.pop(0)
                column_colors = None
                colors = None
            else:
                for _ in range(column_count):
                    column_colors.append(elements.pop(0))

            row_cells = []
            row_colors = []

            for _ in range(row_count):
                row_cells.append(elements.pop(0))

            if color_count == 1:
                elements.pop(0)
                row_colors = None
            else:
                for _ in range(row_count):
                    row_colors.append(elements.pop(0))

            if column_colors:
                column_colors = ';'.join(column_colors)

            if row_colors:
                row_colors = ';'.join(row_colors)

            if author_id:
                author_data = (int(author_id), author_name)
                authors_batch.append(author_data)
                authors_batch = list(set(authors_batch))
            else:
                author_id = None

            nonogram_data = (
                nonogram_id,
                nonogram_title,
                is_adult,
                column_count,
                row_count,
                color_count,
                colors,
                ';'.join(column_cells),
                column_colors,
                ';'.join(row_cells),
                row_colors,
                author_id
            )

            nonograms_batch.append(nonogram_data)

            if len(authors_batch) > 50:
                cur.executemany("INSERT OR IGNORE INTO authors(author_id, name) VALUES(?, ?)", authors_batch)
                con.commit()
                authors_batch.clear()

            if len(nonograms_batch) > 50:
                cur.executemany("INSERT OR IGNORE INTO nonograms VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", nonograms_batch)
                con.commit()
                nonograms_batch.clear()  # added in python 3.13 IF IT'S NOT WORKING FOR YOU IT MAY BE WHY

    if len(authors_batch) > 0:
        cur.executemany("INSERT OR IGNORE INTO authors(author_id, name) VALUES(?, ?)", authors_batch)
        con.commit()

    if len(nonograms_batch) > 0:
        cur.executemany("INSERT OR IGNORE INTO nonograms VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", nonograms_batch)
        con.commit()

    con.close()
    end_time = time.time()

    print(f"time to store into sqlite: {str(timedelta(seconds=end_time - start_time))}")


if __name__ == '__main__':
    create_database()
    insert_data()
