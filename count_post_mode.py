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

for r in range(66,106): #第幾篇到第幾篇
    #case5:c權重高(comment)+p極值，存回post_mode_comment
    sql_p= "select comment_p_value from fakenews.comment where post_id = '%s'" % (r)
    sql_h= "select comment_h_value from fakenews.comment where post_id = '%s'" % (r)
    cursor.execute(sql_p)
    p_value=cursor.fetchall() 
    cursor.execute(sql_h)
    h_value=cursor.fetchall() 

    #計算機率值，要找正的最大的
    data=[]#存結果
    if len(p_value)>1: #超過一則
        for pp in p_value:
            if pp[0] != -2: #有要計算才納入比較[]
                print(pp[0])
                data.append(pp[0])
            else: #此則不計算
                print("不計算")
        if data !=[]:
            data=statistics.mode(data) #取mode
        else:
            data=-2
        data=(f'{data:.4f}') #將浮點數格式化為固定寬度
        print(data) #計算結果
        update="update post_mode_comment set post_p_value='%s' where post_id = '%s'" % (data,r) #max的公式
        cursor.execute(update)
        db_conn.commit()
    else:
        print("只有一則")   
        if p_value != -2:
            update="update post_mode_comment set post_p_value= '%s' where post_id = '%s'" % ( p_value[0][0] , r )  
            cursor.execute(update)
            db_conn.commit()
        else:
            update="update post_mode_comment set post_p_value= -2 where post_id = '%s'" % (r)  
            cursor.execute(update)
            db_conn.commit()

    #計算傷害值
    h_data=[] #存結果
    if len(h_value)>1: #超過一則
        for hh in h_value:
            if hh[0] != -2: #有要計算才納入比較[]
                print(hh[0])
                h_data.append(hh[0])
            else: #此則不計算
                print("不計算")
        if h_data !=[]:
            h_data=statistics.mode(h_data) #取mode
        else:
            h_data=-2
        h_data=(f'{h_data:.4f}') #將浮點數格式化為固定寬度
        print(h_data) #計算結果
        update="update post_mode_comment set post_h_value='%s' where post_id = '%s'" % (h_data,r) #max的公式
        cursor.execute(update)
        db_conn.commit()
    else:
        print("只有一則")   
        if h_value != -2:
            update="update post_mode_comment set post_h_value= '%s' where post_id = '%s'" % ( h_value[0][0] , r )  
            cursor.execute(update)
            db_conn.commit()
        else:
            update="update post_mode_comment set post_h_value= -2 where post_id = '%s'" % (r)  
            cursor.execute(update)
            db_conn.commit()
    #case6:c平均(comment_avg )+p極值，存回post_mode_comment_avg
    sql_p= "select comment_p_value from fakenews.comment_avg where post_id = '%s'" % (r)
    sql_h= "select comment_h_value from fakenews.comment_avg where post_id = '%s'" % (r)
    cursor.execute(sql_p)
    p_value=cursor.fetchall() 
    cursor.execute(sql_h)
    h_value=cursor.fetchall() 

    #計算機率值，要找正的最大的
    avg_data=[]#存結果
    if len(p_value)>1: #超過一則
        for pp in p_value:
            if pp[0] != -2: #有要計算才納入比較[]
                print(pp[0])
                avg_data.append(pp[0])
            else: #此則不計算
                print("不計算")
        if avg_data !=[]:
            avg_data=statistics.mode(avg_data) #取mode
        else:
            avg_data=-2
        avg_data=(f'{avg_data:.4f}') #將浮點數格式化為固定寬度
        print(avg_data) #計算結果
        update="update post_mode_comment_avg set post_p_value='%s' where post_id = '%s'" % (avg_data,r) #max的公式
        cursor.execute(update)
        db_conn.commit()
    else:
        print("只有一則")   
        if p_value != -2:
            update="update post_mode_comment_avg set post_p_value= '%s' where post_id = '%s'" % ( p_value[0][0] , r )  
            cursor.execute(update)
            db_conn.commit()
        else:
            update="update post_mode_comment_avg set post_p_value= -2 where post_id = '%s'" % (r)  
            cursor.execute(update)
            db_conn.commit()

    #計算傷害值
    h_avg_data=[] #存結果
    if len(h_value)>1: #超過一則
        for hh in h_value:
            if hh[0] != -2: #有要計算才納入比較[]
                print(hh[0])
                h_avg_data.append(hh[0])
            else: #此則不計算
                print("不計算")
        if h_avg_data!=[]:
            h_avg_data=statistics.mode(h_avg_data) #取mode
        else:
            h_avg_data=-2    
        h_avg_data=(f'{h_avg_data:.4f}') #將浮點數格式化為固定寬度
        print(h_avg_data) #計算結果
        update="update post_mode_comment_avg set post_h_value='%s' where post_id = '%s'" % (h_avg_data,r) #max的公式
        cursor.execute(update)
        db_conn.commit()
    else:
        print("只有一則")   
        if h_value != -2:
            update="update post_mode_comment_avg set post_h_value= '%s' where post_id = '%s'" % ( h_value[0][0] , r )  
            cursor.execute(update)
            db_conn.commit()
        else:
            update="update post_mode_comment_avg set post_h_value= -2 where post_id = '%s'" % (r)  
            cursor.execute(update)
            db_conn.commit()
            
    #case7:c極值(comment_mode)+p極值，存回post_mode_comment_mode
    sql_p= "select comment_p_value from fakenews.comment_mode where post_id = '%s'" % (r)
    sql_h= "select comment_h_value from fakenews.comment_mode where post_id = '%s'" % (r)
    cursor.execute(sql_p)
    p_value=cursor.fetchall() 
    cursor.execute(sql_h)
    h_value=cursor.fetchall() 

    #計算機率值，要找正的最大的
    max_data_array=[]#存結果
    if len(p_value)>1: #超過一則
        for pp in p_value:
            if pp[0] != -2: #有要計算才納入比較[]
                print(pp[0])
                max_data_array.append(pp[0])
            else: #此則不計算
                print("不計算")
        if len(max_data_array)==0:
            max_data=-2
        else:
            max_data=statistics.mode(max_data_array) #取mode
        max_data=(f'{max_data:.4f}') #將浮點數格式化為固定寬度
        print(max_data) #計算結果
        update="update post_mode_comment_mode set post_p_value='%s' where post_id = '%s'" % (max_data,r) #max的公式
        cursor.execute(update)
        db_conn.commit()
    else:
        print("只有一則")   
        if p_value != -2:
            update="update post_mode_comment_mode set post_p_value= '%s' where post_id = '%s'" % ( p_value[0][0] , r )  
            cursor.execute(update)
            db_conn.commit()
        else:
            update="update post_mode_comment_mode set post_p_value= -2 where post_id = '%s'" % (r)  
            cursor.execute(update)
            db_conn.commit()

    #計算傷害值
    h_max_data_array=[] #存結果
    if len(h_value)>1: #超過一則
        for hh in h_value:
            if hh[0] != -2: #有要計算才納入比較[]
                print(hh[0])
                h_max_data_array.append(hh[0])
            else: #此則不計算
                print("不計算")
        if len(h_max_data_array)==0:
            h_max_data=-2
        else:
            h_max_data=statistics.mode(h_max_data_array) #取mode
        h_max_data=(f'{h_max_data:.4f}') #將浮點數格式化為固定寬度
        print(h_max_data) #計算結果
        update="update post_mode_comment_mode set post_h_value='%s' where post_id = '%s'" % (h_max_data,r) #max的公式
        cursor.execute(update)
        db_conn.commit()
    else:
        print("只有一則")   
        if h_value != -2:
            update="update post_mode_comment_mode set post_h_value= '%s' where post_id = '%s'" % ( h_value[0][0] , r )  
            cursor.execute(update)
            db_conn.commit()
        else:
            update="update post_mode_comment_mode set post_h_value= -2 where post_id = '%s'" % (r)  
            cursor.execute(update)
            db_conn.commit()
cursor.close()