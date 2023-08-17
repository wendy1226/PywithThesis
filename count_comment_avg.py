# -*- coding:utf-8 -*-
from asyncio.windows_events import NULL
from distutils.util import execute
from importlib.resources import path
from sqlite3 import Cursor
from mysql.connector import Error
import pymysql

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
    #計算機率值
    print(r)
    data=0 #存結果
    total=len(p_value) #存總數量
    if len(p_value)>1: #超過一句
        for pp in p_value:
            if pp[0] != -2:
                print(pp[0])
                data=data+pp[0]
            else: #此句不計算
                print("不計算")
                total=total-1
        if total==0:
            data=-2
        else:
            data=data/total
        data=(f'{data:.4f}') #將浮點數格式化為固定寬度
        print(data) #計算結果
        update="update comment_avg set comment_p_value='%s' where comment_id = '%s'" % (data,r)#avg的公式
        cursor.execute(update)
        db_conn.commit()
    else:
        print("只有一句")
        if p_value != -2:
            update="update comment_avg set comment_p_value= '%s' where comment_id = '%s'" % ( p_value[0][0] , r )  
            cursor.execute(update)
            db_conn.commit()
        else:
            update="update comment_avg set comment_p_value= -2 where comment_id = '%s'" % (r)  
            cursor.execute(update)
            db_conn.commit()
    #計算傷害值
    h_data=0 #存結果
    total_h=len(h_value) #存總數量
    if len(h_value)>1:
        for hh in h_value:
            if hh[0] != -2:
                print(hh[0])
                h_data=h_data+hh[0]
            else: #此句不計算
                print("不計算")
                total_h=total_h-1
        if total_h==0:
            h_data=-2
        else:
            h_data=h_data/total_h
        h_data=(f'{h_data:.4f}') #將浮點數格式化為固定寬度
        print(h_data) #計算結果
        update="update comment_avg set comment_h_value='%s' where comment_id = '%s'" % (h_data,r)#avg的公式
        cursor.execute(update)
        db_conn.commit()
    else:
        print("只有一句")
        if h_value != -2:
            update="update comment_avg set comment_h_value= '%s' where comment_id = '%s'" % (h_value[0][0],r)  
            cursor.execute(update)
            db_conn.commit()
        else:
            update="update comment_avg set comment_h_value= -2 where comment_id = '%s'" % (r)  
            cursor.execute(update)
            db_conn.commit()
    #更新0為-2
    sql_up= "update comment_avg set comment_p_value=-2 where comment_p_value=0 and comment_id ='%s'" % (r)
    sql_uh= "update comment_avg set comment_h_value=-2 where comment_h_value=0 and comment_id ='%s'" % (r)
    cursor.execute(sql_up)
    cursor.execute(sql_uh)
    db_conn.commit()
cursor.close()