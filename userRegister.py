from flask import Flask, request
import dbconnect
import server
import re

def solve(emailToTest):
    allowedCharacters = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(allowedCharacters,emailToTest):
      return True
    return False


def userRegister(email, username, passwd):
    if (solve(email)):
        mydb = dbconnect.connect()
        mycursor = mydb.cursor()
        sql = "insert into users (email, username, passwd) values (%s, %s, %s)"
        val = email, username, passwd
        mycursor.execute(sql,val)
        print("passou aqui")

        mydb.commit()

        rowsCount = mycursor.rowcount
        print(rowsCount)

        return "Caso esse email seja valido, você receberá um email em sua caixa de entrada"
    return "a lista de caracteres não coincide com as permitidas no sistema, por favor, reveja os parametros informados e tente novamente."

