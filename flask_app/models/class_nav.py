from flask import session;
from flask_app.models.class_users import Users
from flask_app.models.class_content import Articles
# Not actually a model, but probably necessary.
class NavBar:
    nav_items=[]
    current=""
    def __init__(self):
        pass
    @classmethod
    def pages(cls,current_pg):
        cls.current=current_pg
        cls.nav_items=[]
        cls.add("Home","/")
        if Articles.get_count():
            cls.add("Random","/content/random")
        if "user_loggedon" in session:
            cls.add("Dashboard","/user/dashboard")
            cls.add("Add New","/content/add")
        
        if "user_loggedon" in session:
            user=Users.get_userinfo(session['user_email'])
            name=user.first_name+" "+user.last_name
            cls.add_ext("Login","/user/logout","Logout ("+name+")")
        else:
            cls.add_ext("Login","/user/login","Login")
        #print(cls.nav_items)
        return cls.nav_items
    @classmethod
    def add(cls,page,url):
        return cls.add_ext(page,url,"");
    @classmethod
    def add_ext(cls,page,url,alt):
        li=""
        select=False
        li="<li"
        li+=" onclick=\"window.location.href = '"+url+"'\""
        if cls.current==page:
            li+=" class=\"header-selected\">"
        else:
            li+=">"
        li+="<a href=\""+url+"\">"
        if alt!="":
            li+=alt
        else:
            li+=page
        li+="</a>"
        li+="</li>"
        cls.nav_items.append(li)
    