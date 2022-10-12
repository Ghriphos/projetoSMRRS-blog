from flask import Flask, request, render_template

app = Flask(__name__, static_url_path='/static/')

@app.route("/",methods=['GET'])
def renderMain():
    return render_template("main.jinja")

@app.route("/register",methods=['GET'])
def renderRegister():
    return render_template("register.jinja")

@app.route("/login",methods=['GET'])
def renderLogin():
    return render_template("login.jinja")