# -*- coding: utf-8 -*-

import pandas as pd
import requests
from bs4 import BeautifulSoup
import json


data = pd.read_csv("devto_articles.csv")
urlList = data['Url List'].tolist()

articleList = []

def tag_converter(tag_string):
    tag_mapping = {
        "ai" : "Artificial Intelligence",
        "webdev": "Web Development",
        "machinelearning" : "Machine Learning",
        "javascript" : "JavaScript",
        "bigdata" : "BigData",
        "datascience" : "Data Science",
        "softwaredevelopment" : "Software Development",
        "computerscience" : "Computer Science",
        "csharp" : "C#",
        "designpatterns" : "Design Patterns",
        "sql" : "SQL",
        "ios" : "IOS",
        "css" : "CSS"
    }
    return tag_mapping.get(tag_string, tag_string.capitalize())

for url in urlList:
    page = requests.get(url)
    if(page.status_code == 200):
        soup = BeautifulSoup(page.content, "html.parser")
        articles = soup.find_all('div', attrs={"class":"crayons-story"})
        for article in articles:
            try:
                heading = article.find('h2', attrs={"class":"crayons-story__title"}).findChild()
                url = "https://dev.to"+heading['href']
                title = heading.get_text().strip()
                imageUrl = heading['data-preload-image']
                if(len(imageUrl) == 0):
                    continue
                publishDate = article.find('time').get_text()
                tags = []
                tagBodies = article.find('div', attrs={"class":"crayons-story__tags"}).findChildren()
                for tagBody in tagBodies:
                    tag = tagBody.get_text()
                    if(len(tag) > 1):
                        tags.append(tag_converter(tag[1:]))
                articleData = [url, title, imageUrl, publishDate, json.dumps(tags)]
                if articleData not in articleList:
                    articleList.append(articleData)
            except:
                print("Error !") 
    else:
        print("URL Not Found",url)
    
df = pd.DataFrame(articleList, columns=["url","title","imageUrl","publishDate","tags"])
df.to_csv('dev_to_article_data.csv', index=False)
    
    