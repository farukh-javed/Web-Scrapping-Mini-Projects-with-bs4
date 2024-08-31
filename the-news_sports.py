import requests
from bs4 import BeautifulSoup
import json

url = "https://www.thenews.com.pk/latest/category/sports"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

articles_list = soup.find_all('li')

news_data = []

for article in articles_list:
    news_item = {}

    headline_tag = article.find('h2')
    if headline_tag and headline_tag.a:
        news_item['headline'] = headline_tag.a.get_text(strip=True)
        link = headline_tag.a['href']
    else:
        continue

    description_tag = article.find('p')
    news_item['description'] = description_tag.get_text(strip=True) if description_tag else 'No description available'

    image_tag = article.find('a', class_='open-section latest-page-img')
    if image_tag and image_tag.img:
        news_item['image'] = image_tag.img['src']
    else:
        news_item['image'] = 'No image available'

    response1 = requests.get(link)
    soup1 = BeautifulSoup(response1.content, 'html5lib')

    content = soup1.find_all('p')
    full_text = "\n".join([para.get_text(strip=True) for para in content])
    news_item['full_text'] = full_text if full_text else 'No content available'

    news_data.append(news_item)

with open('the_news_sports.json', 'w+') as json_file:
    json.dump(news_data, json_file, indent=4)

print("Scraping complete. Data saved to 'the_news_sports.json'.")
