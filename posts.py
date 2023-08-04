from venv import create
from flask import Flask, request, render_template
from datetime import datetime
import dbconnect, controller, re, dateFunctions


def insertPost(user_id, title, content, description, photo):
    intAllowedCharacters = "^[0-9]+$"
    if re.match(intAllowedCharacters,user_id):
        created_at = dateFunctions.now()
        user_id = int(user_id)
        mydb = dbconnect.connect()
        mycursor = mydb.cursor()
        sql = "insert into posts (user_id, title, content, description, photo, created_at) values (%s, %s, %s, %s, %s, %s)"
        val = user_id, title, content, description, photo, created_at
        mycursor.execute(sql,val)
        mydb.commit()
        rows_count = mycursor.rowcount

        if rows_count > 0:
            return "postagem concluída"
        else:
            return "postagem mal-sucedida"

    else:
        return "Parametros incorretos"

def retrievePost(post_id):
    intAllowedCharacters = "^[0-9]+$"
    if re.match(intAllowedCharacters, post_id):
        post_id = int(post_id)
        mydb = dbconnect.connect()
        mycursor = mydb.cursor(buffered=True)
        post_id = str(post_id)
        sql = "select * from posts where post_id = " + post_id
        mycursor.execute(sql)
        mydb.commit()
        myresult = mycursor.fetchall()
        rowsCount = mycursor.rowcount

        if rowsCount > 0:
            return myresult
        else:
            return "deu ruim"

    else:
        return "parametros incorretos"

def retrievePosts():
    mydb = dbconnect.connect()
    mycursor = mydb.cursor(buffered=True)

    sql = "select * from posts order by post_id desc"
    mycursor.execute(sql)
    mydb.commit()
    
    myresult = mycursor.fetchall()
    rowsCount = mycursor.rowcount

    if rowsCount > 0:
        return myresult
    else:
        return []
