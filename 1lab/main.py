import sqlite3
import pandas as pd

# создаем базу данных и устанавливаем соединение с ней
connection = sqlite3.connect('./Databases/store(1).db')

print('1 задание')
df1 = pd.read_sql('''
SELECT 
    author.name_author AS Имя_автора,
    book.genre_id,
    book.title AS Название_книги,
    book.price AS Цена_книги 
FROM author, book
WHERE book.genre_id = 1 AND book.price > 300 AND book.price < 600 AND author.author_id = book.author_id;
''', connection)
print(df1)
print('\n')

print('2 задание')
df2 = pd.read_sql('''
SELECT client.name_client,
	   SUM(buy_book.amount) AS "Количество"
FROM client, buy_book, buy
WHERE buy.client_id = client.client_id
      AND buy.buy_id = buy_book.buy_id
GROUP BY client.name_client
UNION
SELECT client.name_client, "0"
FROM client
WHERE client.client_id NOT IN (
    SELECT buy.client_id
    FROM buy
)
ORDER BY client.name_client ASC;
''', connection)
print(df2)
print('\n')

print('Задание 3')
df3 = pd.read_sql('''
SELECT
    author.name_author AS "Автор",
    SUM(buy_book.amount) AS "Количество_проданных_книг"
FROM buy_book, author, book
WHERE buy_book.book_id = book.book_id AND author.author_id = book.author_id
GROUP BY author.name_author
HAVING SUM(buy_book.amount) > (
    SELECT SUM(buy_book.amount)
    FROM buy_book, book
    WHERE book.book_id = buy_book.book_id
    GROUP BY book.author_id
);
''', connection)
print(df3)
print('\n')

print('Задание 4')
cursor = connection.cursor()
cursor.executescript('''
UPDATE book
SET price = price * 1.1
WHERE book_id IN (
    SELECT buy_book.book_id
    FROM buy_book
    GROUP BY buy_book.book_id
    HAVING SUM(buy_book.amount) > (
  	    SELECT AVG(amount)
  	    FROM buy_book
    )
);

UPDATE book
SET price = price * 0.95
WHERE book_id NOT IN (
    SELECT buy_book.book_id
    FROM buy_book
    GROUP BY buy_book.book_id
    HAVING SUM(buy_book.amount) > (
  	    SELECT AVG(amount)
  	    FROM buy_book
    )
);
''')
df4 = pd.read_sql('''
SELECT *
from book;
''', connection)
print(df4)
print('\n')

print('Задание 5')
cur = connection.cursor()
cursor.execute('''
SELECT name_author AS "Автор",
    title || ". " || COALESCE(
        lead(title) OVER (
            PARTITION BY name_author
            ORDER BY name_author,
                price DESC
        ),
        FIRST_VALUE(title) OVER (
            PARTITION BY name_author
            ORDER BY name_author,
                price DESC
        )
    ) AS title12,
    price AS "Стоимость",
    COALESCE(
        lead(price) OVER (
            PARTITION BY name_author
            ORDER BY name_author,
                price DESC
        ),
        MAX(price) OVER (PARTITION BY name_author)
    ) AS "Стоимость2",
    ROUND(
        (
            price + COALESCE(
                lead(price) OVER (
                    PARTITION BY name_author
                    ORDER BY name_author,
                        price DESC
                ),
                FIRST_VALUE(price) OVER (PARTITION BY name_author)
            )
        ) * 0.75,
        2
    ) AS "summa"
FROM book
    JOIN author ON author.author_id = book.author_id;
''')
for e in cursor.fetchall():
    print(e, end="\n")

# закрываем соединение с базой
connection.close()
