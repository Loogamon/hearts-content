from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class Users:
    DB = "hearts_contents"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email= data['email']
        self.password= data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.DB).query_db(query)
        items = []
        for item in results:
            items.append(cls(item))
        return items;
    @classmethod
    def get_one(cls,my_id):
        query = "SELECT * FROM users WHERE id=%(id)s;"
        data = { 'id': my_id}
        results = connectToMySQL(cls.DB).query_db(query,data)
        return cls(results[0]);
    @classmethod
    def get_userinfo(cls,email):
        query = query = "SELECT * FROM users WHERE email = %(email)s;"
        data = { 'email': email}
        results = connectToMySQL(cls.DB).query_db(query,data)
        return cls(results[0]);
    @classmethod
    def save(cls,data):
        query="""INSERT INTO users (first_name,last_name,email,password)
    		VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result;
    @classmethod
    def check_valid_signup(cls,data):
        is_valid=True
        if not len(data['signup_fname'])>=3:
            flash("First Name needs to be 3 or more characters.","signup")
            is_valid=False
        if not len(data['signup_lname'])>=3:
            flash("Last Name needs to be 3 or more characters.","signup")
            is_valid=False 
        if not EMAIL_REGEX.match(data['signup_email']):
            flash("Email is not valid.","signup")
            is_valid = False
        else:
            query = "SELECT * FROM users WHERE email = %(signup_email)s;"
            results = connectToMySQL(cls.DB).query_db(query,data)
            if len(results) >= 1:
                flash(f"{data['signup_email']} is already taken.","signup")
                is_valid = False
        if not len(data['signup_email'])>=3:
            flash("Email needs to be 3 or more characters.","signup")
            is_valid=False
            
        if not len(data['signup_password1'])>=8:
            flash("Password needs to be 8 or more characters.","signup")
            is_valid=False
        if not len(data['signup_password2'])>=8:
            flash("Confirm Password needs to be 8 or more characters.","signup")
            is_valid=False
        if data['signup_password1']!=data['signup_password2']:
            flash("Passwords do not match!","signup")
            is_valid=False
        return is_valid;
    @classmethod
    def check_valid_login(cls,data):
        is_valid=False
        if not EMAIL_REGEX.match(data['email']):
            flash("Email is not valid.","login")
            is_valid = False
        else:
            query = "SELECT * FROM users WHERE email = %(email)s;"
            results = connectToMySQL(cls.DB).query_db(query,data)
            if len(results) >= 1:
                print("FOUND!")
                password_hash=results[0]['password']
                print(password_hash)
                if bcrypt.check_password_hash(password_hash, data['password']):
                    is_valid = True
                else:
                    flash("Password is not correct.","login")
            else:
                flash("User doesn't exist.","login")
                is_valid = False
        return is_valid;