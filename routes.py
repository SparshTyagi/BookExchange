from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///book_exchange.db"
db = SQLAlchemy(app)

@app.route('/user_profiles', methods=['POST'])
def create_user_profile():
    data = request.get_json()
    user_profile = UserProfile(**data)
    db.session.add(user_profile)
    db.session.commit()
    return jsonify({'message': 'User profile created successfully'}), 201

@app.route('/user_profiles/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    user_profile = UserProfile.query.get(user_id)
    if user_profile is None:
        return jsonify({'message': 'User profile not found'}), 404
    return jsonify({'username': user_profile.username, 'email': user_profile.email, 'book_collection': user_profile.book_collection, 'preferences': user_profile.preferences})

@app.route('/user_profiles/<int:user_id>', methods=['PUT'])
def update_user_profile(user_id):
    user_profile = UserProfile.query.get(user_id)
    if user_profile is None:
        return jsonify({'message': 'User profile not found'}), 404
    data = request.get_json()
    for key, value in data.items():
        setattr(user_profile, key, value)
    db.session.commit()
    return jsonify({'message': 'User profile updated successfully'}), 200

@app.route('/user_profiles/<int:user_id>', methods=['DELETE'])
def delete_user_profile(user_id):
    user_profile = UserProfile.query.get(user_id)
    if user_profile is None:
        return jsonify({'message': 'User profile not found'}), 404
    db.session.delete(user_profile)
    db.session.commit()
    return jsonify({'message': 'User profile deleted successfully'}), 200

@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    book = Book(**data)
    db.session.add(book)
    db.session.commit()
    return jsonify({'message': 'Book created successfully'}), 201

@app.route('/books', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    return jsonify([{'id': book.id, 'title': book.title, 'author': book.author, 'description': book.description, 'genre': book.genre} for book in books])

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({'message': 'Book not found'}), 404
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author, 'description': book.description, 'genre': book.genre})

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({'message': 'Book not found'}), 404
    data = request.get_json()
    for key, value in data.items():
        setattr(book, key, value)
    db.session.commit()
    return jsonify({'message': 'Book updated successfully'}), 200

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({'message': 'Book not found'}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'}), 200

@app.route('/search', methods=['GET'])
def search_books():
    query = request.args.get('q')
    books = Book.query.filter(or_(Book.title.like('%' + query + '%'), Book.author.like('%' + query + '%'), Book.description.like('%' + query + '%'))).all()
    return jsonify([{'id': book.id, 'title': book.title, 'author': book.author, 'description': book.description, 'genre': book.genre} for book in books])

@app.route('/exchange_requests', methods=['POST'])
def create_exchange_request():
    data = request.get_json()
    exchange_request = ExchangeRequest(**data)
    db.session.add(exchange_request)
    db.session.commit()
    return jsonify({'message': 'Exchange request created successfully'}), 201

@app.route('/exchange_requests/<int:request_id>', methods=['GET'])
def get_exchange_request(request_id):
    exchange_request = ExchangeRequest.query.get(request_id)
    if exchange_request is None:
        return jsonify({'message': 'Exchange request not found'}), 404
    return jsonify({'id': exchange_request.id, 'book_id': exchange_request.book_id, 'user_id': exchange_request.user_id, 'status': exchange_request.status})

@app.route('/exchange_requests/<int:request_id>', methods=['PUT'])
def update_exchange_request(request_id):
    exchange_request = ExchangeRequest.query.get(request_id)
    if exchange_request is None:
        return jsonify({'message': 'Exchange request not found'}), 404
    data = request.get_json()
    for key, value in data.items():
        setattr(exchange_request, key, value)
    db.session.commit()
    return jsonify({'message': 'Exchange request updated successfully'}), 200

@app.route('/exchange_requests/<int:request_id>', methods=['DELETE'])
def delete_exchange_request(request_id):
    exchange_request = ExchangeRequest.query.get(request_id)
    if exchange_request is None:
        return jsonify({'message': 'Exchange request not found'}), 404
    db.session.delete(exchange_request)
    db.session.commit()
    return jsonify({'message': 'Exchange request deleted successfully'}), 200

@app.route('/discussion_posts', methods=['POST'])
def create_discussion_post():
    data = request.get_json()
    discussion_post = DiscussionPost(**data)
    db.session.add(discussion_post)
    db.session.commit()
    return jsonify({'message': 'Discussion post created successfully'}), 201

@app.route('/discussion_posts/<int:post_id>', methods=['GET'])
def get_discussion_post(post_id):
    discussion_post = DiscussionPost.query.get(post_id)
    if discussion_post is None:
        return jsonify({'message': 'Discussion post not found'}), 404
    return jsonify({'id': discussion_post.id, 'user_id': discussion_post.user_id, 'book_id': discussion_post.book_id, 'content': discussion_post.content})

@app.route('/discussion_posts/<int:post_id>', methods=['PUT'])
def update_discussion_post(post_id):
    discussion_post = DiscussionPost.query.get(post_id)
    if discussion_post is None:
        return jsonify({'message': 'Discussion post not found'}), 404
    data = request.get_json()
    for key, value in data.items():
        setattr(discussion_post, key, value)
    db.session.commit()
    return jsonify({'message': 'Discussion post updated successfully'}), 200

@app.route('/discussion_posts/<int:post_id>', methods=['DELETE'])
def delete_discussion_post(post_id):
    discussion_post = DiscussionPost.query.get(post_id)
    if discussion_post is None:
        return jsonify({'message': 'Discussion post not found'}), 404
    db.session.delete(discussion_post)
    db.session.commit()
    return jsonify({'message': 'Discussion post deleted successfully'}), 200