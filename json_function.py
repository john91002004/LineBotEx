# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 14:10:57 2022

@author: USER
"""

# 載入需要的模組
from __future__ import unicode_literals
from linebot.models import TextSendMessage, ImageSendMessage
import json, os

# 回傳一個dict
def load_json (json_file):  
    if os.path.isfile(json_file) == False :
        debug_log(json_file + ' is not a file.') 
        return ''
    try: 
        with open(file=json_file, encoding='utf-8') as fr : 
            json_data = fr.read() 
        return json.loads(json_data)
    except Exception as e : 
        debug_log("load_json發生了例外情況，請檢查!", 'ERROR')
        exception_log(e)

def Reply_TextMessage(text_list=[]):
    if len(text_list) == 0 : 
        debug_log('空的文字訊息', 'WARN')
    elif type(text_list) != list : 
        if type(text_list) != str: 
            debug_log('錯誤的文字訊息格式', 'WRAN')
        else : 
            text_list = [text_list]

    message_list = [TextSendMessage(text=text_list[i]) for i in range(0,len(text_list))] 
    return message_list[0:5]    # 因為一次最多只能回覆5則訊息

def Reply_JsonMessage(json_file, message_list=[]) : 
    mes = load_json(json_file=json_file)
    if mes != '':
        for key in mes.keys() : 
            if key == "TextMessage": 
                message_list.append(TextSendMessage(text=mes[key]))
            elif key == "ImageMessage": 
                message_list.append (
                    ImageSendMessage(
                        original_content_url=mes[key],
                        preview_image_url=mes[key])
                )
        return message_list[0:5]    # 因為一次最多只能回覆5則訊息

def debug_log(text="", type="INFO") : 
    log_text = '[' + type + '] ' + text 
    print(log_text)

def exception_log(e): 
    for i in range(0,len(e.args)) : 
        debug_log(text=e.args[i], type='EXCEPTION_INFO') 

