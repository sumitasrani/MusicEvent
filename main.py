import requests
import selectorlib

URL = "http://programmer100.pythonanywhere.com/tours/"


def scrape(url):
    """" Scrape the page source from the URL """
    response = requests.get(url)
    text = response.text
    return text

def extract(text):
    """ Extract data from the scrapped source file """
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(text)["tours"]
    return value

if __name__ == "__main__":
    scraped = scrape(URL)
    event_check = extract(scraped)
    print(event_check)



