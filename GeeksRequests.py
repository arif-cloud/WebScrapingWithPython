# -*- coding: utf-8 -*-

import pandas as pd
import requests
from bs4 import BeautifulSoup
import json

data = pd.read_csv("geeks_articles.csv")
urlList = data['Url List'].tolist()

articleList = []

for url in urlList:
    page = requests.get(url)
    if(page.status_code == 200):
        soup = BeautifulSoup(page.content, "html.parser")
        articles = soup.find_all('div', attrs={"class":"article_container2"})
        for article in articles:
            try:
                heading = article.find('a', attrs={"class":"article_heading"})
                url = heading['href']
                title = heading['title']
                imageUrl = article.find('img', attrs={"alt":"image"})['src']
                publishDate = article.find('div', attrs={"class":"article_date"}).get_text().split(":")[1]
                tags = []
                tagList = article.find_all('div', attrs={"class":"article_tag"})
                for tag in tagList:
                    tags.append(tag.findChild().get_text())
            except:
                print("Error !")
            finally:
                articleData = [url, title, imageUrl, publishDate, json.dumps(tags)]
                if not imageUrl.endswith(".gif"):
                    if articleData not in articleList:
                        articleList.append(articleData)
    else:
        print("URL Not Found",url)
    
df = pd.DataFrame(articleList, columns=["url","title","imageUrl","publishDate","tags"])
df.to_csv('geeks_article_data.csv', index=False)
    
    
    
