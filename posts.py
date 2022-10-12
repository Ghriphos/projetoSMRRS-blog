from flask import Flask, request, render_template
import dbconnect, controller


def insertPost(user_id, title, text, description, photo):
    if isinstance(user_id, int) and isinstance(title, str) and isinstance(text, str) and isinstance(description, str) and isinstance(photo, str):
        mydb = dbconnect.connect()
        mycursor = mydb.cursor()
        sql = "insert into posts (user_id, title, content, description, photo) values (%s, %s, %s, %s, %s)"

        val = user_id, title, text, description, photo
        mycursor.execute(sql,val)

        mydb.commit()
        rows_count = mycursor.rowcount
        if rows_count > 0:
            return "postagem concluída"
        else:
            return "postagem mal-sucedida"
    return "parametros incorretos"

def retrievePost(post_id):
    mydb = dbconnect.connect()
    mycursor = mydb.cursor(buffered=True)
    sql = "select title, content, description from posts where post_id = %s;"

    val = post_id

    mycursor.execute(sql,val)

    mydb.commit()

    rowsCount = mycursor.rowcount
    if rowsCount > 0:
        return "???"
    else:
        return "???"

