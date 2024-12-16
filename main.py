import requests
import json
from bs4 import BeautifulSoup as bs
from bs4 import Tag

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


def generate_html(data_file="data.json", template_file="template.html", output_file="index.html"):
    # Загрузка данных из JSON
    with open(data_file, "r", encoding="utf-8") as f:
        quotes = json.load(f)

    # Загрузка HTML-шаблона
    with open(template_file, "r", encoding="utf-8") as f:
        template = f.read()

    # Парсинг шаблона
    soup = bs(template, "html.parser")

    # Нахождение элемента для вставки таблицы
    container = soup.find("div", class_="place-here")
    if not container:
        raise ValueError("В шаблоне отсутствует элемент с классом 'place-here' для вставки таблицы.")

    # Создание таблицы
    table = Tag(name="table", attrs={"class": "quotes-table"})

    # Создание заголовков таблицы
    thead = Tag(name="thead")
    tr_head = Tag(name="tr")
    headers = ["№", "Цитата", "Автор"]
    for header in headers:
        th = Tag(name="th")
        th.string = header
        tr_head.append(th)
    thead.append(tr_head)
    table.append(thead)

    # Создание строк таблицы
    tbody = Tag(name="tbody")
    for idx, quote in enumerate(quotes, start=1):
        tr = Tag(name="tr")

        td_num = Tag(name="td")
        td_num.string = str(idx)
        tr.append(td_num)

        td_quote = Tag(name="td")
        td_quote.string = quote["quote"]
        tr.append(td_quote)

        td_author = Tag(name="td")
        td_author.string = quote["author"]
        tr.append(td_author)

        tbody.append(tr)
    table.append(tbody)

    # Вставка таблицы в шаблон
    container.append(table)

    # Сохранение результата в файл
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(soup.prettify())

# Пример вызова функции
generate_html()
