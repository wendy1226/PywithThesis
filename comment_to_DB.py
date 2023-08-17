#import套件
from asyncio.windows_events import NULL
from csv import reader
from distutils.util import execute
from importlib.resources import path
from sqlite3 import Cursor
from mysql.connector import Error
# -*- coding:utf-8 -*-
import pandas as pd
import csv
import pymysql

count=0

db_conn = pymysql.connect(host='127.0.0.1',database='fakenews',user='root',password='1234')
cursor=db_conn.cursor()
#打開csv
with open('./post105.csv',newline='',encoding="utf-8-sig") as csvfile:
    rows = csv.reader(csvfile)
    print(rows)
    new_list=[]
    for i in rows:
        number=i[0] 
        content=i[1]
        count=count+1
        tup=(number,content,None,None,None,None,None,105)#post_id
        new_list.append(tup)
    #留言數量
    update="update fakenews.post_comment set comment_count='%s' where post_id =105 " % (count) #post_id
    cursor.execute(update)
    db_conn.commit()
    #存入comment table
    insert="insert into comment(comment_number,comment_content,sentence_count,comment_p_value,comment_h_value,count_false,count_true,post_id) values(%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.executemany(insert, new_list)
    db_conn.commit()
cursor.close()