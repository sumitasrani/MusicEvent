import os
import smtplib
import ssl
import time
import requests
import selectorlib

URL = "http://programmer100.pythonanywhere.com/tours/"


def scrape(url):
    """" Scrape the page source from the URL """
    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    """ Extract data from the scrapped source file """
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(message):
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


def store(event):
    with open("data.txt", 'a') as file:
        file.write(event + "\n")


def read(event):
    with open("data.txt", 'r') as file:
        return file.read()


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        event_check = extract(scraped)
        print(event_check)

        content = read(event_check)
        if event_check != "No upcoming tours":
            if event_check not in content:
                store(event_check)
                send_email(message="Hey, there's a new event")
        time.sleep(2)
