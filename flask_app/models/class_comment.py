from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models.class_users import Users
from datetime import datetime
import math

class Comments:
    DB = "hearts_contents"
    def __init__(self,data):
        self.id = data['id']
        self.text = data['text']
        self.author_id= data['user_id']
        self.content_id= data['content_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.author=Users.get_one(self.author_id)
        self.when=self.time_span()
    
    @classmethod
    def get_all(cls,content_id):
        query = "SELECT * FROM comments WHERE content_id = %(id)s ORDER BY id DESC;"
        data={"id": content_id }
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
    def check_valid(cls,data):
        is_valid=True
        if not len(data['content_body'])>=3:
            is_valid=False
            flash("Comment needs to be 3 characters or more.","content_posting")
        if not len(data['content_body'])<=255:
            is_valid=False
            flash("Comment must be 255 characters max.","content_posting")
        return is_valid;
    
    @classmethod
    def save(cls,data,content_id,user_id):
        query="""INSERT INTO comments (text,content_id,user_id)
    		VALUES (%(text)s, %(content_id)s, %(author_id)s);"""
        insert={
            "text": data['content_body'],
            "content_id": content_id,
            "author_id": user_id
        }
        result = connectToMySQL(cls.DB).query_db(query,insert)
        return result;

    @classmethod
    def delete(cls,my_id,user_id):
        query  = "DELETE FROM comments WHERE id = %(id)s AND user_id = %(user_id)s;"
        data = {
            "id": my_id,
            "user_id": user_id
        }
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result;