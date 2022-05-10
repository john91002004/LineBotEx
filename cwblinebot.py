# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 14:10:57 2022

@author: USER
"""

# 載入需要的模組
from __future__ import unicode_literals
from unittest.mock import DEFAULT
from flask import Flask, request, abort
import linebot
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
import configparser as conf 
import json 
from json_function import Reply_JsonMessage, debug_log, Reply_TextMessage

# 參數
config = conf.ConfigParser()
config.read("config.ini")
ChannelAccessToken = config.get("john-line-bot-ex", "CHANNEL_ACCESS_TOKEN")
ChannelSecret = config.get("john-line-bot-ex", "CHANNEL_SECRET")

app = Flask(__name__)

# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi(ChannelAccessToken)
handler = WebhookHandler(ChannelSecret)


# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])   # 可以有好多個@app.route，都會回應。
def hahahaha():     # 這個函式必須接在@app.route後面，這是該@app.route路徑專屬的回覆函數，但這個函式的名字不重要，亂取也可以。(用line webhook url verify試驗成功)
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        debug_log('簽名檔驗證失敗，有人正非法嘗試存取您的Line Bot Api！', 'WARNING')
        abort(400)

    return 'OK'


# 收到文字訊息時，回覆訊息
@handler.add(MessageEvent, message=TextMessage)
def TextMessage_Reply(event):
    try:
        message_list = [] 
        debug_log("收到了TextMessage訊息，內容是: " + event.message.text)
        # 決定讀取哪個json 檔案
        if event.message.text == "查看最新一筆衛星資料！":
            json_file = './LatestData/sat_data.json'
        elif event.message.text == "查看主機狀態！":
            json_file = './LatestData/host_status.json'
        elif event.message.text == "查看最新一筆雷達資料！":
            json_file = './LatestData/radar_data.json'
        elif event.message.text == "查看機房狀態！":
            json_file = './LatestData/environment_status.json'
        else: 
            json_file = ''

        # 用line bot api回覆
        if json_file != '':
            message_list = Reply_JsonMessage(json_file=json_file, message_list=message_list)
            line_bot_api.reply_message(event.reply_token, message_list)  
            debug_log('已回覆' + str(min(5, len(message_list))) +'則訊息。')
        else : 
            default_reply = '哩係勒供三小餵啦!?'
            message_list = Reply_TextMessage(default_reply)
            line_bot_api.reply_message(event.reply_token, message_list)  
            debug_log('已回覆 ' + default_reply)

    except linebot.exceptions.LineBotApiError as e:
        debug_log("TextMessage_Reply發生了例外情況，請檢查!", 'ERROR')
        print(e.status_code)
        print(e.request_id)
        print(e.error.message)
        print(e.error.details)



if __name__ == "__main__":
    app.run()
