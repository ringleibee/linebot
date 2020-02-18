
from flask import Flask, request, abort,render_template,redirect
import os
from bs4 import BeautifulSoup
import requests
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage,PostbackEvent,JoinEvent, TextSendMessage,TemplateSendMessage, ButtonsTemplate,
    PostbackAction, MessageAction,
    URIAction, DatetimePickerAction,
    ConfirmTemplate, CarouselTemplate, CarouselColumn,
    ImageCarouselTemplate, ImageCarouselColumn
)

import psycopg2
from contextlib import closing
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

#環境変数取得
ACCESS_TOKEN = os.environ["MY_CHANNEL_ACCESS_TOKEN"]
SECRET = os.environ["MY_CHANNEL_SECRET"]

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET)



@app.route("/")
def hello_world():
    
     #食べログ文回す (完成したら60にする)
    for i in range(1, 3):
        url = "https://tabelog.com/tokyo/rstLst/lunch/" + str(i) + "/?LstSmoking=0&svd=20200204&svt=1900&svps=2&LstCosT=1&RdoCosTp=1"
        
        response = requests.get(url)
        response.encoding = response.apparent_encoding

        bs = BeautifulSoup(response.text, 'html.parser')

    #店舗名取得
        titles = bs.find_all(class_="list-rst__rst-name-target")

    
    #SQLにInsertするため、店舗名と店舗URLを結合しタプルのリスト
        st = []
        tupleOfList = []
        for contents in titles:
            
            # 第一引数は店舗、第二引数はURL、第三引数は駅
            
            def getStation():
                stDisJun = contents.find_next(class_="list-rst__area-genre").text
                station = re.split('[駅m/0-9]+', stDisJun)
                return station[0]
                        
            content = (contents.text, contents.get('href'), getStation(),)
            tupleOfList.append(content)

    #SQlite
    #PostgreSQL


        
        # dbname = 'tabelogs'
        # user = 'postgres'
        # conn = psycopg2.connect("dbname=tabelogs user=postgres password=" + password)

    dbname =  'database.db'
            
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()

        drop_table = "DROP TABLE IF EXISTS tabelogs"
        create_table = '''create table tabelogs (id integer primary key autoincrement, name varchar(64), url text, station text)'''
        c.execute(drop_table)
        c.execute(create_table)

        insert_sql = 'insert into tabelogs (name, url, station) values (?,?,?)'
        c.executemany(insert_sql, tupleOfList)
        # content = tupleOfList
        # c.executemany(sql, tupleOfList)


        # 一度に複数のSQL文を実行したいときは，タプルのリストを作成した上で
        # executemanyメソッドを実行する
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


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    textData = event.message.text
    if textData in "店長":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="a")


if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)