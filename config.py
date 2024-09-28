import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'book_exchange.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "my_secret_key_1234567890"
