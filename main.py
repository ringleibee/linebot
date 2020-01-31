
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

def hello_world():
    url = "https://tenbai.blog/"

    response = requests.get(url)
    response.encoding = response.apparent_encoding

    bs = BeautifulSoup(response.text, 'html.parser')

    date = bs.find(class_="published")
    title = bs.find(class_="entry-title")
    link = bs.find(class_="entry-read").a.get("href")
    result = "{}\n{}\n{}".format(date.text, title.text, link)
    return result


@app.route("/")
def hello_world():
    url = "https://tenbai.blog/"

    response = requests.get(url)
    response.encoding = response.apparent_encoding

    bs = BeautifulSoup(response.text, 'html.parser')

    date = bs.find(class_="published")
    title = bs.find(class_="entry-title")
    link = bs.find(class_="entry-read").a.get("href")
    result = "{}\n{}\n{}".format(date.text, title.text, link)
    return result


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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=hello_world()))

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)