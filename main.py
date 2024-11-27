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

def html(file="data.json",file_html="index.html"):
    with open(file,"r",encoding="utf-8")as f:
        quotes=json.load(f)
    
    html_cont='''
    <html>
    <head>
        <title>Список цитат</title>
         <style>
            body {
                color: #696969;
            }
            table {
                background: #fff;
            }
            th, td {
                padding: 20px;
                border: 1px solid #ddd;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
                color: #333;
            }
            h1 {
                text-align: center;
                margin-bottom: 40px;
            }
            p {
                text-align: center;
                margin-top: 40px;
            }
            a {
                color: #ff7e5f;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div>
            <h1>Коллекция цитат</h1>
            <table>
                <tr>
                    <th>№</th>
                    <th>Цитата</th>
                    <th>Автор</th>
                </tr>
    '''

    # Добавление цитат в таблицу
    for idx, quote in enumerate(quotes, 1):
        html_cont += f'''
        <tr>
            <td><h3>{idx}</h3></td>
            <td><h3>{quote["quote"]}</h3></td>
            <td><h3>{quote["author"]}<h3>/</td>
        </tr>
        '''

    # Завершение HTML-контента
    html_cont += '''
            </table>
            <p>
                <h2><a href="http://quotes.toscrape.com/">Источник: Цитаты для соскребания</a></h2>
            </p>
        </div>
    </body>
    </html>
    '''

    # Запись HTML-контента в файл
    with open(file_html, "w", encoding="utf-8") as f:
        f.write(html_cont)

# Вызов функции для генерации HTML
html()