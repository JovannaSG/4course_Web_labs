import sqlite3
import pandas as pd


# создаем базу данных и устанавливаем соединение с ней
connection = sqlite3.connect('./Databases/store(1).db')

# выводим всех авторов
authors = pd.read_sql('''
SELECT *
FROM author
''', connection)
print(authors)
print('\n')
'''
   author_id       name_author
0          1     Булгаков М.А.
1          2  Достоевский Ф.М.
2          3       Есенин С.А.
3          4    Пастернак Б.Л.
4          5    Лермонтов М.Ю.
'''

# выводим все книги
curs = connection.cursor()
curs.executescript('''
UPDATE book
SET price = 670.99
WHERE book_id = 1;
UPDATE book
SET price = 540.50
WHERE book_id = 2;
UPDATE book
SET price = 460.00
WHERE book_id = 3;
UPDATE book
SET price = 799.01
WHERE book_id = 4;
UPDATE book
SET price = 480.50
WHERE book_id = 5;
UPDATE book
SET price = 650.00
WHERE book_id = 6;
UPDATE book
SET price = 570.20
WHERE book_id = 7;
UPDATE book
SET price = 518.99
WHERE book_id = 8;
''')
books = pd.read_sql('''
SELECT *
FROM book
''', connection)
print(books)
print('\n')
'''
 book_id                  title  author_id  genre_id   price  amount
0        1     Мастер и Маргарита          1         1  670.99       3
1        2          Белая гвардия          1         1  540.50       5
2        3                  Идиот          2         1  460.00      10
3        4      Братья Карамазовы          2         1  799.01       3
4        5                  Игрок          2         1  480.50      10
5        6  Стихотворения и поэмы          3         2  650.00      15
6        7         Черный человек          3         2  570.20       6
7        8                 Лирика          4         2  518.99       2
'''

# выводим все жанры
genres = pd.read_sql('''
SELECT *
FROM genre
''', connection)
print(genres)
print('\n')
'''
   genre_id   name_genre
0         1        Роман
1         2       Поэзия
2         3  Приключения
'''

# выводим всех клиентов
clients = pd.read_sql('''
SELECT *
FROM client
''', connection)
print(clients)
print('\n')
'''
   client_id      name_client  city_id           email
0          1    Баранов Павел        3    baranov@test
1          2    Абрамова Катя        1   abramova@test
2          3   Семенонов Иван        2    semenov@test
3          4  Яковлева Галина        1  yakovleva@test
'''

# выводим table buy
buyings = pd.read_sql('''
SELECT *
FROM buy
''', connection)
print(buyings)
print('\n')
'''
   buy_id                        buy_description  client_id
0       1                Доставка только вечером          1
1       2                                   None          3
2       3  Упаковать каждую книгу по отдельности          2
3       4                                   None          1
'''

# выводим table buy_book
buy_books = pd.read_sql('''
SELECT *
FROM buy_book
''', connection)
print(buy_books)
print('\n')
'''
   buy_book_id  buy_id  book_id  amount
0            1       1        1       1
1            2       1        7       2
2            3       1        3       1
3            4       2        8       2
4            5       3        3       2
5            6       3        2       1
6            7       3        1       1
7            8       4        5       1
'''
