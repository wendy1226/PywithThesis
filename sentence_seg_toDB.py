# -*- coding:utf-8 -*-
import re
from asyncio.windows_events import NULL
from csv import reader
from distutils.util import execute
from importlib.resources import path
from sqlite3 import Cursor
from mysql.connector import Error
import pandas as pd
import pymysql
import csv

new_list=[]
count=0

db_conn = pymysql.connect(host='127.0.0.1',database='fakenews',user='root',password='1234')
cursor=db_conn.cursor()

def cut_sentences(content):
	sentences = re.split(r'\.|\!|\?|。|！|，|？|\.{6}', content)
	return sentences

sql= "select comment_id,comment_content from fakenews.comment where post_id = 105"
cursor.execute(sql)
comment=cursor.fetchall() 
print(comment)
for c in comment:
    print(c) 
    sentences = cut_sentences(c[1])
    print(c[0])
    print(sentences)
    for i in sentences:
        s=[i]
        count=count+1
        tup=(count,s,None,None,c[0])
        d=[count,s,c[0]]
        new_list.append(tup)
    update="update fakenews.comment set sentence_count='%s' where comment_id ='%s' " % (count,c[0])
    cursor.execute(update)
    db_conn.commit()
    count=0 

insert="insert into sentence(sentence_number,sentence_content,sentence_p_value,sentence_h_value,source_comment_id) values(%s,%s,%s,%s,%s)"
cursor.executemany(insert, new_list)
db_conn.commit()

cursor.close()