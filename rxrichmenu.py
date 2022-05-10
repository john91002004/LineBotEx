# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 14:42:21 2022

@author: USER
"""
from distutils.log import debug
import os 
import requests
import json
import configparser as conf 
from linebot import LineBotApi
from json_function import load_json, debug_log

# 參數
config = conf.ConfigParser()
config.read("config.ini")
ChannelAccessToken = config.get("john-line-bot-ex", "CHANNEL_ACCESS_TOKEN")
ChannelSecret = config.get("john-line-bot-ex", "CHANNEL_SECRET")

rich_menu_folder = config.get('path-param', 'RICH_MENU_FOLDER') 
rich_menu_list_file = config.get('path-param', 'RICH_MENU_LIST') 

json_file = 'rxrichmenu.json'
richmenu_title = json_file.split('.')[0]
pic_file = richmenu_title + '.jpg'
richmenu_json = rich_menu_folder + json_file
richmenu_pic = rich_menu_folder + pic_file

# 檢查是否已經上傳過了
rich_menu_list = load_json(json_file=rich_menu_list_file)
if rich_menu_list.get(richmenu_title) != None : 
    debug_log('該檔案已經上傳過了哦！請更名或刪除雲端的RichMenu！', 'WARN') 
elif os.path.isfile(richmenu_pic) == False : 
    debug_log(f'沒有找到 {richmenu_pic} 圖片檔哦！', 'WARN')
else : 
# 製作richmenu的請求，這個請求由header 和 body 組成
    headers = {"Authorization":"Bearer " + ChannelAccessToken,"Content-Type":"application/json"}
    body = load_json(richmenu_json) 

    # 發出請求
    debug_log('正在發出請求...')
    req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu', 
                        headers=headers,data=json.dumps(body).encode('utf-8'))
    richmenu_id = json.loads(req.text) ["richMenuId"] 
    debug_log("New rich menu id -> " + str(richmenu_id)) # 傳回{"richMenuId": "......"} richmenu的ID

    # 設定rich menu的圖片
    line_bot_api = LineBotApi(ChannelAccessToken)
    with open(richmenu_pic, 'rb') as f:
        line_bot_api.set_rich_menu_image(richmenu_id, "image/jpeg", f)

    # 啟用rich menu
    debug_log('正在將 ' + richmenu_title + ' 設為預設rich menu...')
    line_bot_api.set_default_rich_menu(richmenu_id)

    # 將設定存回rich_menu_list 
    debug_log('更新 ' + json_file + ' ...')
    with open(file=rich_menu_list_file) as fr : 
        tmp_json = fr.read() 
    tmp_dict = json.loads(tmp_json)
    tmp_dict[richmenu_title] = { 'id': richmenu_id, 'pic': pic_file, 'json': json_file} 
    tmp_json = json.dumps(tmp_dict)
    with open(file=rich_menu_list_file, mode='w') as fa: 
        fa.write(tmp_json)


