#import套件
from asyncio.windows_events import NULL
from csv import reader
from distutils.util import execute
from importlib.resources import path
from sqlite3 import Cursor
import mysql.connector 
from mysql.connector import Error
# -*- coding:utf-8 -*-
import pandas as pd
import os
import csv
import time
import pymysql

db_conn = pymysql.connect(host='127.0.0.1',database='fakenews',user='root',password='1234')
cursor=db_conn.cursor()

with open('./rumor.csv',newline='',encoding="utf-8") as csvfile:
    rows = csv.reader(csvfile)
    new_list=[]
    for i in rows:
        date=i[0]
        content=i[1]
        tup=(date,content,None,None,None,None,None)
        new_list.append(tup)
    insert="insert into post_comment(post_date,post_content,post_p_value,post_h_value,count_false,count_true,comment_count) values(%s,%s,%s,%s,%s,%s,%s)"
    cursor.executemany(insert, new_list)
    db_conn.commit()
cursor.close()


# try:
#     # 連接 MySQL/MariaDB 資料庫
#     connection = mysql.connector.connect(
#         host='127.0.0.1',          # 主機名稱
#         database='fakenews', # 資料庫名稱
#         user='root',        # 帳號
#         password='1234')  # 密碼

#     # 更新資料
#     sql = "INSERT INTO post (post_date,post_content,post_p_value,post_h_value,count_false,count_true,comment_count) VALUES (%s,%s,%s,%s,%s,%s,%s);"
#     new_data = ("2023/1/1", "內容",NULL,NULL,NULL,NULL,NULL)
#     cursor = connection.cursor()
#     cursor.execute(sql, new_data)

#     # 確認資料有存入資料庫
#     connection.commit()

# except Error as e:
#     print("資料庫連接失敗：", e)

# finally:
#     if (connection.is_connected()):
#         cursor.close()
#         connection.close()
