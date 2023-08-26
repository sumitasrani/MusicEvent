import sqlite3

connection = sqlite3.connect("Data.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM events WHERE date='2023.10.15'")

result = cursor.fetchall()
print(result)

new_row = [('Pink Floyd', 'Navi Mumbai', '2023.10.20')]

cursor.executemany("INSERT INTO events VALUES(?, ?, ?)", new_row)
connection.commit()

cursor.execute("SELECT * FROM events")
result = cursor.fetchall()
print(result)


" INSERT INTO events VALUES ('Tiger', 'Thane', '2023.12.15')"
"SELECT * FROM events WHERE date='2023.10.15'"