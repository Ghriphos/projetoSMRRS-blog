from flask import Flask, request, render_template, session, redirect
from dotenv import load_dotenv
from datetime import datetime

import usersUtility, posts, comments, os

load_dotenv()

app = Flask(__name__, static_url_path='/static/')
app.secret_key = os.getenv('SECRET_KEY')

@app.route("/",methods=['GET'])
def renderMain():
    return render_template("main.jinja")

@app.route("/register",methods=['GET'])
def renderRegister():
    return render_template("register.jinja")

@app.route("/login",methods=['GET'])
def renderLogin():
    return render_template("login.jinja")

@app.route("/post/<id>",methods=['GET'])
def renderPost(id):
    result = posts.retrievePost(id)

    if isinstance(result, str):
        return redirect("/") # 404 or 500

    [post_id, user_id, content, title, description, photo, created_at] = result[0]

    post = {'id': post_id, 'title': title, 'description': description, 'content': content, 'photo': photo, 'created_at': created_at.strftime("%d de %B, %Y")}
    author = {'username': user_id} # todo fetch post user

    return render_template("post.jinja", post=post, author=author)

@app.route("/login",methods=['POST'])
def userLogin():
    email = request.form['email']
    passwd = request.form['passwd']

    return usersUtility.userLogin(email,passwd)

@app.route("/logout",methods=['POST'])
def logout():
    session.pop('username', None)

    return render_template("main.jinja")

@app.route("/register",methods=['POST'])
def emailRegister():
    email = request.form['email']
    username = request.form['username']
    passwd = request.form['passwd']
    
    return usersUtility.userRegister(email, username, passwd)

@app.route("/posts",methods=['POST'])
def createPost():
    user_id = request.form['user_id']
    title = request.form['title']
    content = request.form['content']
    description = request.form['description']
    photo = request.form['photo']
    
    return posts.insertPost(user_id, title, content, description, photo)

@app.route("/selectPosts",methods=['POST'])
def selectPost():
    post_id = request.form['post_id']
    
    return posts.retrievePost(post_id)
    
@app.route("/comments", methods=['POST'])
def createComment():
    user_id = request.form['user_id']
    post_id = request.form['post_id']
    content = request.form['content']

    return comments.insertComment(content, post_id, user_id)

@app.route("/selectComment",methods=['POST'])
def selectComment():
    comment_id = request.form['comment_id']
    
    return comments.retrieveComment(comment_id)

@app.route("/selectPostComment",methods=['POST'])
def selectPostComment():
    post_id = request.form['post_id']
    
    return comments.retrievePostComment(post_id)