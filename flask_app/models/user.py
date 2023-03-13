from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    DB = "users_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = """SELECT * 
        FROM users;"""
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def save(cls, data ):
        query = """
                INSERT INTO 
                    users ( first_name , last_name , email , created_at, updated_at ) 
                VALUES 
                    ( %(first_name)s , %(last_name)s , %(email)s , NOW() , NOW() );
                """
        # session variable here
        # results = connectmysql.class()
        #session["variable_name"] = xxx.xxx
        return connectToMySQL(cls.DB).query_db( query, data )
    
    @classmethod
    def get_one(cls,data):
        query = """
                SELECT * 
                FROM users
                WHERE id = %(id)s; 
        """
        result = connectToMySQL(cls.DB).query_db( query, data )
        return cls(result[0])
    
    @classmethod
    def update(cls, data):
        query = """
                UPDATE users
                SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, updated_at=NOW()
                WHERE id = %(id)s;
        """
        return connectToMySQL(cls.DB).query_db( query, data )


    @classmethod
    def remove(cls, data):
        query = """
                DELETE FROM users
                WHERE id = %(id)s;
        """
        return connectToMySQL(cls.DB).query_db( query, data )
    
    # get user by email, in order to check if they exist, if so they can log in
    @classmethod
    def get_user_by_email(cls, data):

        query= '''
            SELECT * FROM users
            WHERE users.email = %(email)s;
        '''
        results= connectToMySQL(cls.DB).query_db(query, data)
        if results:
            one_user = cls(results[0])
            return one_user
        else:
            return False
    
    @staticmethod
    def validate_user(user):
        is_valid = True # we assume this is true
        data= { "email": user["email"]}
        valid_user = User.get_user_by_email(data)
        if len(user['first_name']) < 3:
            flash("First Name must be at least 3 characters.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last Name must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if valid_user:
            flash("Email already in use!", "register")
            is_valid=False
        return is_valid
