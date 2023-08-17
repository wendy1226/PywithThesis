# -*- coding:utf-8 -*-
from asyncio.windows_events import NULL
from distutils.util import execute
from importlib.resources import path
from sqlite3 import Cursor
from mysql.connector import Error
import pymysql
import statistics

db_conn = pymysql.connect(host='127.0.0.1',database='fakenews',user='root',password='1234')
cursor=db_conn.cursor()

for r in range(3249,5069): #第幾則到第幾則
    sql_p= "select sentence_p_value from fakenews.sentence where source_comment_id = '%s' order by sentence_number " % (r)
    sql_h= "select sentence_h_value from fakenews.sentence where source_comment_id = '%s' order by sentence_number " % (r)
    cursor.execute(sql_p)
    p_value=cursor.fetchall() 
    cursor.execute(sql_h)
    h_value=cursor.fetchall() 
    print(len(p_value))
    print(len(h_value))

    #計算機率值，要找正的最大的
    data=[]#存結果
    if len(p_value)>1: #超過一句
        for pp in p_value:
            print(pp[0])
            data.append(pp[0])
        data=statistics.mode(data) #取mode
        data=(f'{data:.4f}') #將浮點數格式化為固定寬度
        print(data) #計算結果
        update="update comment_mode set comment_p_value='%s' where comment_id = '%s'" % (data,r) #max的公式
        cursor.execute(update)
        db_conn.commit()
    else:
        print("只有一句")   
        if p_value != -2:
            update="update comment_mode set comment_p_value= '%s' where comment_id = '%s'" % ( p_value[0][0] , r )  
            cursor.execute(update)
            db_conn.commit()
        else:
            update="update comment_mode set comment_p_value= -2 where comment_id = '%s'" % (r)  
            cursor.execute(update)
            db_conn.commit()

    #計算傷害值
    h_data=[] #存結果
    if len(h_value)>1: #超過一句
        for hh in h_value:
            print(hh[0])
            h_data.append(hh[0])
        h_data=statistics.mode(h_data) #取mode
        h_data=(f'{h_data:.4f}') #將浮點數格式化為固定寬度
        print(h_data) #計算結果
        update="update comment_mode set comment_h_value='%s' where comment_id = '%s'" % (h_data,r) #max的公式
        cursor.execute(update)
        db_conn.commit()
    else:
        print("只有一句")   
        if h_value != -2:
            update="update comment_mode set comment_h_value= '%s' where comment_id = '%s'" % ( h_value[0][0] , r )  
            cursor.execute(update)
            db_conn.commit()
        else:
            update="update comment_mode set comment_h_value= -2 where comment_id = '%s'" % (r)  
            cursor.execute(update)
            db_conn.commit()
cursor.close()