from bs4 import BeautifulSoup
import requests
from datetime import datetime

url = "https://tenbai.blog/"

response = requests.get(url)
response.encoding = response.apparent_encoding

bs = BeautifulSoup(response.text, 'html.parser')

date = bs.find(class_="published")
title = bs.find(class_="entry-title")
link = bs.find(class_="entry-read").a.get("href")
result = "{}\n{}\n{}".format(date.text, title.text, link)
print(result)

