from flask import Flask, request
import userRegister

app = Flask(__name__)

@app.route("/",methods=['POST'])
def emailRegister():
    email = request.form['email']
    
    return userRegister.userRegister(email), userRegister.solve(email)
