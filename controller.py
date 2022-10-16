from flask import Flask, request, render_template
from dotenv import load_dotenv
import usersUtility, posts, comments, os

load_dotenv()

app = Flask(__name__, static_url_path='/static/')
app.secret_key = os.getenv('SECRET_KEY')

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