import requests
import json
from bs4 import BeautifulSoup as bs
quotes = []
url = "http://quotes.toscrape.com/"
while url:
    response = requests.get(url)
    soup = bs(response.text, "html.parser")
    for quote in soup.find_all("div", class_="quote"):
        text = quote.find("span", class_="text").get_text()
        author = quote.find("small", class_="author").get_text()
        quotes.append({"quote": text, "author": author})
    next_button = soup.find("li", class_="next")
    url = next_button.find("a")["href"] if next_button else None
    url = "http://quotes.toscrape.com" + url if url else None

def print_quotes(quotes):
    for idx, quote in enumerate(quotes, 1):
        print(f'{idx}. Quote: {quote["quote"]}; Author: {quote["author"]};')

print_quotes(quotes)

def save_to_json(quotes,file="data.json"):
    with open(file,"w",encoding="utf-8")as f:
        json.dump(quotes, f, ensure_ascii=False, indent=4)

save_to_json(quotes)