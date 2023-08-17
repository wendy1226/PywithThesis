# -*- coding:utf-8 -*-
from asyncio.windows_events import NULL
from distutils.util import execute
from importlib.resources import path
from sqlite3 import Cursor
from mysql.connector import Error
import pymysql

db_conn = pymysql.connect(host='127.0.0.1',database='fakenews',user='root',password='1234')
cursor=db_conn.cursor()
#公式1:最後一句權重較高
sql_p= """select sentence_p_value from fakenews.sentence where source_comment_id = 26 order by sentence_number """
sql_h= """select sentence_h_value from fakenews.sentence where source_comment_id = 26 order by sentence_number """
sql_u="update comment set comment_p_value= %s where comment_id = 26"
sql_uh="update comment set comment_h_value= %s where comment_id = 26"
cursor.execute(sql_p)
p_value=cursor.fetchall() 
cursor.execute(sql_h)
h_value=cursor.fetchall() 

print(len(p_value))
print(len(h_value))

data=0 #存結果
if len(p_value)>1:
  i=0
  for pp in p_value:
    if p_value != -2:
      if i==len(p_value)-1:
        print(pp[0])
        data=(data+pp[0]*m)/(len(p_value)-1+m)
      else:
        print(pp[0])
        data=data+pp[0] 
        i=i+1
    else:
      cursor.execute(sql_u,-2)
      db_conn.commit()
  data=(f'{data:.4f}') #將浮點數格式化為固定寬度
  print(data) #計算結果
  try:
    cursor.execute(sql_u,data)
    db_conn.commit()
  except:
    print("failed")
else:
  print("只有一句")
  if p_value != -2:
    cursor.execute(sql_u,p_value)
    db_conn.commit()
  else:
    cursor.execute(sql_u,-2)
    db_conn.commit()

m=2 #宣告最後一句權重
datah=0 #存結果
if len(h_value)>1:
  i=0
  for hh in h_value:
    if h_value != -2:
      if i==len(h_value)-1:
        print(hh[0])
        datah=(datah+hh[0]*m)/(len(h_value)-1+m)
      else:
        print(hh[0])
        datah=datah+hh[0] 
        i=i+1
    else:
      cursor.execute(sql_uh,-2)
      db_conn.commit()
  datah=(f'{datah:.4f}') #將浮點數格式化為固定寬度
  print(datah) #計算結果
  try:
    cursor.execute(sql_uh,datah)
    db_conn.commit()
  except:
    print("failed")
else:
  print("只有一句")
  if p_value != -2:
    cursor.execute(sql_uh,h_value)
    db_conn.commit()
  else:
    cursor.execute(sql_uh,-2)
    db_conn.commit()

#計算真假人數
sql_1= """
select sentence_p_value from fakenews.sentence where source_comment_id = 26
"""
cursor.execute(sql_1)
p_count=cursor.fetchall()  
print(p_count)
cfalse = 0
ctrue = 0

for i in p_count:
    if i[0] >0:
        cfalse=cfalse+1 #機率值>0則認為是假的
    elif i[0] >=-1:
        ctrue=ctrue+1 #機率值<=0則認為是真的
    else:
        print("不計算")
c=(cfalse,ctrue)
#count_false&count_true存回comment表
sql_c = """
    update comment set count_false= %s,count_true= %s where comment_id = 26
    """
try:
    cursor.execute(sql_c,c)
    db_conn.commit()
except:
    print("failed")
cursor.close()