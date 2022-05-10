# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 11:23:42 2022

這是用來喚醒我們的APP用的，因為是免費方案，所以會20分鐘沒有使用就會睡覺。

@author: USER
"""

# 一定要寫urllib.request，不能只寫urllib，要不然會因為python版本原因報錯
import urllib.request
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime 

# 排程工具
sched = BlockingScheduler()
Period = 30 
PeriodFormat = '*/' + str(Period)  # 用的是cron的形式 

@sched.scheduled_job('cron', day_of_week='mon-fri', minute=PeriodFormat)
def scheduled_job():
    print('========== APScheduler CRON START =========')
    print('This job runs every day 'f'{Period} min.')
    print(f'{datetime.now().ctime()}')
    print('========== PRINT TARGET URL CONTENT =========')
    url = "https://johnlinebotex.herokuapp.com/"
    conn = urllib.request.urlopen(url)
        
    for key, value in conn.getheaders():
        print(key, value)
        
    print('========== APScheduler CRON END =========')

sched.start()

