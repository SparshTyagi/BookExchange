from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from models import Base, UserProfile, Book, ExchangeRequest, DiscussionPost
from database import db

routes = Blueprint('routes', __name__)

@routes.route('/user_profiles', methods=['POST'])
def create_user_profile():
    data = request.get_json()
    user_profile = UserProfile(**data)
    db.session.add(user_profile)
    db.session.commit()
    return jsonify({'message': 'User profile created successfully'}), 201

@routes.route('/user_profiles/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    user_profile = UserProfile.query.get(user_id)
    if user_profile is None:
        return jsonify({'message': 'User profile not found'}), 404
    return jsonify({'username': user_profile.username, 'email': user_profile.email, 'book_collection': user_profile.book_collection, 'preferences': user_profile.preferences})

@routes.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    book = Book(**data)
    db.session.add(book)
    db.session.commit()
    return jsonify({'message': 'Book created successfully'}), 201

@routes.route('/books', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    return jsonify([{'id': book.id, 'title': book.title, 'author': book.author, 'description': book.description, 'genre': book.genre} for book in books])

@routes.route('/exchange_requests', methods=['POST'])
def create_exchange_request():
    data = request.get_json()
    exchange_request = ExchangeRequest(**data)
    db.session.add(exchange_request)
    db.session.commit()
    return jsonify({'message': 'Exchange request created successfully'}), 201

@routes.route('/exchange_requests/<int:request_id>', methods=['GET'])
def get_exchange_request(request_id):
    exchange_request = ExchangeRequest.query.get(request_id)
    if exchange_request is None:
        return jsonify({'message': 'Exchange request not found'}), 404
    return jsonify({'book_id': exchange_request.book_id, 'user_id': exchange_request.user_id, 'status': exchange_request.status})

@routes.route('/discussion_posts', methods=['POST'])
def create_discussion_post():
    data = request.get_json()
    discussion_post = DiscussionPost(**data)
    db.session.add(discussion_post)
    db.session.commit()
    return jsonify({'message': 'Discussion post created successfully'}), 201

@routes.route('/discussion_posts/<int:post_id>', methods=['GET'])
def get_discussion_post(post_id):
    discussion_post = DiscussionPost.query.get(post_id)
    if discussion_post is None:
        return jsonify({'message': 'Discussion post not found'}), 404
    return jsonify({'user_id': discussion_post.user_id, 'book_id': discussion_post.book_id, 'content': discussion_post.content})

@routes.route('/search', methods=['GET'])
def search_books():
    search_query = request.args.get('q')
    books = Book.query.filter(Book.title.like(f'%{search_query}%')).all()
    return jsonify([{'id': book.id, 'title': book.title, 'author': book.author, 'description': book.description, 'genre': book.genre} for book in books])

@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/books')
def books():
    books = Book.query.all()
    return render_template('books.html', books=books)

@routes.route('/user_profiles')
def user_profiles():
    user_profiles = UserProfile.query.all()
    return render_template('user_profiles.html', user_profiles=user_profiles)

@routes.route('/search')
def search():
    return render_template('search.html')

@routes.route('/create_profile', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':
        # Create a new user profile
        user_profile = UserProfile(username=request.form['username'], email=request.form['email'], password=request.form['password'])
        db.session.add(user_profile)
        db.session.commit()
        return redirect(url_for('routes.user_profiles'))
    return render_template('create_profile.html')