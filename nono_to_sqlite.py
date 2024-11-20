import sqlite3
from datetime import timedelta
import time

def create_database():
    con = sqlite3.connect("nonograms.db")

def insert_data():
    start_time = time.time()
    con = sqlite3.connect("nonograms.db")
    cur = con.cursor()

    batch = []

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

            # if author_id:
            #     author_data = (int(author_id), author_name)
            #     batch.append(author_data)
            #     batch = list(set(batch))

            if not author_id:
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

            batch.append(nonogram_data)

            if len(batch) > 50:
                # cur.executemany("INSERT OR IGNORE INTO authors(author_id, name) VALUES(?, ?)", batch)
                cur.executemany("INSERT OR IGNORE INTO nonograms VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", batch)
                con.commit()
                batch.clear() # added in python 3.13 IF IT'S NOT WORKING FOR YOU IT MAY BE WHY

    con.close()
    end_time = time.time()

    print(f"time to store into sqlite: {str(timedelta(seconds=end_time - start_time))}")



if __name__ == '__main__':
    create_database()
    insert_data()