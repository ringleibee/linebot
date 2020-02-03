
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

app = Flask(__name__)

#環境変数取得
ACCESS_TOKEN = os.environ["MY_CHANNEL_ACCESS_TOKEN"]
SECRET = os.environ["MY_CHANNEL_SECRET"]

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET)

def scraper():
    url = "https://tenbai.blog/"

    response = requests.get(url)
    response.encoding = response.apparent_encoding

    bs = BeautifulSoup(response.text, 'html.parser')

    print("*転売店長ブログ")
    date = bs.find(class_="published")
    title = bs.find(class_="entry-title")
    link = bs.find(class_="entry-read").a.get("href")
    result = "{}\n{}\n{}".format(date.text, title.text, link)
    return result


def scrapo():
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
    return result


   



@app.route("/")
def hello_world():
    return "hello world"


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
            TextSendMessage(text=scraper()))
    elif textData in "スニーカー":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=scrapo()))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="ha?"))
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=scrapo()))


if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)