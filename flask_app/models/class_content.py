from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models.class_users import Users
from datetime import datetime
import math

class Articles:
    DB = "hearts_contents"
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.body= data['body']
        self.author_id= data['author_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.author=Users.get_one(self.author_id)
        self.when=self.time_span()
        self.views=None
        self.comments=None
        self.likes=None
    @classmethod
    def get_count(cls):
        count=0;
        query = "SELECT * FROM content;"
        results = connectToMySQL(cls.DB).query_db(query)
        for item in results:
            count+=1
        return count;

    @classmethod
    def get_one(cls,my_id):
        query = "SELECT * FROM content WHERE id=%(id)s;"
        data={ "id": my_id }
        results = connectToMySQL(cls.DB).query_db(query,data)
        if (not len(results)):
            print("BAD DATA")
            return None;
        items = []
        for item in results:
            items.append(cls(item))
        i=0
        while i < len(items):
            items[i].views=cls.get_views_count(items[i].id)
            items[i].comments=cls.get_comments_count(items[i].id)
            items[i].likes=cls.get_likes_count(items[i].id)
            i+=1
        return items[0];
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM content ORDER BY id DESC;"
        results = connectToMySQL(cls.DB).query_db(query)
        items = []
        for item in results:
            items.append(cls(item))
        i=0
        while i < len(items):
            items[i].views=cls.get_views_count(items[i].id)
            items[i].comments=cls.get_comments_count(items[i].id)
            items[i].likes=cls.get_likes_count(items[i].id)
            i+=1
        return items;
        
    @classmethod
    def get_all_by_like(cls):
        #i thought of maybe doing it a clever query, but I realize I could just rearrange the results within the web server, MUCH easier that way I think
        query = "SELECT * FROM content ORDER BY id DESC;"
        results = connectToMySQL(cls.DB).query_db(query)
        items = []
        for item in results:
            items.append(cls(item))
        i=0
        items_cpy=[]
        while i < len(items):
            #items[i].views=cls.get_views_count(items[i].id)
            #items[i].comments=cls.get_comments_count(items[i].id)
            items[i].likes=cls.get_likes_count(items[i].id)
            if (items[i].likes>0):
                items_cpy.append(items[i])
            i+=1
        i=1
        while i < len(items_cpy):
            x=items_cpy[i]
            j=i-1
            while (j>=0) and (items_cpy[j].likes<x.likes):
                items_cpy[j+1]=items_cpy[j]
                j-=1
            items_cpy[j+1]=x
            i+=1
        return items_cpy;

    @classmethod
    def get_all_by_user(cls,user_id):
        query = "SELECT * FROM content WHERE author_id=%(id)s;"
        data = { 'id': user_id}
        results = connectToMySQL(cls.DB).query_db(query,data)
        items = []
        for item in results:
            items.append(cls(item))
        i=0
        while i < len(items):
            items[i].views=cls.get_views_count(items[i].id)
            items[i].comments=cls.get_comments_count(items[i].id)
            items[i].likes=cls.get_likes_count(items[i].id)
            i+=1
        return items;
        
    @classmethod
    def get_all_by_user_desc(cls,user_id):
        query = "SELECT * FROM content WHERE author_id=%(id)s ORDER BY id DESC;"
        data = { 'id': user_id}
        results = connectToMySQL(cls.DB).query_db(query,data)
        items = []
        for item in results:
            items.append(cls(item))
        i=0
        while i < len(items):
            items[i].views=cls.get_views_count(items[i].id)
            items[i].comments=cls.get_comments_count(items[i].id)
            items[i].likes=cls.get_likes_count(items[i].id)
            i+=1
        return items;
    
    def time_span(self):
        now = datetime.now()
        delta = now - self.created_at
        if delta.days > 0:
            return now.strftime("%B %d, %Y")
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hour(s) ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minute(s) ago"
        else:
            return f"{math.floor(delta.total_seconds())} second(s) ago"

    @classmethod
    def get_likes_count(cls,my_id):
        count=0;
        query = "SELECT * FROM likes WHERE content_id=%(id)s;"
        data = { 'id': my_id}
        results = connectToMySQL(cls.DB).query_db(query,data)
        for item in results:
            count+=1
        return count;
    
    @classmethod
    def get_comments_count(cls,my_id):
        count=0;
        query = "SELECT * FROM comments WHERE content_id=%(id)s;"
        data = { 'id': my_id}
        results = connectToMySQL(cls.DB).query_db(query,data)
        for item in results:
            count+=1
        return count;
    
    @classmethod
    def get_views_count(cls,my_id):
        count=0;
        query = "SELECT * FROM views WHERE content_id=%(id)s;"
        data = { 'id': my_id}
        results = connectToMySQL(cls.DB).query_db(query,data)
        for item in results:
            count+=1
        return count;
    
    @classmethod
    def check_valid(cls,data):
        is_valid=True
        if not len(data['content_title'])>=3:
            is_valid=False
            flash("Title needs to be 3 characters or more.","content_posting")
        if not len(data['content_title'])<=32:
            is_valid=False
            flash("Title must be 32 characters max.","content_posting")
        if not len(data['content_desc'])>=3:
            is_valid=False
            flash("Description needs to be 3 characters or more.","content_posting")
        if not len(data['content_desc'])<=150:
            is_valid=False
            flash("Title must be 150 characters max.","content_posting")
        if not len(data['content_body'])>=3:
            is_valid=False
            flash("Body needs to be 3 characters or more.","content_posting")
        return is_valid;
    
    @classmethod
    def save(cls,data,user_id):
        query="""INSERT INTO content (title,description,body,author_id)
    		VALUES (%(title)s,
            %(description)s,
            %(body)s,
            %(author_id)s);"""
        insert={
            "title": data['content_title'],
            "description": data['content_desc'],
            "body": data['content_body'],
            "author_id": user_id
        }
        result = connectToMySQL(cls.DB).query_db(query,insert)
        return result;
        
    @classmethod
    def update(cls,data,my_id,user_id):
        query="""UPDATE content
    	SET title=%(title)s,
            description=%(description)s,
            body=%(body)s,
            updated_at=NOW()
            WHERE id=%(id)s AND author_id=%(user_id)s;
            """
        insert={
            "title": data['content_title'],
            "description": data['content_desc'],
            "body": data['content_body'],
            "id":  my_id,
            "user_id": user_id
        }
        result = connectToMySQL(cls.DB).query_db(query,insert)
        return result;
    
    @classmethod
    def delete_all_likes(cls,my_id):
        query  = "DELETE FROM likes WHERE content_id = %(id)s;"
        data = {
            "id": my_id
        }
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result;
    
    @classmethod
    def delete_all_comments(cls,my_id):
        query  = "DELETE FROM comments WHERE content_id = %(id)s;"
        data = {
            "id": my_id
        }
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result; 
        
    @classmethod
    def delete_all_views(cls,my_id):
        query  = "DELETE FROM views WHERE content_id = %(id)s;"
        data = {
            "id": my_id
        }
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result; 
        
    @classmethod
    def delete(cls,my_id,user_id):
        cls.delete_all_likes(my_id)
        cls.delete_all_comments(my_id)
        cls.delete_all_views(my_id)
        query  = "DELETE FROM content WHERE id = %(id)s AND author_id = %(user_id)s;"
        data = {
            "id": my_id,
            "user_id": user_id
        }
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result;

    @classmethod
    def view_me(cls,content_id):
        query="""INSERT INTO views (content_id)
    		VALUES (%(id)s);"""
        insert={
            "id": content_id
        }
        result = connectToMySQL(cls.DB).query_db(query,insert)
        return result;

    @classmethod
    def is_liked(cls,content_id,user_id):
        query = "SELECT * FROM likes WHERE content_id = %(content_id)s AND user_id = %(user_id)s;"
        data={
            "content_id": content_id,
            "user_id": user_id
        }
        results = connectToMySQL(cls.DB).query_db(query,data)
        if len(results) >= 1:
            return True;
        return False;
        
    @classmethod
    def like_me(cls,content_id,user_id):
        query="""INSERT INTO likes (content_id,user_id)
    		VALUES (%(id)s,%(uid)s);"""
        insert={
            "id": content_id,
            "uid": user_id
        }
        result = connectToMySQL(cls.DB).query_db(query,insert)
        return result;
        
    @classmethod
    def reset_me(cls,content_id,user_id):
        query  = "DELETE FROM likes WHERE content_id = %(id)s AND user_id = %(uid)s;"
        insert={
            "id": content_id,
            "uid": user_id
        }
        result = connectToMySQL(cls.DB).query_db(query,insert)
        return result;