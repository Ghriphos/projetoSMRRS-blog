from flask import Flask, request, render_template
import usersUtility, posts

app = Flask(__name__, static_url_path='/static/')

@app.route("/login",methods=['POST'])
def userLogin():
    email = request.form['email']
    passwd = request.form['passwd']

    return usersUtility.userLogin(email,passwd)

@app.route("/register",methods=['POST'])
def emailRegister():
    email = request.form['email']
    username = request.form['username']
    passwd = request.form['passwd']
    
    return usersUtility.userRegister(email, username, passwd), usersUtility.valid_mail_characters(email)

@app.route("/posts",methods=['POST'])
def createPost():
    user_id = request.form['user_id']
    title = request.form['title']
    content = request.form['content']
    description = request.form['description']
    photo = request.form['photo']
    
    return posts.insertPost(user_id, title, content, description, photo)

