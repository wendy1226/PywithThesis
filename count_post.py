# -*- coding:utf-8 -*-
from asyncio.windows_events import NULL
from distutils.util import execute
from importlib.resources import path
from sqlite3 import Cursor
from mysql.connector import Error
import pymysql
db_conn = pymysql.connect(host='127.0.0.1',database='fakenews',user='root',password='1234')
cursor=db_conn.cursor()
for r in range(66,106): #第幾篇到第幾篇
    print(r)
    #case1:c權重高(comment)+p直接平均，存回post_comment
    sql_p= "select comment_p_value from fakenews.comment where post_id = '%s'" % (r)
    sql_h= "select comment_h_value from fakenews.comment where post_id = '%s'" % (r)
    cursor.execute(sql_p)
    p_value=cursor.fetchall() 
    cursor.execute(sql_h)
    h_value=cursor.fetchall() 
    #計算機率值(直接平均)
    data=0 #存結果
    total=len(p_value) #存總數量
    if len(p_value)>1: #超過一則
        i=0
        for pp in p_value:
            if pp[0] != -2:
                print(pp[0])
                data=data+pp[0]
            else: #此則不計算
                print("不計算")
                total=total-1
            i=i+1
        if total==0:
            data=-2
        else:
            data=data/total
        data=(f'{data:.4f}') #將浮點數格式化為固定寬度
        print(data) #計算結果
        update="update post_comment set post_p_value='%s' where post_id = '%s'" % (data,r)
        cursor.execute(update)
        db_conn.commit()
    else:
        print("只有一則")
        if p_value != -2:
            update="update post_comment set post_p_value= '%s' where post_id = '%s'" % ( p_value[0][0] , r )  
            cursor.execute(update)
            db_conn.commit()
        else:
            update="update post_comment set post_p_value= -2 where post_id = '%s'" % (r)  
            cursor.execute(update)
            db_conn.commit()
    #計算傷害值
    h_data=0 #存結果
    total_h=len(h_value) #存總數量
    if len(h_value)>1:
        i=0
        for hh in h_value:
            if hh[0] != -2:
                print(hh[0])
                h_data=h_data+hh[0]
            else: #此句不計算
                print("不計算")
                total_h=total_h-1
            i=i+1
        if total_h==0:
            h_data=-2
        else:
            h_data=h_data/total_h
        h_data=(f'{h_data:.4f}') #將浮點數格式化為固定寬度
        print(h_data) #計算結果
        update="update post_comment set post_h_value='%s' where post_id = '%s'" % (h_data,r)
        cursor.execute(update)
        db_conn.commit()
    else:
        print("只有一句")
        if h_value != -2:
            update="update post_comment set post_h_value= '%s' where post_id = '%s'" % (h_value[0][0],r)  
            cursor.execute(update)
            db_conn.commit()
        else:
            update="update post_comment set post_h_value= -2 where post_id = '%s'" % (r)  
            cursor.execute(update)
            db_conn.commit()
            
    #case2:c平均(comment_avg)+p直接平均，存回post_comment_avg
    sql_p= "select comment_p_value from fakenews.comment_avg where post_id = '%s'" % (r)
    sql_h= "select comment_h_value from fakenews.comment_avg where post_id = '%s'" % (r)
    cursor.execute(sql_p)
    p_value=cursor.fetchall() 
    cursor.execute(sql_h)
    h_value=cursor.fetchall() 
    #計算機率值(直接平均)
    data=0
    total=len(p_value) #存總數量
    if len(p_value)>1: #超過一則
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
        update="update post_comment_avg set post_p_value='%s' where post_id = '%s'" % (data,r)
        cursor.execute(update)
        db_conn.commit()
    else:
        print("只有一則")
        if p_value != -2:
            update="update post_comment_avg set post_p_value= '%s' where post_id = '%s'" % ( p_value[0][0] , r )  
            cursor.execute(update)
            db_conn.commit()
        else:
            update="update post_comment_avg set post_p_value= -2 where post_id = '%s'" % (r)  
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
        update="update post_comment_avg set post_h_value='%s' where post_id = '%s'" % (h_data,r)
        cursor.execute(update)
        db_conn.commit()
    else:
        print("只有一句")
        if h_value != -2:
            update="update post_comment_avg set post_h_value= '%s' where post_id = '%s'" % (h_value[0][0],r)  
            cursor.execute(update)
            db_conn.commit()
        else:
            update="update post_comment_avg set post_h_value= -2 where post_id = '%s'" % (r)  
            cursor.execute(update)
            db_conn.commit()
    #newcase3:c極值(comment_mode)+p直接平均，存回post_comment_mode
    sql_p= "select comment_p_value from fakenews.comment_mode where post_id = '%s'" % (r)
    sql_h= "select comment_h_value from fakenews.comment_mode where post_id = '%s'" % (r)
    cursor.execute(sql_p)
    p_value=cursor.fetchall() 
    cursor.execute(sql_h)
    h_value=cursor.fetchall() 
    #計算機率值(直接平均)
    data=0
    total=len(p_value) #存總數量
    if len(p_value)>1: #超過一則
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
        update="update post_comment_mode set post_p_value='%s' where post_id = '%s'" % (data,r)
        cursor.execute(update)
        db_conn.commit()
    else:
        print("只有一則")
        if p_value != -2:
            update="update post_comment_mode set post_p_value= '%s' where post_id = '%s'" % ( p_value[0][0] , r )  
            cursor.execute(update)
            db_conn.commit()
        else:
            update="update post_comment_mode set post_p_value= -2 where post_id = '%s'" % (r)  
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
        update="update post_comment_mode set post_h_value='%s' where post_id = '%s'" % (h_data,r)
        cursor.execute(update)
        db_conn.commit()
    else:
        print("只有一句")
        if h_value != -2:
            update="update post_comment_mode set post_h_value= '%s' where post_id = '%s'" % (h_value[0][0],r)  
            cursor.execute(update)
            db_conn.commit()
        else:
            update="update post_comment_mode set post_h_value= -2 where post_id = '%s'" % (r)  
            cursor.execute(update)
            db_conn.commit()
cursor.close()