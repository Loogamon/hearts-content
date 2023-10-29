#I didn't really like giving the controller file a very similar name to the model files (ex: users.py & user.py), so I decided to go with this filename instead. Less confusion for my own end.
# Do you know how I said I wouldn't do that for the exam...? Well, I lied. I'm still going to make it as organized as possible, however.
from flask import Flask, render_template, session, redirect, request, flash
from flask_app.models.class_users import Users
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.class_nav import NavBar
import datetime
bcrypt = Bcrypt(app)

@app.route('/')
def page_home():
    nav=NavBar.pages("Home");
    # if "user_loggedon" in session:
    #    return redirect('/dashboard')
    return render_template("home.html",nav=nav);
    
@app.route('/content/random')
def page_content_random():
    return redirect('/');

@app.route('/user/login')
def page_user_login():
    nav=NavBar.pages("Login");
    if "user_loggedon" in session:
        return redirect('/user/logout')
    return render_template("login.html",nav=nav);

@app.route('/user/logout')
def page_user_logout():
    session.clear();
    return redirect("/user/login");
    
@app.route('/user/dashboard')
def page_user_dashboard():
    nav=NavBar.pages("Dashboard");
    if "user_loggedon" not in session:
        return redirect('/user/login')
    return render_template("dashboard.html",nav=nav);
    
@app.route('/content/add')
def page_content_add():
    if "user_loggedon" not in session:
        return redirect('/user/login')
    edit={
        "title": "Add New",
        "action": "Post",
        "digimon_ico": "img/mushmon.gif",
        "digimon_name": "Mushmon",
        "location_post": "/action/content/add",
        "location_cancel": "/",
        "content_title": "Detective Series #1: Alternative Theorem",
        "content_desc": "Something about a detective.",
        "content_body": "In one strange night it's been a"
    }
    nav=NavBar.pages("Add New");
    return render_template("add_new.html",nav=nav,edit=edit);