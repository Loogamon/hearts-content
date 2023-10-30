#I didn't really like giving the controller file a very similar name to the model files (ex: users.py & user.py), so I decided to go with this filename instead. Less confusion for my own end.
# Do you know how I said I wouldn't do that for the exam...? Well, I lied. I'm still going to make it as organized as possible, however.
from flask import Flask, render_template, session, redirect, request, flash
from flask_app.models.class_users import Users
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.class_nav import NavBar
from flask_app.models.class_content import Articles
import datetime
bcrypt = Bcrypt(app)

@app.route('/')
def page_home():
    nav=NavBar.pages("Home");
    latest_content=Articles.get_all();
    liked_content=Articles.get_all_by_like();
    # if "user_loggedon" in session:
    #    return redirect('/dashboard')
    return render_template("home.html",nav=nav,latest_content=latest_content,liked_content=liked_content);
    
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
    user=Users.get_userinfo(session['user_email'])
    user_content=Articles.get_all_by_user(user.id);
    return render_template("dashboard.html",nav=nav,user_content=user_content);
    
@app.route('/content/add')
def page_content_add():
    if "user_loggedon" not in session:
        return redirect('/user/login')
    edit={
        "route": "/content/add",
        "title": "Add New",
        "action": "Post",
        "digimon_ico": "img/mushmon.gif",
        "digimon_name": "Mushmon",
        "location_post": "/action/content/add",
        "location_cancel": "/",
        "content_title": "",
        "content_desc": "",
        "content_body": ""
    }
    if "prev" in session:
        if session['prev']==True:
            session['prev']=False
            print("PREVIOUSLY ON BIG BABY")
            edit["content_title"]=session['prev_title']
            edit["content_desc"]=session['prev_desc']
            edit["content_body"]=session['prev_body']
            
    session['page']=edit["route"]
    nav=NavBar.pages("Add New");
    return render_template("add_new.html",nav=nav,edit=edit);
    
@app.route('/content/edit/<int:edit_id>')
def page_content_edit(edit_id):
    if "user_loggedon" not in session:
        return redirect('/user/login')
    content=Articles.get_one(edit_id);
    edit={
        "route": f"/content/edit/{edit_id}",
        "title": "Editing Content",
        "action": "Done",
        "digimon_ico": "img/floramon.gif",
        "digimon_name": "Floramon",
        "location_post": "/action/content/edit",
        "location_cancel": "/user/dashboard",
        "content_title": content.title,
        "content_desc": content.description,
        "content_body": content.body
    }
    if "prev" in session:
        if session['prev']==True:
            session['prev']=False
            print("PREVIOUSLY ON BIG BABY")
            edit["content_title"]=session['prev_title']
            edit["content_desc"]=session['prev_desc']
            edit["content_body"]=session['prev_body']
            
    session['page']=edit["route"]
    session['edit_id']=edit_id
    nav=NavBar.pages("");
    return render_template("add_new.html",nav=nav,edit=edit);
    
@app.errorhandler(404)
def page_404(e):
     nav=NavBar.pages("")
     error_txt={
        "title": "404 Not Found",
        "desc": "You know the drill, or something like that."
     }
     return render_template("error_message.html",nav=nav,error_txt=error_txt);