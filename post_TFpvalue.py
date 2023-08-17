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
    #計算真假人數(comment)
    sql= "select comment_p_value from fakenews.comment where post_id = '%s'" % (r)  
    cursor.execute(sql)
    p_count=cursor.fetchall()  
    count_false_1 = 0
    count_true_1 = 0
    for p in p_count:
        if p[0] >0:
            count_false_1=count_false_1+1 #機率值>0則認為是假的
        elif p[0] >=-1 and p[0] <0 :
            count_true_1=count_true_1+1 #機率值<=0則認為是真的
        else:
            print("不計算")

    sql_p= "select comment_p_value from fakenews.comment where post_id = '%s'" % (r)
    cursor.execute(sql_p)
    p_value=cursor.fetchall() 
    #計算機率值(人數平均)
    #存結果
    data_f=0 
    data_t=0
    t_mode_data=[]#存結果
    f_mode_data=[]#存結果
    for pp in p_value:
        if pp[0] != -2:
            if pp[0] >0: #假 
                data_f=data_f+pp[0]
                f_mode_data.append(pp[0])
            else: #真
                data_t=data_t+pp[0]
                t_mode_data.append(pp[0])
        else: #此句不計算
            print("不計算")
    #false的機率
    if count_false_1 !=0: #人數!=0
        f_pvalue=data_f/count_false_1
        f_mode_data=statistics.mode(f_mode_data) #取max
    else:
        f_pvalue=-2
        f_mode_data=-2
    #true的機率
    if count_true_1 !=0: #人數!=0
        t_pvalue=data_t/count_true_1
        t_mode_data=statistics.mode(t_mode_data) #取max
    else:
        t_pvalue=-2
        t_mode_data=-2
    f_pvalue=(f'{f_pvalue:.4f}') #將浮點數格式化為固定寬度
    t_pvalue=(f'{t_pvalue:.4f}') #將浮點數格式化為固定寬度  
    f_mode_data=(f'{f_mode_data:.4f}') #將浮點數格式化為固定寬度
    t_mode_data=(f'{t_mode_data:.4f}') #將浮點數格式化為固定寬度
    update_1 = "update post_comment set t_pvalue= '%s' ,f_pvalue= '%s' where post_id = '%s'" % (t_pvalue,f_pvalue,r)  
    update_2 = "update post_avg_comment set t_pvalue= '%s' ,f_pvalue= '%s' where post_id = '%s'" % (t_pvalue,f_pvalue,r) 
    update_3 = "update post_mode_comment set t_pvalue= '%s' ,f_pvalue= '%s' where post_id = '%s'" % (t_mode_data,f_mode_data,r) 
    cursor.execute(update_1)
    cursor.execute(update_2)
    cursor.execute(update_3)
    db_conn.commit()

    #計算真假人數(comment_avg)
    sql= "select comment_p_value from fakenews.comment_avg where post_id = '%s'" % (r)  
    cursor.execute(sql)
    p_count=cursor.fetchall()  
    count_false_2 = 0
    count_true_2 = 0
    for p in p_count:
        if p[0] >0:
            count_false_2=count_false_2+1 #機率值>0則認為是假的
        elif p[0] >=-1 and p[0] <0 :
            count_true_2=count_true_2+1 #機率值<=0則認為是真的
        else:
            print("不計算")

    sql_p= "select comment_p_value from fakenews.comment_avg where post_id = '%s'" % (r)
    cursor.execute(sql_p)
    p_value=cursor.fetchall() 
    #計算機率值(人數平均)
    #存結果
    data_f=0 
    data_t=0
    t_max_data=[]#存結果
    f_max_data=[]#存結果
    for pp in p_value:
        if pp[0] != -2:
            if pp[0] >0: #假 
                data_f=data_f+pp[0]
                f_max_data.append(pp[0])
            else: #真
                data_t=data_t+pp[0]
                t_max_data.append(pp[0])
        else: #此句不計算
            print("不計算")
    #false的機率
    if count_false_2 !=0: #人數!=0
        f_pvalue=data_f/count_false_2
        f_max_data=max(f_max_data) #取max
    else:
        f_pvalue=-2
        f_max_data=-2
    #true的機率
    if count_true_2 !=0: #人數!=0
        t_pvalue=data_t/count_true_2
        t_max_data=max(t_max_data) #取max
    else:
        t_pvalue=-2
        t_max_data=-2
    f_pvalue=(f'{f_pvalue:.4f}') #將浮點數格式化為固定寬度
    t_pvalue=(f'{t_pvalue:.4f}') #將浮點數格式化為固定寬度  
    f_max_data=(f'{f_max_data:.4f}') #將浮點數格式化為固定寬度
    t_max_data=(f'{t_max_data:.4f}') #將浮點數格式化為固定寬度
    update_1 = "update post_comment_avg set t_pvalue= '%s' ,f_pvalue= '%s' where post_id = '%s'" % (t_pvalue,f_pvalue,r)  
    update_2 = "update post_avg_comment_avg set t_pvalue= '%s' ,f_pvalue= '%s' where post_id = '%s'" % (t_pvalue,f_pvalue,r) 
    update_3 = "update post_mode_comment_avg set t_pvalue= '%s' ,f_pvalue= '%s' where post_id = '%s'" % (t_max_data,f_max_data,r) 
    cursor.execute(update_1)
    cursor.execute(update_2)
    cursor.execute(update_3)
    db_conn.commit()

    #計算真假人數(comment_max)
    sql= "select comment_p_value from fakenews.comment_mode where post_id = '%s'" % (r)  
    cursor.execute(sql)
    p_count=cursor.fetchall()  
    count_false_3 = 0
    count_true_3 = 0
    for p in p_count:
        if p[0] >0:
            count_false_3=count_false_3+1 #機率值>0則認為是假的
        elif p[0] >=-1 and p[0] <0 :
            count_true_3=count_true_3+1 #機率值<=0則認為是真的
        else:
            print("不計算")

    sql_p= "select comment_p_value from fakenews.comment_mode where post_id = '%s'" % (r)
    cursor.execute(sql_p)
    p_value=cursor.fetchall() 
    #計算機率值(人數平均)
    #存結果
    data_f=0 
    data_t=0
    t_max_data=[]#存結果
    f_max_data=[]#存結果
    for pp in p_value:
        if pp[0] != -2:
            if pp[0] >0: #假 
                data_f=data_f+pp[0]
                f_max_data.append(pp[0])
            else: #真
                data_t=data_t+pp[0]
                t_max_data.append(pp[0])
        else: #此句不計算
            print("不計算")
    #false的機率
    if count_false_3 !=0: #人數!=0
        f_pvalue=data_f/count_false_3
        f_max_data=max(f_max_data) #取max
    else:
        f_pvalue=-2
        f_max_data=-2
    #true的機率
    if count_true_3 !=0: #人數!=0
        t_pvalue=data_t/count_true_3
        t_max_data=max(t_max_data) #取max
    else:
        t_pvalue=-2
        t_max_data=-2
    f_pvalue=(f'{f_pvalue:.4f}') #將浮點數格式化為固定寬度
    t_pvalue=(f'{t_pvalue:.4f}') #將浮點數格式化為固定寬度  
    f_max_data=(f'{f_max_data:.4f}') #將浮點數格式化為固定寬度
    t_max_data=(f'{t_max_data:.4f}') #將浮點數格式化為固定寬度
    update_1 = "update post_comment_mode set t_pvalue= '%s' ,f_pvalue= '%s' where post_id = '%s'" % (t_pvalue,f_pvalue,r)  
    update_2 = "update post_avg_comment_mode set t_pvalue= '%s' ,f_pvalue= '%s' where post_id = '%s'" % (t_pvalue,f_pvalue,r) 
    update_3 = "update post_mode_comment_mode set t_pvalue= '%s' ,f_pvalue= '%s' where post_id = '%s'" % (t_max_data,f_max_data,r) 
    cursor.execute(update_1)
    cursor.execute(update_2)
    cursor.execute(update_3)
    db_conn.commit()
cursor.close()