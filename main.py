import os
import smtplib
import ssl
import time
import requests
import selectorlib
import sqlite3


URL = "http://programmer100.pythonanywhere.com/tours/"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'}


class Tours:
    def scrape(self, url):
        """" Scrape the page source from the URL """
        response = requests.get(url, headers=HEADERS)
        source = response.text
        return source

    def extract(self, source):
        """ Extract data from the scrapped source file """
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tours"]
        return value


class Email:
    def send(self, message):
        host = "smtp.gmail.com"
        port = 465

        username = "sumitasranicoder@gmail.com"
        password = os.getenv("password_event")

        receiver = "sumitasranicoder@gmail.com"
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(username, password)
            server.sendmail(username, receiver, message)
        print("email sent")

class Database:

    def __init__(self, database_path):
        self.connection = sqlite3.connect(database_path)

    def store(self, event):
        row = event.split(",")
        row = [item.strip() for item in row]
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO events VALUES(?, ?, ?)", row)
        self.connection.commit()


    def read(self, event):
        row = event.split(",")
        row = [item.strip() for item in row]
        band, city, date = row
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
        rows = cursor.fetchall()
        print(rows)
        return rows


if __name__ == "__main__":
    while True:
        tours = Tours()
        scraped = tours.scrape(URL)
        event_check = tours.extract(scraped)
        print(event_check)
        if event_check != "No upcoming tours":
            db = Database(database_path="Data.db")
            row = db.read(event_check)
            if not row:
                db.store(event_check)
                newline = "\n"
                email = Email()
                email.send(message="Hey, there's a new event" + f'{newline}{event_check}')
        time.sleep(2)
