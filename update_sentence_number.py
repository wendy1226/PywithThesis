# -*- coding:utf-8 -*-
import re
from asyncio.windows_events import NULL
from csv import reader
from distutils.util import execute
from importlib.resources import path
from sqlite3 import Cursor
from mysql.connector import Error
import pymysql

new_list=[]
count=0

db_conn = pymysql.connect(host='127.0.0.1',database='fakenews',user='root',password='1234')
cursor=db_conn.cursor()

for r in range(3249,5069) : #第幾則到第幾則
    sql= "select sentence_id from fakenews.sentence where source_comment_id ='%s'" % (r)
    cursor.execute(sql)
    sentence=cursor.fetchall() 
    # print(sentence)
    # print(len(sentence))
    update="update fakenews.comment set sentence_count='%s' where comment_id ='%s' " % (len(sentence),r)
    cursor.execute(update)
    db_conn.commit()
    for i in sentence:
        count=count+1
        # print("sentence_id=",i[0])
        # print("sentence_number=",count)
        update="update fakenews.sentence set sentence_number='%s' where sentence_id='%s' " % (count,i[0])
        cursor.execute(update)
        db_conn.commit()
    count=0    
cursor.close()