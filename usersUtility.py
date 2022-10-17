from flask import Flask, request, render_template, session
import dbconnect, controller, validateEmail, re

def valid_mail_characters(emailToTest):
    allowedCharacters = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(allowedCharacters,emailToTest):
        return True
    return False

def verifyDuplicatedUsername(username):
    mydb = dbconnect.connect()
    mycursor = mydb.cursor(buffered=True)
    sql = "select * from users where username = (%s)"
    val = (username,)
    mycursor.execute(sql, val)
    mydb.commit()
    rowsCount = mycursor.rowcount

    if rowsCount > 0:
        return False
    else:
        return True

def verifyDuplicatedEmail(email):
    mydb = dbconnect.connect()
    mycursor = mydb.cursor(buffered=True)
    sql = "select * from users where email = (%s)"
    val = (email,)
    mycursor.execute(sql, val)
    mydb.commit()
    rowsCount = mycursor.rowcount

    if rowsCount > 0:
        return False
    else:
        return True


def userRegister(email, username, passwd):
    if (valid_mail_characters(email)):
        if verifyDuplicatedEmail(email):
            if verifyDuplicatedUsername(username):
                mydb = dbconnect.connect()
                mycursor = mydb.cursor()
                sql = "insert into users (email, username, passwd) values (%s, %s, %s)"
                val = email, username, passwd
                mycursor.execute(sql, val)
                mydb.commit()

                rowsCount = mycursor.rowcount
                if rowsCount > 0:
                    session['username'] = username
                    print(session['username'])
                    return render_template("main.jinja")
                else:
                    return render_template('register.jinja', error="Houve um erro interno.")
            return render_template('register.jinja', error="Nome de usuário já foi cadastrado.")
        return render_template('register.jinja', error="Este email já pertence a uma conta registrada.")
    return render_template('register.jinja', error="A lista de caracteres não coincide com as permitidas no sistema, por favor, reveja os parametros informados e tente novamente.")

def userLogin(email, passwd):
    if (valid_mail_characters(email)):
        mydb = dbconnect.connect()
        mycursor = mydb.cursor(buffered=True)
        sql = "select * from users where email = %s and passwd = %s;"
        val = email, passwd
        mycursor.execute(sql, val)
        mydb.commit()
        myresult = mycursor.fetchall()

        rowsCount = mycursor.rowcount
        if rowsCount > 0:
            session['username'] = myresult[0][2]
            print(session['username'])
            return render_template('main.jinja')
        else:
            return render_template('login.jinja', error='ou tu n tem cadastro ou botou errado joia?')
    return render_template('login.jinja', error="A lista de caracteres não coincide com as permitidas no sistema, por favor, reveja os parametros informados e tente novamente.")