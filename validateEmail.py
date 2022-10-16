import random, dbconnect

def generateValidationCode():
    validationCode = random.randint(100000, 999999)

    return validationCode

def insertEmailAndValidationCode(email):
    code = generateValidationCode()
    mydb = dbconnect.connect()
    mycursor = mydb.cursor()
    sql = "insert into validation_codes (email, validation_code) values (%s, %s)"
    val = email, code
    mycursor.execute(sql,val)
    mydb.commit()
    rowsCount = mycursor.rowcount

    return "código cadastrado"