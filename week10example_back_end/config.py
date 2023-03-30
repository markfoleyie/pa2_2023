import os
from datetime import timedelta

SECRET_KEY = os.urandom(16)
SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://docker:docker@localhost:25432/week10example2"
SQLALCHEMY_TRACK_MODIFICATIONS = True
# JWT_SECRET_KEY = os.urandom(16)
# JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
# JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
