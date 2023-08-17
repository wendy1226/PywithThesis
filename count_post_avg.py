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
    #計算真假人數(comment)
    sql= "select comment_p_value from fakenews.comment where post_id = '%s'" % (r)  
    cursor.execute(sql)
    p_count=cursor.fetchall()  
    print(p_count)
    count_false_1 = 0
    count_true_1 = 0
    for p in p_count:
        if p[0] >0:
            count_false_1=count_false_1+1 #機率值>0則認為是假的
        elif p[0] >=-1 and p[0] <0 :
            count_true_1=count_true_1+1 #機率值<=0則認為是真的
        else:
            print("不計算")
    #count_false&count_true存回comment表
    update_1 = "update post_comment set count_false= '%s' ,count_true= '%s' where post_id = '%s'" % (count_false_1,count_true_1,r)  
    update_2 = "update post_avg_comment set count_false= '%s' ,count_true= '%s' where post_id = '%s'" % (count_false_1,count_true_1,r) 
    update_3 = "update post_mode_comment set count_false= '%s' ,count_true= '%s' where post_id = '%s'" % (count_false_1,count_true_1,r) 
    cursor.execute(update_1)
    cursor.execute(update_2)
    cursor.execute(update_3)
    db_conn.commit()

    #case3:c權重高(comment)+p人數平均，存回post_avg_comment
    sql_p= "select comment_p_value from fakenews.comment where post_id = '%s'" % (r)
    sql_h= "select comment_h_value from fakenews.comment where post_id = '%s'" % (r)
    cursor.execute(sql_p)
    p_value=cursor.fetchall() 
    cursor.execute(sql_h)
    h_value=cursor.fetchall() 
    #計算機率值(人數平均)
    #存結果
    data=0
    data_f=0 
    data_t=0
    if len(p_value)>1: #超過一則
        for pp in p_value:
            if pp[0] != -2:
                if pp[0] >0: #假 
                    data_f=data_f+pp[0]
                else: #真
                    data_t=data_t+pp[0]
            else: #此句不計算
                print("不計算")
        if count_true_1 !=0 and count_false_1!=0: #人數皆不為0
            data=(data_f/count_false_1+data_t/count_true_1)/2
        elif count_false_1 ==0 and count_true_1!=0: #假的人數0&真的人數不為0
            data=(data_t/count_true_1)/2
        elif count_true_1 ==0 and count_false_1!=0: #真的人數0&假的人數不為0
            data=(data_f/count_false_1)/2
        else: #人數皆為0
            print("人數皆為0")
        data=(f'{data:.4f}') #將浮點數格式化為固定寬度
        print(data) #計算結果
        update="update post_avg_comment set post_p_value='%s' where post_id = '%s'" % (data,r)
        cursor.execute(update)
        db_conn.commit()
    else:
        print("只有一則")
        if p_value != -2:
            update="update post_avg_comment set post_p_value= '%s' where post_id = '%s'" % ( p_value[0][0] , r )  
            cursor.execute(update)
            db_conn.commit()
        else:
            update="update post_avg_comment set post_p_value= -2 where post_id = '%s'" % (r)  
            cursor.execute(update)
            db_conn.commit()
    #計算傷害值
    #存結果
    h_data=0
    h_data_f=0 
    h_data_t=0
    if len(h_value)>1:
        for hh in h_value:
            if hh[0] != -2:
                print(hh[0])
                if hh[0] >0: #假 
                    h_data_f=h_data_f+hh[0]
                else: #真
                    h_data_t=h_data_t+hh[0]
            else: #此句不計算
                print("不計算")
        if count_true_1 !=0 and count_false_1!=0:
            h_data=(h_data_f/count_false_1+h_data_t/count_true_1)/2
        elif count_false_1 ==0 and count_true_1!=0:
            h_data=(h_data_t/count_true_1)/2
        elif count_true_1 ==0 and count_false_1!=0:
            h_data=(h_data_f/count_false_1)/2
        else:
            print("人數皆為0")
        h_data=(f'{h_data:.4f}') #將浮點數格式化為固定寬度
        print(h_data) #計算結果
        update="update post_avg_comment set post_h_value='%s' where post_id = '%s'" % (h_data,r)
        cursor.execute(update)
        db_conn.commit()
        print("failed")
    else:
        print("只有一句")
        if h_value != -2:
            update="update post_avg_comment set post_h_value= '%s' where post_id = '%s'" % (h_value[0][0],r)  
            cursor.execute(update)
            db_conn.commit()
        else:
            update="update post_avg_comment set post_h_value= -2 where post_id = '%s'" % (r)  
            cursor.execute(update)
            db_conn.commit()

    #計算真假人數(comment_avg)
    sql= "select comment_p_value from fakenews.comment_avg where post_id = '%s'" % (r)  
    cursor.execute(sql)
    p_count=cursor.fetchall()  
    print(p_count)
    count_false_2 = 0
    count_true_2 = 0
    for p in p_count:
        if p[0] >0:
            count_false_2=count_false_2+1 #機率值>0則認為是假的
        elif p[0] >=-1 and p[0] <0 :
            count_true_2=count_true_2+1 #機率值<=0則認為是真的
        else:
            print("不計算")
        #count_false&count_true存回comment表
    update_1 = "update post_comment_avg set count_false= '%s' ,count_true= '%s' where post_id = '%s'" % (count_false_2,count_true_2,r)  
    update_2 = "update post_avg_comment_avg set count_false= '%s' ,count_true= '%s' where post_id = '%s'" % (count_false_2,count_true_2,r) 
    update_3 = "update post_mode_comment_avg set count_false= '%s' ,count_true= '%s' where post_id = '%s'" % (count_false_2,count_true_2,r) 
    cursor.execute(update_1)
    cursor.execute(update_2)
    cursor.execute(update_3)
    db_conn.commit()

    #case4:c平均(comment_avg)+p人數平均，存回post_avg_comment_avg
    sql_p= "select comment_p_value from fakenews.comment_avg where post_id = '%s'" % (r)
    sql_h= "select comment_h_value from fakenews.comment_avg where post_id = '%s'" % (r)
    cursor.execute(sql_p)
    p_value=cursor.fetchall() 
    cursor.execute(sql_h)
    h_value=cursor.fetchall() 
    #計算機率值(人數平均)
    #存結果
    data=0
    data_f=0 
    data_t=0
    if len(p_value)>1: #超過一則
        for pp in p_value:
            if pp[0] != -2:
                print(pp[0])
                if pp[0] >0:
                    data_f=data_f+pp[0]
                else:
                    data_t=data_t+pp[0]
            else: #此句不計算
                print("不計算")
        if count_true_1 !=0 and count_false_1!=0:
            data=(data_f/count_false_1+data_t/count_true_1)/2
        elif count_false_1 ==0 and count_true_1!=0:
            data=(data_t/count_true_1)/2
        elif count_true_1 ==0 and count_false_1!=0:
            data=(data_f/count_false_1)/2
        else:
            print("人數皆為0")
        data=(f'{data:.4f}') #將浮點數格式化為固定寬度
        print(data) #計算結果
        update="update post_avg_comment_avg set post_p_value='%s' where post_id = '%s'" % (data,r)
        cursor.execute(update)
        db_conn.commit()
    else:
        print("只有一則")
        if p_value != -2:
            update="update post_avg_comment_avg set post_p_value= '%s' where post_id = '%s'" % ( p_value[0][0] , r )  
            cursor.execute(update)
            db_conn.commit()
        else:
            update="update post_avg_comment_avg set post_p_value= -2 where post_id = '%s'" % (r)  
            cursor.execute(update)
            db_conn.commit()
    #計算傷害值
    #存結果
    h_data=0
    h_data_f=0 
    h_data_t=0
    if len(h_value)>1:
        for hh in h_value:
            if hh[0] != -2:
                print(hh[0])
                if hh[0] >0:
                    h_data_f=h_data_f+hh[0]
                else:
                    h_data_t=h_data_t+hh[0]
            else: #此句不計算
                print("不計算")
        if count_true_1 !=0 and count_false_1!=0:
            h_data=(h_data_f/count_false_1+h_data_t/count_true_1)/2
        elif count_false_1 ==0 and count_true_1!=0:
            h_data=(h_data_t/count_true_1)/2
        elif count_true_1 ==0 and count_false_1!=0:
            h_data=(h_data_f/count_false_1)/2
        else:
            print("人數皆為0")
        h_data=(f'{h_data:.4f}') #將浮點數格式化為固定寬度
        print(h_data) #計算結果
        update="update post_avg_comment_avg set post_h_value='%s' where post_id = '%s'" % (h_data,r)
        cursor.execute(update)
        db_conn.commit()
    else:
        print("只有一句")
        if h_value != -2:
            update="update post_avg_comment_avg set post_h_value= '%s' where post_id = '%s'" % (h_value[0][0],r)  
            cursor.execute(update)
            db_conn.commit()
        else:
            update="update post_avg_comment_avg set post_h_value= -2 where post_id = '%s'" % (r)  
            cursor.execute(update)
            db_conn.commit()
    #計算真假人數(comment_max)
    sql= "select comment_p_value from fakenews.comment_mode where post_id = '%s'" % (r)  
    cursor.execute(sql)
    p_count=cursor.fetchall()  
    print(p_count)
    count_false_3 = 0
    count_true_3 = 0
    for p in p_count:
        if p[0] >0:
            count_false_3=count_false_3+1 #機率值>0則認為是假的
        elif p[0] >=-1 and p[0] <0 :
            count_true_3=count_true_3+1 #機率值<=0則認為是真的
        else:
            print("不計算")
    #count_false&count_true存回post表
    update_1 = "update post_comment_mode set count_false= '%s' ,count_true= '%s' where post_id = '%s'" % (count_false_3,count_true_3,r)  
    update_2 = "update post_avg_comment_mode set count_false= '%s' ,count_true= '%s' where post_id = '%s'" % (count_false_3,count_true_3,r) 
    update_3 = "update post_mode_comment_mode set count_false= '%s' ,count_true= '%s' where post_id = '%s'" % (count_false_3,count_true_3,r)
    cursor.execute(update_1)
    cursor.execute(update_2)
    cursor.execute(update_3)
    db_conn.commit()

    #new case5:c極值(comment_mode)+p人數平均，存回post_avg_comment_mode
    sql_p= "select comment_p_value from fakenews.comment_mode where post_id = '%s'" % (r)
    sql_h= "select comment_h_value from fakenews.comment_mode where post_id = '%s'" % (r)
    cursor.execute(sql_p)
    p_value=cursor.fetchall() 
    cursor.execute(sql_h)
    h_value=cursor.fetchall() 
    #計算機率值(人數平均)
    #存結果
    data=0
    data_f=0 
    data_t=0
    if len(p_value)>1: #超過一則
        for pp in p_value:
            if pp[0] != -2:
                print(pp[0])
                if pp[0] >0:
                    data_f=data_f+pp[0]
                else:
                    data_t=data_t+pp[0]
            else: #此句不計算
                print("不計算")
        if count_true_1 !=0 and count_false_1!=0:
            data=(data_f/count_false_1+data_t/count_true_1)/2
        elif count_false_1 ==0 and count_true_1!=0:
            data=(data_t/count_true_1)/2
        elif count_true_1 ==0 and count_false_1!=0:
            data=(data_f/count_false_1)/2
        else:
            print("人數皆為0")
        data=(f'{data:.4f}') #將浮點數格式化為固定寬度
        print(data) #計算結果
        update="update post_avg_comment_mode set post_p_value='%s' where post_id = '%s'" % (data,r)
        cursor.execute(update)
        db_conn.commit()
    else:
        print("只有一則")
        if p_value != -2:
            update="update post_avg_comment_mode set post_p_value= '%s' where post_id = '%s'" % ( p_value[0][0] , r )  
            cursor.execute(update)
            db_conn.commit()
        else:
            update="update post_avg_comment_mode set post_p_value= -2 where post_id = '%s'" % (r)  
            cursor.execute(update)
            db_conn.commit()
    #計算傷害值
    #存結果
    h_data=0
    h_data_f=0 
    h_data_t=0
    if len(h_value)>1:
        for hh in h_value:
            if hh[0] != -2:
                print(hh[0])
                if hh[0] >0:
                    h_data_f=h_data_f+hh[0]
                else:
                    h_data_t=h_data_t+hh[0]
            else: #此句不計算
                print("不計算")
        if count_true_1 !=0 and count_false_1!=0:
            h_data=(h_data_f/count_false_1+h_data_t/count_true_1)/2
        elif count_false_1 ==0 and count_true_1!=0:
            h_data=(h_data_t/count_true_1)/2
        elif count_true_1 ==0 and count_false_1!=0:
            h_data=(h_data_f/count_false_1)/2
        else:
            print("人數皆為0")
        h_data=(f'{h_data:.4f}') #將浮點數格式化為固定寬度
        print(h_data) #計算結果
        update="update post_avg_comment_mode set post_h_value='%s' where post_id = '%s'" % (h_data,r)
        cursor.execute(update)
        db_conn.commit()
    else:
        print("只有一句")
        if h_value != -2:
            update="update post_avg_comment_mode set post_h_value= '%s' where post_id = '%s'" % (h_value[0][0],r)  
            cursor.execute(update)
            db_conn.commit()
        else:
            update="update post_avg_comment_mode set post_h_value= -2 where post_id = '%s'" % (r)  
            cursor.execute(update)
            db_conn.commit()
cursor.close()