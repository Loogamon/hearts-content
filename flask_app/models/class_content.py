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
        self.views=self.get_views_count(self.id)
        self.comments=self.get_comments_count(self.id)
        self.likes=self.get_likes_count(self.id)
    @classmethod
    def get_count(cls):
        count=0;
        query = "SELECT * FROM content;"
        results = connectToMySQL(cls.DB).query_db(query)
        for item in results:
            count+=1
        return count;
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM content ORDER BY id DESC;"
        results = connectToMySQL(cls.DB).query_db(query)
        items = []
        for item in results:
            items.append(cls(item))
        return items;
        
    @classmethod
    def get_all_by_like(cls):
        query = "SELECT * FROM content LEFT JOIN likes ON content.id = likes.user_id ORDER BY content.id DESC;"
        results = connectToMySQL(cls.DB).query_db(query)
        items = []
        #for item in results:
        #    items.append(cls(item))
        return items;

    @classmethod
    def get_all_by_user(cls,user_id):
        query = "SELECT * FROM content WHERE author_id=%(id)s;"
        data = { 'id': user_id}
        results = connectToMySQL(cls.DB).query_db(query,data)
        items = []
        for item in results:
            items.append(cls(item))
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