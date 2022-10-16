import mysql.connector

def connect():
    dbconnection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="researchprojectdb")
        
    return(dbconnection)