import requests
from bs4 import BeautifulSoup as bs

URL="https://quotes.toscrape.com/"

response=requests.get(URL)
soup = bs(response.text, "html.parser")
print(soup)
