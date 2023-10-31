#I didn't really like giving the controller file a very similar name to the model files (ex: users.py & user.py), so I decided to go with this filename instead. Less confusion for my own end.
# Do you know how I said I wouldn't do that for the exam...? Well, I lied. I'm still going to make it as organized as possible, however.
from flask import Flask, render_template, session, redirect, request, flash
from flask_app.models.class_users import Users
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.class_nav import NavBar
from flask_app.models.class_content import Articles
from flask_app.models.class_comment import Comments
import datetime
import random
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
    pick=Articles.get_all()
    num=random.randint(0,len(pick)-1)
    a_num=pick[num].id
    return redirect(f"/content/view/{a_num}");

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
    session['delete_page']="dashboard"
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
    if content==None:
        return redirect('/error/missing-content')
    user=Users.get_userinfo(session['user_email'])
    if not content.author_id==user.id:
        return redirect('/error/block-action')
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

@app.route('/user/profile/<int:user_id>')
def page_profile(user_id):
    nav=NavBar.pages("");
    user_data=Users.get_one(user_id)
    user_comments=Users.get_comments_count(user_id)
    if user_data==None:
        return redirect('/error/missing-user')
    user_content=Articles.get_all_by_user_desc(user_id);
    # if "user_loggedon" in session:
    #    return redirect('/dashboard')
    return render_template("profile_page.html",nav=nav,user=user_data,user_content=user_content,comments=user_comments);

@app.route('/action/content/delete/<int:edit_id>')
def page_content_delete(edit_id):
    if "user_loggedon" not in session:
        return redirect('/user/login')
    content=Articles.get_one(edit_id);
    if content==None:
        return redirect('/error/missing-content')
    user=Users.get_userinfo(session['user_email'])
    if not content.author_id==user.id:
        return redirect('/error/block-action')
    Articles.delete(edit_id,user.id)
    if "delete_page" in session:
        if session['delete_page']=="dashboard":
            session['delete_page']=""
            return redirect('/user/dashboard')
    return redirect('/');

@app.route('/content/view/<int:view_id>')
def page_content_view(view_id):
    options=[]
    content=Articles.get_one(view_id);
    me=-1;
    if "user_loggedon" in session:
        user=Users.get_userinfo(session['user_email']);
        me=user.id;
        if content==None:
            return redirect('/error/missing-content')
        if user.id!=content.author.id:
            Articles.view_me(view_id)
            if Articles.is_liked(view_id,user.id):
                options.append(f"<a href=\"/action/rate/reset/{view_id}\">unlike</a>")
            else:
                options.append(f"<a href=\"/action/rate/like/{view_id}\">like</a>")
        else:
            options.append(f"<a href=\"/content/edit/{view_id}\">edit</a>")
            options.append(f"<a href=\"/action/content/delete/{view_id}\">delete</a>")
    else:
        me=-1
        Articles.view_me(view_id)
    edit={}
    
    edit={
        "route": f"/content/edit/{view_id}",
        "title": "Editing Content",
        "action": "Done",
        "digimon_ico": "img/floramon.gif",
        "digimon_name": "Floramon",
        "location_post": "/action/content/edit",
        "location_cancel": "/user/dashboard",
        "content_title": "",
        "content_desc": "",
        "content_body": ""
    }
    if "prev" in session:
        if session['prev']==True:
            session['prev']=False
            print("PREVIOUSLY ON BIG BABY")
            edit["content_body"]=session['prev_body']
    session['page']=edit["route"]
        
    
    session['edit_id']=view_id
    nav=NavBar.pages("");
    #body=content.body.split("\r\n")
    body=content.body.replace('\\n', '<br>')
    #print(body)
    comments=Comments.get_all(view_id)
    return render_template("view_content.html",content=content,nav=nav,edit=edit,body=body,options=options,comments=comments,user_id=me);

@app.route('/action/rate/like/<int:target_id>')
def action_rate_like(target_id):
    if "user_loggedon" not in session:
        return redirect('/user/login')
    content=Articles.get_one(target_id);
    if content==None:
        return redirect('/error/missing-content')
    user=Users.get_userinfo(session['user_email'])
    if content.author_id==user.id:
        return redirect('/error/block-action')
    Articles.like_me(target_id,user.id)
    return redirect(f"/content/view/{target_id}");
    
@app.route('/action/rate/reset/<int:target_id>')
def action_rate_reset(target_id):
    if "user_loggedon" not in session:
        return redirect('/user/login')
    content=Articles.get_one(target_id);
    if content==None:
        return redirect('/error/missing-content')
    user=Users.get_userinfo(session['user_email'])
    if content.author_id==user.id:
        return redirect('/error/block-action')
    Articles.reset_me(target_id,user.id)
    return redirect(f"/content/view/{target_id}");
    
@app.route('/action/comment/delete/<int:target_id>')
def action_comment_delete(target_id):
    if "user_loggedon" not in session:
        return redirect('/user/login')
    content=Articles.get_one(target_id);
    if content==None:
        return redirect('/error/missing-content')
    user=Users.get_userinfo(session['user_email'])
    
    Comments.delete(target_id,user.id)
    return redirect(f"/content/view/{session['edit_id']}");

# ==========================================================
# -------------------- [ERRORS] ----------------------------
# ==========================================================

@app.route('/error/missing-content')
def page_error_content():
     nav=NavBar.pages("")
     error_txt={
        "title": "Content Not Found",
        "desc": "This is not necessarily a 404 error per se; but the content doesn't actually exist here.",
        "digimon_ico": "img/floramon.gif",
        "digimon_name": "Floramon"
     }
     return render_template("error_message.html",nav=nav,error_txt=error_txt);

@app.route('/error/missing-user')
def page_error_user():
     nav=NavBar.pages("")
     error_txt={
        "title": "User Not Found",
        "desc": "This is not necessarily a 404 error per se; but there's no user at this slot.<br> But if you were really looking for nobody, you had offically succeeded!",
        "digimon_ico": "img/palmon.gif",
        "digimon_name": "Palmon"
     }
     return render_template("error_message.html",nav=nav,error_txt=error_txt);

@app.route('/error/block-action')
def page_error_block():
     nav=NavBar.pages("")
     error_txt={
        "title": "Denied Request",
        "desc": "I'm afraid I can't let you do that.",
        "digimon_ico": "img/mushmon.gif",
        "digimon_name": "Mushmon"
     }
     return render_template("error_message.html",nav=nav,error_txt=error_txt);

@app.errorhandler(404)
def page_404(e):
     nav=NavBar.pages("")
     error_txt={
        "title": "404 Not Found",
        "desc": "You know the drill, or something like that.",
        "digimon_ico": "img/piyomon.gif",
        "digimon_name": "Piyomon",
     }
     return render_template("error_message.html",nav=nav,error_txt=error_txt);