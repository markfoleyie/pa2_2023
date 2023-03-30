from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_restful import Resource, Api, reqparse

from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from functools import wraps
from models import db, User
import json
import uuid


app = Flask(__name__)
app.config.from_pyfile("config.py", silent=True)
jwt = JWTManager(app)
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)


# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason.
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


# Here is a custom decorator that verifies the JWT is present in the request,
# as well as insuring that the JWT has a claim indicating that this user is
# an administrator
def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims["is_admin"]:
                return fn(*args, **kwargs)
            else:
                return jsonify(message="Admins only!"), 403

        return decorator

    return wrapper


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


class Login(Resource):
    def post(self):
        try:
            incoming_data = check_incoming_user(request)
            if not incoming_data:
                raise ValueError("Invalid User data")

            user = db.session.query(User).filter_by(username=incoming_data["username"]).one_or_none()
            if not user:
                raise ValueError("Couldn't get user from database")

            if not user.password_is_verified(incoming_data['password']):
                raise ValueError("Invalid password")

            access_token = create_access_token(
                identity=user,
                additional_claims={"is_admin": user.is_admin}
            )
            # access_token = create_access_token(identity=user)
            refresh_token = create_refresh_token(identity=user)
            # return {"user": user.as_dict_short, "access_token": access_token}, 200
            return {"refresh": refresh_token, "access": access_token}, 200

        except Exception as e:
            return {"error": f"{e}"}, 400


class UserMe(Resource):
    @jwt_required()
    def get(self):
        try:
            return current_user.as_dict_short, 200
        except Exception as e:
            return {"error": f"{e}"}, 400


api.add_resource(HelloWorld, "/")
api.add_resource(Register, "/register/")
api.add_resource(Login, "/login/")
api.add_resource(UserMe, "/user/me/")


if __name__ == '__main__':
    app.run()
