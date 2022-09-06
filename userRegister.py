from flask import Flask, request
import dbconnect
import controller
import validateEmail
import re

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
            return "Caso esse email seja valido, você receberá um email em sua caixa de entrada, juntamente com um código de validação do email", validateEmail.insertEmailAndValidationCode(email)
        else:
            return "Houve um erro interno"
    return "a lista de caracteres não coincide com as permitidas no sistema, por favor, reveja os parametros informados e tente novamente."

