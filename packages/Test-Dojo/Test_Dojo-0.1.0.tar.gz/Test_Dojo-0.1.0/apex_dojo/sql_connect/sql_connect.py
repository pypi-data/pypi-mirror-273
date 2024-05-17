import pymssql

conn = pymssql.connect(
    server="127.0.0.1",
    user="sa",
    password="1qazXSW@",
    database="test_database",
    as_dict=True,
)

title = "dato"
author = "apex"
genre = "Fantasy"
ISBN = "410"

SQL_QUERY = """
    INSERT INTO book_a (title, author, genre, ISBN)
    VALUES (%s, %s, %s, %s);
"""
cursor = conn.cursor()
cursor.execute(SQL_QUERY, (title, author, genre, ISBN))
conn.commit()

SQL_SELECT = """
    SELECT title, author, genre, ISBN
    FROM book_a;
"""
cursor.execute(SQL_SELECT)
records = cursor.fetchall()
for r in records:
    print(f"{r['title']}\t{r['author']}\t{r['genre']}\t{r['ISBN']}")

cursor.close()
conn.close()
