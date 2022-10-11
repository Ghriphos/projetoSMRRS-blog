from flask import Flask, request, render_template
import dbconnect, controller

def insertComment(context, post_id, user_id):
    if isinstance(context, str) and isinstance(post_id, int) and isinstance(user_id, int):
        mydb = dbconnect.connect()
        mycursor = mydb.cursor()
        sql = "insert into comment (context, post_id, user_id) values (%s, %s, %s)"

        val = context, post_id, user_id
        mycursor.execute(sql,val)

        mydb.commit()
        rows_count = mycursor.rowcount
        if rows_count > 0:
            return "comentario feito com sucesso"
        else:
            return "comentario mal-sucedido"

def retrieveComment(comment_id):
    mydb = dbconnect.connect()
    mycursor = mydb.cursor(buffered=True)
    sql = "select title, content, description from posts where post_id = %s;"

    val = comment_id

    mycursor.execute(sql,val)

    mydb.commit()

    rowsCount = mycursor.rowcount
    if rowsCount > 0:
        return "???"
    else:
        return "???"