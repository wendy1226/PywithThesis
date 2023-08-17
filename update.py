#import套件
# -*- coding:utf-8 -*-
from asyncio.windows_events import NULL
from csv import reader
from distutils.util import execute
from importlib.resources import path
from sqlite3 import Cursor
from mysql.connector import Error
import pymysql

db_conn = pymysql.connect(host='127.0.0.1',database='fakenews',user='root',password='1234')
cursor=db_conn.cursor()
#corpus_a label完後執行
#修改從多少到多少
#人工檢視完畢後，更新狀態7975
sql_1= "UPDATE corpus_a SET corpus='a' WHERE corpus is null and word_id BETWEEN 7976 AND 10794"
sql_2= "UPDATE corpus_a SET manual_check='1' WHERE word_id BETWEEN 7976 AND 10794 " 
cursor.execute(sql_1)
db_conn.commit()
cursor.execute(sql_2)
db_conn.commit()
#詞庫移動
sql_3= "insert into fakenews.corpus_b(word_id,word) select corpus_a.word_id as word_id ,corpus_a.word as word from corpus_a where corpus='b' and word_id BETWEEN 7976 AND 10794" 
sql_4= "insert into fakenews.corpus_c(word_id,word) select corpus_a.word_id as word_id ,corpus_a.word as word from corpus_a where corpus='c' and word_id BETWEEN 7976 AND 10794" 
cursor.execute(sql_3)
db_conn.commit()
cursor.execute(sql_4)
db_conn.commit()

cursor.close()