#! /usr/bin/python3
# -*- coding: UTF-8 -*-
# enable debugging
import cgitb
cgitb.enable()
import textwrap
import os, sys, io, cgi
sys.path.append('/home/makizaki/.local/lib/python3.8/site-packages')
import MySQLdb
form = cgi.FieldStorage(keep_blank_values = True )
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
print("Content-Type: text/html;charset=utf-8\n")
print( """

<!DOCTYPE html>
<html>
    <head>
        <title>一言掲示板</title>
    </haed>
    <body>
            <form action ="bbs.py" method="post">
            <input type = "hidden" name= "method" value="post">
            <div>
                <label for="name">氏名</label>
                <input id="name" type="text" name="name" >
            </div>
                <label for="content">内容</label>
                <div style =  "display: inline-block; height: 50px">
                <textarea ="content" name="content" cols="30" rows="5" ></textarea>
                </div>
                <div style =  "display: inline-block; position: relative;bottom: 9px;">
                <input type="submit" name="btn_submit" value="送信">
                </div>
            </form>
</html>

            """)

#接続
con = MySQLdb.connect(
user='test',
passwd='test',
host='localhost',
db='bbs_db',
charset="utf8")
cur= con.cursor()

#リダイレクト
def redirect():
            source =textwrap.dedent( '''
            <html>
                <head>
                    <meta http-equiv="refresh" content=0; url=./bbs.py">
                </head>
                <body>
                    メッセージの登録に成功しました。
                </body>
            </html>
            ''' )
            print(source)

#表示
cur.execute("select * from bbs_tb order by id desc;")
rows = cur.fetchall()
for row in rows:
    post_text=("""
            <div style=" margin: 10px 10%; background-color:#E6FFE9">
               <p>氏名:{name} </br> {content}</p>
            </div>
                """).format(
                        name = row[1],
                        content = row[2],
            )
    print(post_text)

name = form.getvalue('name')
content = form.getvalue('content')
method = form.getvalue('method')

#条件
if(method == 'post' and not name == "" and not content ==""):
        sql = 'insert into bbs_tb(name, content) values (%s, %s)'
        cur.execute(sql, (name, content))
        con.commit()
        redirect()
elif(method == 'post'and (name == "" or content =="")):
                 print("""
                 <p id='error_message'>
                 表示名かメッセージが入力されていません</p>
                 """)
cur.close
con.close
