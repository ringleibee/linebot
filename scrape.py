from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd

# def src():
#     def scraper():
#         url = "https://tenbai.blog/"

#         response = requests.get(url)
#         response.encoding = response.apparent_encoding

#         bs = BeautifulSoup(response.text, 'html.parser')

#         print("*転売店長ブログ")
#         date = bs.find(class_="published")
#         title = bs.find(class_="entry-title")
#         link = bs.find(class_="entry-read").a.get("href")
#         result = "{}\n{}\n{}".format(date.text, title.text, link)
#         return result


#     def scrapo():
#         url = "https://sneakerhack.com/"

#         response = requests.get(url)
#         response.encoding = response.apparent_encoding

#         bs = BeautifulSoup(response.text, 'html.parser')

#         print("*スニーカーハック")
#         d = bs.find(class_="entry-date")
#         title = bs.find(class_="title")
#         desc = bs.find(class_="excerpt")
#         link = bs.find(class_="num1").a.get("href")
#         # result = "{}\n{}\n{}".format(date.text, title.text, link)
#         # print(result)

#         dWithoutpiriodo = d.text
#         date = dWithoutpiriodo.replace('.', '/')

#         result = "{}\n{}\n{}\n{}".format(date, title.text, desc.text, link)
#         return result

#     tentyo = scraper()
#     sneaker = scrapo()







# src()


import sqlite3
from contextlib import closing



for i in range(1, 3):
    url = "https://tabelog.com/tokyo/rstLst/lunch/" + str(i) + "/?LstSmoking=0&svd=20200204&svt=1900&svps=2&LstCosT=1&RdoCosTp=1"
    
    response = requests.get(url)
    response.encoding = response.apparent_encoding

    bs = BeautifulSoup(response.text, 'html.parser')

    titles = bs.find_all(class_="list-rst__rst-name-target")
    links = bs.find_all("href")

    tupleOfList = []
    for contents in titles:
        content = (contents.text, contents.get('href'),)
        tupleOfList.append(content)
        

    # tupleOfListNames = []
    # for ti in titles:
    #     name = ti.text,
    #     tupleOfListNames.append(name)


dbname =  'database.db'
        
with closing(sqlite3.connect(dbname)) as conn:
    c = conn.cursor()

    drop_table = "DROP TABLE IF EXISTS tabelogs"
    create_table = '''create table tabelogs (id integer primary key autoincrement, name varchar(64), url text)'''
    c.execute(drop_table)
    c.execute(create_table)

    sql= 'insert into tabelogs (name, url) values (?, ?)'
    content = tupleOfList
    c.executemany(sql, tupleOfList)



    # insertLinks= 'insert into tabelogs (url) values (?)'
    
    # c.executemany(insertLinks, url)


    # 一度に複数のSQL文を実行したいときは，タプルのリストを作成した上で
    # executemanyメソッドを実行する
    # insert_sql = 'insert into users (id, name, age, gender) values (?,?,?,?)'
    # users = [
    #     (2, 'Shota', 54, 'male'),
    #     (3, 'Nana', 40, 'female'),
    #     (4, 'Tooru', 78, 'male'),
    #     (5, 'Saki', 31, 'female')
    # ]
    # c.executemany(insert_sql, users)
    conn.commit()

    select_sql = 'select * from tabelogs'
    for row in c.execute(select_sql):
        print(row)
