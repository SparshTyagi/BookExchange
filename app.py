from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import Base, UserProfile, Book, ExchangeRequest, DiscussionPost
from routes import create_user_profile, get_user_profile, create_book, get_all_books, create_exchange_request, get_exchange_request, create_discussion_post, get_discussion_post

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///book_exchange.db"
db = SQLAlchemy(app)

@app.route('/user_profiles', methods=['POST'])
def create_user_profile():
    return create_user_profile()

@app.route('/user_profiles/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    return get_user_profile(user_id)

@app.route('/books', methods=['POST'])
def create_book():
    return create_book()

@app.route('/books', methods=['GET'])
def get_all_books():
    return get_all_books()

@app.route('/exchange_requests', methods=['POST'])
def create_exchange_request():
    return create_exchange_request()

@app.route('/exchange_requests/<int:request_id>', methods=['GET'])
def get_exchange_request(request_id):
    return get_exchange_request(request_id)

@app.route('/discussion_posts', methods=['POST'])
def create_discussion_post():
    return create_discussion_post()

@app.route('/discussion_posts/<int:post_id>', methods=['GET'])
def get_discussion_post(post_id):
    return get_discussion_post(post_id)

@app.route('/', methods=['GET'])
def index():
    return "Welcome to the Book Exchange Platform!"

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)