from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
    FollowEvent, MessageEvent, TextMessage, ImageMessage, ImageSendMessage, 
    TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction
)

import os
app = Flask(__name__)

#環境変数からLINE Access Tokenを設定
MY_CHANNEL_ACCESS_TOKEN = "C6exflgSoQMC692XwTxnQEB1Ze2onSN5mACvCW8VQGxNPYXHf26Q3JWEvr7BepTjf+Q6+Sbq5KvH42vLl9LJqvxLKfocBF/9ArkrZkjemXCfTRIeKXyF07THbVQosj8bqmWNpFvUxvEsfdwqBi2P0gdB04t89/1O/w1cDnyilFU="

#環境変数からLINE Channel Secretを設定
MY_CHANNEL_SECRET = "c0107250e6d78be8919c4c30f60254e9S"

line_bot_api = LineBotApi(MY_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(MY_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    #get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    #get request body as text
    body = request.get_dadta(as_text=True)
    app.logger.info("Request body: " + body)

    #handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

#MessageEvent
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=' 「' + event.message.text + '」って何？')
    )

if __name__ == "__main__":
    port = os.getenv("PORT")
    app.run(host="0.0.0.0", port=port)