from flask import Flask, request, render_template
import dbconnect, controller, re, dateFunctions

def insertComment(content, post_id, user_id):
    intAllowedCharacters = "^[0-9]+$"
    if re.match(intAllowedCharacters, post_id) and re.match(intAllowedCharacters, user_id):
        created_at = dateFunctions.now()
        mydb = dbconnect.connect()
        mycursor = mydb.cursor()
        sql = "insert into comments (content, post_id, user_id, created_at) values (%s, %s, %s, %s)"
        val = content, post_id, user_id, created_at
        mycursor.execute(sql,val)
        mydb.commit()
        rows_count = mycursor.rowcount

        if rows_count > 0:
            return "comentario feito com sucesso"
        else:
            return "comentario mal-sucedido"
            
    else:
        return "parametros incorretos"

def retrieveComment(comment_id):
    intAllowedCharacters = "^[0-9]+$"
    if re.match(intAllowedCharacters, comment_id):
        mydb = dbconnect.connect()
        mycursor = mydb.cursor(buffered=True)
        comment_id = str(comment_id)
        sql = "select * from comments where comment_id = %s"
        val = (comment_id,)
        mycursor.execute(sql, val)
        mydb.commit()
        myresult = mycursor.fetchall()
        rowsCount = mycursor.rowcount

        if rowsCount > 0:
            return myresult
        else:
            return "deu ruim"

    else:
        return "parametros incorretos"

def retrievePostComment(post_id):
    intAllowedCharacters = "^[0-9]+$"
    if re.match(intAllowedCharacters, post_id):
        mydb = dbconnect.connect()
        mycursor = mydb.cursor(buffered=True)
        post_id = str(post_id)
        sql = "select * from comments where post_id = %s"
        val = (post_id,)
        mycursor.execute(sql, val)
        mydb.commit()
        myresult = mycursor.fetchall()
        rowsCount = mycursor.rowcount

        if rowsCount > 0:
            return myresult
        else:
            return []