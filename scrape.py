from bs4 import BeautifulSoup
import requests
from datetime import datetime

url = "https://sneakerhack.com/"

response = requests.get(url)
response.encoding = response.apparent_encoding

bs = BeautifulSoup(response.text, 'html.parser')

print("*スニーカーハック")
d = bs.find(class_="entry-date")
title = bs.find(class_="title")
desc = bs.find(class_="excerpt")
link = bs.find(class_="num1").a.get("href")
# result = "{}\n{}\n{}".format(date.text, title.text, link)
# print(result)

dWithoutpiriodo = d.text
date = dWithoutpiriodo.replace('.', '/')

result = "{}\n{}\n{}\n{}".format(date, title.text, desc.text, link)

print(result)