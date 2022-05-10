# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 14:42:21 2022

@author: USER
"""
import os, json
import configparser as conf 
from linebot import LineBotApi
from json_function import debug_log, load_json

# 參數
config = conf.ConfigParser()
config.read("config.ini")
ChannelAccessToken = config.get("john-line-bot-ex", "CHANNEL_ACCESS_TOKEN")
ChannelSecret = config.get("john-line-bot-ex", "CHANNEL_SECRET")

rich_menu_folder = config.get('path-param', 'RICH_MENU_FOLDER') 
rich_menu_list_file = config.get('path-param', 'RICH_MENU_LIST') 

# 進入我們的Line Bot API去查看rich menu list
line_bot_api = LineBotApi(ChannelAccessToken)
rich_menu_list = line_bot_api.get_rich_menu_list()

# 讀取本地rich_menu_list檔案
json_list = load_json(json_file=rich_menu_list_file)

# 刪除先前所有的richmenu
debug_log('刪除先前所有的rich menu:')
for rich_menu in rich_menu_list:
    debug_log("Delete rich menu -> " + (rich_menu.rich_menu_id))
    line_bot_api.delete_rich_menu(rich_menu.rich_menu_id) 
    # 找出本地json的相對應key, value 並刪除
    tmp_key_list = []
    for k,v in json_list.items() : 
        if v['id'] == rich_menu.rich_menu_id : 
            tmp_key_list.append(k)
    for k in tmp_key_list : 
        json_list.pop(k)

debug_log('更新 ' + os.path.basename(rich_menu_list_file) + ' ...') 
with open(file=rich_menu_list_file, mode='w') as fw: 
    fw.write(json.dumps(json_list))

