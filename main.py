import requests
import json
from bs4 import BeautifulSoup as bs

quotes = []
url = "http://quotes.toscrape.com/"

# Сбор данных
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

# Сохранение данных в JSON
def save_to_json(quotes, file="data.json"):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=4)

save_to_json(quotes)

# Генерация HTML через BeautifulSoup
def html(file="data.json", file_html="index.html"):
    with open(file, "r", encoding="utf-8") as f:
        quotes = json.load(f)

    # Создание базового HTML-документа
    soup = bs("<html></html>", "html.parser")

    # Head с заголовком и стилями
    head = soup.new_tag("head")
    title = soup.new_tag("title")
    title.string = "Коллекция цитат для Владика"
    head.append(title)

    style = soup.new_tag("style")
    style.string = """
        body {
            font-family: Arial, sans-serif;
            color: #444;
            background-color: #f0f8ff;
            margin: 40px;
        }
        table {
            width: 100%;
            background: #fff;
            border-collapse: collapse;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        th, td {
            padding: 15px;
            border: 1px solid #ddd;
            text-align: center;
        }
        th {
            background-color: #ff7e5f;
            color: #fff;
        }
        h1 {
            text-align: center;
            color: #ff7e5f;
            margin-bottom: 40px;
        }
        a {
            color: #0077cc;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            font-style: italic;
        }
    """
    head.append(style)
    soup.html.append(head)

    # Body с заголовком и таблицей
    body = soup.new_tag("body")
    h1 = soup.new_tag("h1")
    h1.string = "Коллекция цитат"
    body.append(h1)

    table = soup.new_tag("table")
    # Заголовки таблицы
    thead = soup.new_tag("tr")
    headers = ["№", "Цитата", "Автор"]
    for h in headers:
        th = soup.new_tag("th")
        th.string = h
        thead.append(th)
    table.append(thead)

    # Добавление цитат в таблицу
    for idx, quote in enumerate(quotes, 1):
        tr = soup.new_tag("tr")

        td_num = soup.new_tag("td")
        td_num.string = str(idx)
        tr.append(td_num)

        td_quote = soup.new_tag("td")
        td_quote.string = quote["quote"]
        tr.append(td_quote)

        td_author = soup.new_tag("td")
        td_author.string = quote["author"]
        tr.append(td_author)

        table.append(tr)

    body.append(table)

    # Добавление ссылки на источник
    footer = soup.new_tag("p", **{"class": "footer"})
    source_link = soup.new_tag("a", href="http://quotes.toscrape.com/")
    source_link.string = "Источник: Цитаты для соскребания"
    footer.append(source_link)
    body.append(footer)

    soup.html.append(body)

    # Сохранение в файл
    with open(file_html, "w", encoding="utf-8") as f:
        f.write(soup.prettify())

# Вызов функции для генерации HTML
html()