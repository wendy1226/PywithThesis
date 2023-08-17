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
from ckiptagger import WS, POS, NER
import pandas as pd
import time
import numpy as np
import string
#path
ws = WS("C:/Users/acer/AppData/Local/Programs/Python/Python39/Lib/site-packages/ckiptagger/data") #斷詞


db_conn = pymysql.connect(host='127.0.0.1',database='fakenews',user='root',password='1234')
cursor=db_conn.cursor()


for r in range(3249,5069): #第幾則到第幾則(-1) 
    sql= "select sentence_id,sentence_content from fakenews.sentence where source_comment_id = '%s'" % (r)
    cursor.execute(sql)
    sentence_list=cursor.fetchall() 
    for c in sentence_list:
        segword_list=[]
        print(c) 
        seg_word = ws(
        [c[1]],
        # sentence_segmentation = True, # To consider delimiters 分隔符號
        # segment_delimiter_set = ({",", "。", ":", "?", "!", ";", "[", "]", "'"}),
        )
        #問號
        #判斷是否為標點符號
        punc=string.punctuation
        for word_list in seg_word:
            for word in word_list:
                if word not in punc:
                    segword_list.append(word)
                else:
                    print("{} 是標點符號".format(word))
        tupseg_word=tuple(segword_list) 

        for i in tupseg_word:
            sql = "SELECT 1 FROM fakenews.corpus_a where word='%s' limit 1" % (i)
            cursor.execute(sql)
            data=cursor.fetchall() #比對資料庫
            if len(data) == 0:
                # print("not exist")#詞庫不存在，則insert
                word=i
                tup=(word,None,None) 
                insert="insert into corpus_a(word,corpus,manual_check) values(%s,%s,%s)"
                cursor.execute(insert,tup)
                db_conn.commit()
                sql1 = "SELECT word_id FROM fakenews.corpus_a where word='%s' limit 1" % (i)
                cursor.execute(sql1)
                wordid=cursor.fetchall() #比對資料庫
                tup=(wordid[0][0],i,c[0],None,None) 
                #插入index
                insert="insert into fakenews.index(word_id ,word, sentence_id,sentence_p_check, sentence_h_check) values(%s,%s,%s,%s,%s)"
                cursor.execute(insert,tup)
                db_conn.commit()
            else:
                # print("exist")#詞庫存在
                #插入到index
                sql1 = "SELECT word_id FROM fakenews.corpus_a where word='%s' limit 1" % (i)
                cursor.execute(sql1)
                wordid=cursor.fetchall() #比對資料庫
                tup=(wordid[0][0],i,c[0],None,None) 
                #插入index
                insert="insert into fakenews.index(word_id ,word, sentence_id,sentence_p_check, sentence_h_check) values(%s,%s,%s,%s,%s)"
                cursor.execute(insert,tup)
                db_conn.commit()
cursor.close()