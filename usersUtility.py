from flask import Flask, request, render_template, session, redirect
import dbconnect, controller, validateEmail, re, bcrypt

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
    if 'username' in session:
        return redirect('/')

    if (valid_mail_characters(email)):
        if verifyDuplicatedEmail(email):
            if verifyDuplicatedUsername(username):
                salt = bcrypt.gensalt()
                passwd = passwd.encode('utf-8')
                hashedPasswd = bcrypt.hashpw(passwd, salt)
                print(hashedPasswd)

                mydb = dbconnect.connect()
                mycursor = mydb.cursor()
                sql = "insert into users (email, username, passwd) values (%s, %s, %s)"
                val = email, username, hashedPasswd
                mycursor.execute(sql, val)
                mydb.commit()

                rowsCount = mycursor.rowcount
                if rowsCount > 0:
                    return redirect("/login")
                else:
                    return render_template('register.jinja', error="Houve um erro interno.")
            return render_template('register.jinja', error="Nome de usuário já foi cadastrado.")
        return render_template('register.jinja', error="Este email já pertence a uma conta registrada.")
    return render_template('register.jinja', error="A lista de caracteres não coincide com as permitidas no sistema, por favor, reveja os parametros informados e tente novamente.")

def userLogin(email, passwd):
    if 'username' in session:
        return redirect('/')

    if (valid_mail_characters(email)):
        mydb = dbconnect.connect()
        mycursor = mydb.cursor(buffered=True)
        sql = "select passwd from users where email = %s;"
        val = (email,)
        mycursor.execute(sql,val)
        mydb.commit()
        hashedPasswd = mycursor.fetchall()
        hashedPasswd = hashedPasswd[0][0]
        print(hashedPasswd)

        if bcrypt.checkpw(passwd.encode('utf-8'),hashedPasswd.encode('utf-8')):
            sql = "select * from users where email = %s and passwd = %s;"
            val = email, hashedPasswd
            mycursor.execute(sql, val)
            mydb.commit()
            myresult = mycursor.fetchall()

            rowsCount = mycursor.rowcount
            if rowsCount > 0:
                session['username'] = myresult[0][2]
                print(session['username'])
                return redirect("/")
            else:
                return render_template('login.jinja', error='Email ou senha incorretos')
        return render_template('login.jinja', error="A senha informada não coincide com a cadastrada neste email")
    return render_template('login.jinja', error="A lista de caracteres não coincide com as permitidas no sistema, por favor, reveja os parametros informados e tente novamente.")