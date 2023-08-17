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
    #計算機率值
    m=2 #宣告最後一句權重
    data=0 #存結果
    total=len(p_value) #存總數量
    if len(p_value)>1: #超過一句
        i=0
        for pp in p_value:
            if i==len(p_value)-1: #最後一句
                if pp[0] != -2: #此句有要計算
                    data=(data+pp[0]*m)/(total-1+m)
                else: #最後一句是不計算的
                    total=total-1
                    if total==0:
                        data=-2
                    else:
                        data=data/total
            else: #不是最後一句
                if pp[0] != -2: #此句有要計算
                    data=data+pp[0] 
                else: #不計算
                    print("不計算")
                    total=total-1
            i=i+1
        data=(f'{data:.4f}') #將浮點數格式化為固定寬度
        print(data) #計算結果
        update="update comment set comment_p_value='%s' where comment_id = '%s'" % (data,r) #最後一句權重高的公式
        cursor.execute(update)
        db_conn.commit()
    else:
        print("只有一句")
        if p_value != -2:
            update="update comment set comment_p_value= '%s' where comment_id = '%s'" % ( p_value[0][0] , r )  
            cursor.execute(update)
            db_conn.commit()
        else:
            update="update comment set comment_p_value= -2 where comment_id = '%s'" % (r)  
            cursor.execute(update)
            db_conn.commit()
    #計算傷害值
    m=2 #宣告最後一句權重
    h_data=0 #存結果
    total_h=len(h_value) #存總數量
    if len(h_value)>1:
        i=0
        for hh in h_value:
            if i==len(h_value)-1: #最後一句
                if hh[0] != -2: #此句有要計算
                    h_data=(h_data+hh[0]*m)/(total_h-1+m)
                else: #最後一句是不計算的
                    total_h=total_h-1
                    if total_h==0:
                        h_data=-2
                    else:
                        h_data=h_data/total_h
            else: #不是最後一句
                if hh[0] != -2: #此句有要計算
                    h_data=h_data+hh[0] 
                else: #不計算
                    print("不計算")
                    total_h=total_h-1
            i=i+1
        h_data=(f'{h_data:.4f}') #將浮點數格式化為固定寬度
        print(h_data) #計算結果
        update="update comment set comment_h_value='%s' where comment_id = '%s'" % (h_data,r) #最後一句權重高的公式
        cursor.execute(update)
        db_conn.commit()
    else:
        print("只有一句")
        if h_value != -2:
            update="update comment set comment_h_value= '%s' where comment_id = '%s'" % (h_value[0][0],r)  
            cursor.execute(update)
            db_conn.commit()
        else:
            update="update comment set comment_h_value= -2 where comment_id = '%s'" % (r)  
            cursor.execute(update)
            db_conn.commit()
    #更新0為-2
    sql_up= "update comment set comment_p_value=-2 where comment_p_value=0 and comment_id ='%s'" % (r)
    sql_uh= "update comment set comment_h_value=-2 where comment_h_value=0 and comment_id ='%s'" % (r)
    cursor.execute(sql_up)
    cursor.execute(sql_uh)
    db_conn.commit()
    #計算真假人數
    print(r)
    sql= "select sentence_p_value from fakenews.sentence where source_comment_id = '%s'" % (r)  
    cursor.execute(sql)
    p_count=cursor.fetchall()  
    print(p_count)
    count_false = 0
    count_true = 0
    for p in p_count:
        if p[0] >0:
            count_false=count_false+1 #機率值>0則認為是假的
        elif p[0] >=-1 and p[0] <0 :
            count_true=count_true+1 #機率值<=0則認為是真的
        else:
            print("不計算")
    print(count_false,count_true)
    update = "update comment set count_false= '%s' ,count_true= '%s' where comment_id = '%s'" % (count_false,count_true,r)  
    cursor.execute(update)
    db_conn.commit()
cursor.close()