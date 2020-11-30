import sqlite3
from flask_restful import Resource, reqparse


class User:
    TABLE_NAME = 'users'

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        select_query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(select_query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
            connection.close()
        return user

    @classmethod
    def find_by_id(cls, id):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        select_query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(select_query, (id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
            connection.close()
        return user


class UserRegister(Resource):
    TABLE_NAME = "users"
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()
        if User.find_by_username(data["username"]):
            return {"message": "A user with this username already exists in the database!"},400
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))
        connection.commit()
        connection.close()
        return {"message": f"user {data['username']} has been added to the database!"}
