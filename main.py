import requests
import json
from bs4 import BeautifulSoup as bs

URL="https://quotes.toscrape.com/"

quotes=[]
response=requests.get(URL)
soup = bs(response.text, "html.parser")
for quote in soup.find_all("div",class_="quote"):
    text=quote.find_all("span",class_="text").get_text()
    author=quote.find_all("small",class_="author").get_text()
    quotes.append({"quote":text,"author":author})
next=soup.find("li",class_="next")
url=next.find("a")["href"]
url