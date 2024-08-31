import requests
from bs4 import BeautifulSoup
import json

url = "https://www.dawn.com/sport"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

articles = soup.find_all('article')

news_data = []

for article in articles:
    news_item = {}

    headline_tag = article.find('h2', class_='story__title')
    if headline_tag and headline_tag.a:
        news_item['headline'] = headline_tag.a.get_text(strip=True)
        link = headline_tag.a['href']
    else:
        continue

    description_tag = article.find('div', class_='story__excerpt')
    if description_tag:
       news_item['description'] = description_tag.get_text(strip=True)
    else:
       'No description available'

    image_tag = article.find('div', class_='media__item')
    if image_tag and image_tag.img:
        news_item['image'] = image_tag.img['src']
    else:
        news_item['image'] = 'No image available'

    response1 = requests.get(link)
    soup1 = BeautifulSoup(response1.content, 'html5lib')

    content = soup1.find_all('p')
    full_text = "\n".join([para.get_text(strip=True) for para in content])
    if full_text:
       news_item['full_text'] = full_text
    else:
       'No content available'

    news_data.append(news_item)

with open('dawn_sports_news.json', 'w+') as json_file:
    json.dump(news_data, json_file, indent=4)

print("Scraping complete. Data saved to 'dawn_sports_news.json'.")
