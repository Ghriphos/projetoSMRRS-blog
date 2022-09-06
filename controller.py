from flask import Flask, request
import userRegister

app = Flask(__name__)

@app.route("/",methods=['POST'])
def emailRegister():
    email = request.form['email']
    username = request.form['username']
    passwd = request.form['passwd']
    
    return userRegister.userRegister(email, username, passwd), userRegister.valid_mail_characters(email)
