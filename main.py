import requests
from bs4 import BeautifulSoup
import json


def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def get_quotes(soup):
    quotes = []
    for quote in soup.select('.quote'):
        text = quote.find('span', class_='text').get_text(strip=True)
        author = quote.find('small', class_='author').get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote.select('.tag')]
        quotes.append({
            'text': text,
            'author': author,
            'tags': tags
        })
    return quotes


def get_authors(soup):
    authors = {}
    for author in soup.select('.author'):
        fullname = author.get_text(strip=True)
        birth_date_element = author.find_next_sibling('span', class_='birthDate')

        if birth_date_element:
            birth_date = birth_date_element.get_text(strip=True)
        else:
            birth_date = "N/A"

        authors[fullname] = {
            'fullname': fullname,
            'born_date': birth_date
        }
    return authors


def main():
    base_url = 'http://quotes.toscrape.com'
    quotes_data = []
    authors_data = {}

    page_number = 1
    while True:
        url = f'{base_url}/page/{page_number}/'
        soup = scrape_page(url)

        if 'No quotes found!' in soup.get_text():
            break

        quotes_data.extend(get_quotes(soup))
        authors_data.update(get_authors(soup))

        page_number += 1

    with open('quotes.json', 'w', encoding='utf-8') as quotes_file:
        json.dump(quotes_data, quotes_file, ensure_ascii=False, indent=2)

    with open('authors.json', 'w', encoding='utf-8') as authors_file:
        json.dump(authors_data, authors_file, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
