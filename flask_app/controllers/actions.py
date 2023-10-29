#I didn't really like giving the controller file a very similar name to the model files (ex: users.py & user.py), so I decided to go with this filename instead. Less confusion for my own end.
# Do you know how I said I wouldn't do that for the exam...? Well, I lied. I'm still going to make it as organized as possible, however.
from flask import Flask, render_template, session, redirect, request, flash
from flask_app.models.class_users import Users
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.class_nav import NavBar
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