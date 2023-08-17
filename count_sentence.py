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

for i in range(7921,12732): #第幾句到第幾句
    sql_1= "select h_value from fakenews.corpus_b where word_id in (select word_id from fakenews.index where sentence_id ='%s')" % (i)
    sql_2= "select p_value from fakenews.corpus_c where word_id in (select word_id from fakenews.index where sentence_id ='%s')" % (i)
    cursor.execute(sql_1)
    db_conn.commit()
    h_data=cursor.fetchall()
    cursor.execute(sql_2)
    db_conn.commit()
    p_data=cursor.fetchall()
    print(h_data,p_data)
    if len(h_data) != 0: #有關聯詞
        h=[]
        h.append(h_data)
        h_data=max(h_data)
        print(h_data)
        for h in h_data:
            if len(p_data) != 0: #有機率詞，則計算
                for p in p_data:
                    # 將corpus_b中的word給定值=1，與corpus_c中的word其p_value相乘，得出sentence_p_value
                    sentence_p_value = p[0]*1
                    # 將corpus_b中的word其h_value與corpus_c中的word其p_value相乘，得出sentence_h_value
                    sentence_h_value = p[0]*h
                    #sentence_p_value存回sentence表
                    sql_p = "update sentence set sentence_p_value= '%s' where sentence_id = '%s' " % (sentence_p_value,i)
                    cursor.execute(sql_p)
                    db_conn.commit()
                    #sentence_h_value存回sentence表
                    if sentence_h_value<0:
                        sql_h = "update sentence set sentence_h_value= -2 where sentence_id = '%s' " % (i)
                        cursor.execute(sql_h)
                        db_conn.commit()
                    else:
                        sql_h = "update sentence set sentence_h_value= '%s' where sentence_id = '%s' " % (sentence_h_value,i)
                        cursor.execute(sql_h)
                        db_conn.commit()
            else:
                print("沒有機率詞!")
                sql_3 = "update sentence set sentence_p_value=1 , sentence_h_value='%s' where sentence_id = '%s'" % (h,i)
                cursor.execute(sql_3)        
                db_conn.commit()
    else:
        print("沒有關聯詞或機率詞!")
        #只要沒有關聯詞就不計算，更新為-2
        sql_4 = "update sentence set sentence_p_value=-2 , sentence_h_value=-2 where sentence_id = '%s' " % (i)
        cursor.execute(sql_4)
        db_conn.commit()
    #更新index的sentence_p_check&sentence_h_check 
    sql_5 = "update fakenews.index set sentence_p_check=1 , sentence_h_check=1 where sentence_id = '%s'" % (i)
    cursor.execute(sql_5)
    db_conn.commit()

cursor.close()