from flask import Flask, request, render_template, session, redirect
from dotenv import load_dotenv
from datetime import datetime

import usersUtility, posts, comments, os, re

load_dotenv()

app = Flask(__name__, static_url_path='/static/')
app.secret_key = os.getenv('SECRET_KEY')

@app.route("/blog",methods=['GET'])
def viewPosts():
    posts_list = []
    
    for post in posts.retrievePosts():
        [id, author_id, content, title, description, photo, created_at] = post
        author_user = usersUtility.retrieveUser(str(author_id))[0]
        
        posts_list.append({
            'id': id,
            'author': author_user[2],
            'title': title,
            'description': description,
            'content': content,
            'photo': photo,
            'comments': comments.countComments(str(id)),
            'created_at': created_at.strftime("%d de %B, %Y"),
        })

    return render_template("posts.jinja", posts=posts_list)

@app.route("/register",methods=['GET'])
def renderRegister():
    if 'username' in session:
        return redirect('/')

    return render_template("register.jinja")

@app.route("/login",methods=['GET'])
def renderLogin():
    if 'username' in session:
        return redirect('/')

    return render_template("login.jinja")

@app.route("/post/<id>",methods=['GET'])
def renderPost(id):
    result = posts.retrievePost(id)

    if isinstance(result, str):
        return redirect("/") # 404 or 500

    [post_id, user_id, content, title, description, photo, created_at] = result[0]
    author_user = usersUtility.retrieveUser(str(user_id))[0]

    post = {'id': post_id, 'title': title, 'description': description, 'content': content, 'photo': photo, 'created_at': created_at.strftime("%d de %B, %Y")}
    author = {'username': author_user[2]} # todo fetch post user

    post_comments = []
    
    for comment in comments.retrievePostComment(str(post_id)):
        [comment_id, author_id, post_id, content, created_at] = comment

        user = usersUtility.retrieveUser(str(author_id))[0]

        post_comments.append({
            'author': user[2],
            'content': content,
            'created_at': created_at
        })

    return render_template("post.jinja", post=post, author=author, comments=post_comments)

@app.route("/post/<id>/comment",methods=['POST'])
def createCommentPost(id):
    if re.match("^[0-9]+$", id) or 'id' not in session:
        content = request.form['content']
        
        if isinstance(content, str) and len(content) < 1024:
            comments.insertComment(content, id, str(session['id']))

            return redirect(f'/post/{id}')

    return redirect(f'/')

@app.route("/login",methods=['POST'])
def userLogin():
    email = request.form['email']
    passwd = request.form['passwd']

    return usersUtility.userLogin(email,passwd)

@app.route("/logout",methods=['POST'])
def logout():
    session.pop('id', None)
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

# @app.route("/selectPosts",methods=['POST'])
# def selectPost():
#     post_id = request.form['post_id']
    
#     return posts.retrievePost(post_id)
    
# @app.route("/comments", methods=['POST'])
# def createComment():
#     user_id = request.form['user_id']
#     post_id = request.form['post_id']
#     content = request.form['content']

#     return comments.insertComment(content, post_id, user_id)

# @app.route("/selectComment",methods=['POST'])
# def selectComment():
#     comment_id = request.form['comment_id']
    
#     return comments.retrieveComment(comment_id)

# @app.route("/selectPostComment",methods=['POST'])
# def selectPostComment():
#     post_id = request.form['post_id']
    
#     return comments.retrievePostComment(post_id)

# @app.route("/selectUsers",methods=['POST'])
# def selectUsers():
#     user_id = request.form['user_id']
    
#     return usersUtility.retrieveUser(user_id)