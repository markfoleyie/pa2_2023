from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_restful import Resource, Api, reqparse

from functools import wraps
from models import db, User
import json
import uuid


app = Flask(__name__)
app.config.from_pyfile("config.py", silent=True)
# jwt = JWTManager(app)
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)


def check_incoming_data(request):
    try:
        if request.get_json():
            incoming_data = request.get_json()
        else:
            incoming_data = request.data.decode(encoding="utf-8")
            incoming_data = json.dumps(incoming_data)

        return incoming_data
    except Exception as e:
        return False


def check_incoming_user(request):
    try:
        incoming_data = check_incoming_data(request)
        if not incoming_data:
            raise ValueError("Invalid data")

        if "username" not in incoming_data:
            raise ValueError("Missing username")

        if "password" not in incoming_data:
            raise ValueError("Missing password")

        return incoming_data
    except Exception as e:
        return False


# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'


class HelloWorld(Resource):
    def get(self):
        return {'greeting': 'Welcome to Week 10 Example 2'}


class Register(Resource):
    def post(self):
        try:
            incoming_data = check_incoming_user(request)
            if not incoming_data:
                raise ValueError("Invalid User data")

            plain_password = incoming_data.pop("password")
            hashed_password = User.create_password_hash(plain_password)
            if not hashed_password:
                raise ValueError("Password error")

            new_user = User(**incoming_data)
            new_user.password = hashed_password

            db.session.add(new_user)
            db.session.commit()

            return incoming_data, 201

        except Exception as e:
            return {"error": f"{e}"}, 400


api.add_resource(HelloWorld, "/")
api.add_resource(Register, "/register/")
# api.add_resource(Login, "/login/")
# api.add_resource(UserMe, "/user/me/")


if __name__ == '__main__':
    app.run()
