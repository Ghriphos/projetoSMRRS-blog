from flask import Flask, request, render_template
import dbconnect, controller, validateEmail, re

def valid_mail_characters(emailToTest):
    allowedCharacters = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(allowedCharacters,emailToTest):
        return True
    return False

def userRegister(email, username, passwd):
    if (valid_mail_characters(email)):
        mydb = dbconnect.connect()
        mycursor = mydb.cursor()
        sql = "insert into users (email, username, passwd) values (%s, %s, %s)"
        val = email, username, passwd
        mycursor.execute(sql,val)

        mydb.commit()

        rowsCount = mycursor.rowcount
        if rowsCount > 0:
            return render_template("main.jinja")
        else:
            return render_template('register.jinja', error="Houve um erro interno.")     
    return render_template('register.jinja', error="A lista de caracteres não coincide com as permitidas no sistema, por favor, reveja os parametros informados e tente novamente.")

def userLogin(email, passwd):
    mydb = dbconnect.connect()
    mycursor = mydb.cursor(buffered=True)
    sql = "select * from users where email = %s and passwd = %s;"

    val = email, passwd
    mycursor.execute(sql,val)

    mydb.commit()

    rowsCount = mycursor.rowcount
    if rowsCount > 0:
        return render_template('main.jinja')
    else:
        return render_template('login.jinja', error='ou tu n tem cadastro ou botou errado joia?')