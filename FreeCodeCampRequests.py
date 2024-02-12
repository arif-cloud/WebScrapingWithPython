# -*- coding: utf-8 -*-

import pandas as pd
import requests
from bs4 import BeautifulSoup
import json

data = pd.read_csv("free_code_articles.csv")
urlList = data['Url List'].tolist()

articleList = []

def tag_converter(tag_string):
    tag_mapping = {
        "c#" : "C#",
        "Sql" : "SQL",
        "iOS" : "IOS"
    }
    return tag_mapping.get(tag_string, tag_string)

for url in urlList:
    page = requests.get(url)
    if(page.status_code == 200):
        soup = BeautifulSoup(page.content, "html.parser")
        articles = soup.find_all('article', attrs={"class":"post-card"})
        for article in articles:
            try:
                postCardTitle = article.find('h2', attrs={"class":"post-card-title"}).findChild()
                url = "https://www.freecodecamp.org/"+postCardTitle['href']
                title = postCardTitle.get_text().strip()
                imageUrlList = article.find('img', attrs={"class":"post-card-image"})['srcset'].split(",")
                if(len(imageUrlList)==1):
                    imageUrl = imageUrlList[0].strip()
                else:
                    imageUrl = imageUrlList[1].strip()[:-5]
                publishDate = article.find('time')['datetime'][4:15]
                tags = []
                tag = article.find('span', attrs={"class":"post-card-tags"}).findChild().get_text().strip()[1:]
                tags.append(tag_converter(tag))
                articleData = [url, title, imageUrl, publishDate, json.dumps(tags)]
                if articleData not in articleList:
                    articleList.append(articleData)
            except:
                print("Error !") 
    else:
        print("URL Not Found",url)
    
df = pd.DataFrame(articleList, columns=["url","title","imageUrl","publishDate","tags"])
df.to_csv('free_code_camp_article_data.csv', index=False)