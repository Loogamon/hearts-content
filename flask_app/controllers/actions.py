from flask import Flask, render_template, session, redirect, request, flash
from flask_app.models.class_users import Users
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.class_nav import NavBar
from flask_app.models.class_content import Articles
from flask_app.models.class_comment import Comments
import datetime
bcrypt = Bcrypt(app)

@app.route('/action/user/signup',methods=['POST'])
def action_user_signup():
    if "user_loggedon" in session:
        return redirect("/");
    if not Users.check_valid_signup(request.form):
        print("BLOCKED!")
        return redirect('/user/login')
    data = { 
        "first_name": request.form['signup_fname'],
        "last_name": request.form['signup_lname'],
        "email": request.form['signup_email'],
        "password": bcrypt.generate_password_hash(request.form['signup_password1'])
        }
    Users.save(data)
    session['user_loggedon']=True
    session['user_email']=request.form['signup_email']
    return redirect("/");
    
@app.route('/action/user/login',methods=['POST'])
def action_user_login():
    if "user_loggedon" in session:
        return redirect("/");
    data = { 
        "email": request.form['login_email'],
        "password": request.form['login_password']
        }
    if not Users.check_valid_login(data):
        print("BLOCKED!")
        return redirect('/user/login')
    session['user_loggedon']=True
    session['user_email']=request.form['login_email']
    return redirect("/");
    
@app.route('/action/content/add',methods=['POST'])
def action_content_add():
    if "user_loggedon" not in session:
        return redirect('/user/login')
    if "page" not in session:
        return redirect('/')
    print(request.form)
    if not Articles.check_valid(request.form):
        session['prev']=True
        session['prev_title']=request.form['content_title']
        session['prev_desc']=request.form['content_desc']
        session['prev_body']=request.form['content_body']
        return redirect(session['page'])
    user=Users.get_userinfo(session['user_email'])
    where=Articles.save(request.form,user.id)
    return redirect(f"/content/view/{where}");
    
@app.route('/action/content/edit',methods=['POST'])
def action_content_edit():
    if "user_loggedon" not in session:
        return redirect('/user/login')
    if "page" not in session:
        return redirect('/')
    if "edit_id" not in session:
        return redirect('/')
    print(request.form)
    if not Articles.check_valid(request.form):
        session['prev']=True
        session['prev_title']=request.form['content_title']
        session['prev_desc']=request.form['content_desc']
        session['prev_body']=request.form['content_body']
        return redirect(session['page'])
    user=Users.get_userinfo(session['user_email'])
    Articles.update(request.form,session['edit_id'],user.id)
    return redirect(f"/content/view/{session['edit_id']}");
    
@app.route('/action/comment/add',methods=['POST'])
def action_comment_add():
    if "user_loggedon" not in session:
        return redirect('/user/login')
    
    print(request.form)
    if not Comments.check_valid(request.form):
        session['prev']=True
        session['prev_body']=request.form['content_body']
        return redirect(f"/content/view/{session['edit_id']}");
    user=Users.get_userinfo(session['user_email'])
    Comments.save(request.form,session['edit_id'],user.id)
    return redirect(f"/content/view/{session['edit_id']}");