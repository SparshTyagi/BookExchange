from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from models import Base, UserProfile, Book, ExchangeRequest, DiscussionPost
from database import db
from flask_login import login_user, current_user, logout_user, login_required

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
    user_profile = db.session.query(UserProfile).get(user_id)
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
    books = db.session.query(Book).all()
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
    exchange_request = db.session.query(ExchangeRequest).get(request_id)
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
    discussion_post = db.session.query(DiscussionPost).get(post_id)
    if discussion_post is None:
        return jsonify({'message': 'Discussion post not found'}), 404
    return jsonify({'user_id': discussion_post.user_id, 'book_id': discussion_post.book_id, 'content': discussion_post.content})

@routes.route('/search', methods=['GET'])
def search_books():
    search_query = request.args.get('q')
    books = db.session.query(Book).filter(Book.title.like(f'%{search_query}%')).all()
    return jsonify([{'id': book.id, 'title': book.title, 'author': book.author, 'description': book.description, 'genre': book.genre} for book in books])


@routes.route('/')
def main():
    return render_template('main.html')

@routes.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = db.session.query(UserProfile).filter_by(username=username).first()
    if user and user.password == password:
        login_user(user)
        return redirect(url_for('routes.index'))
    else:
        return render_template('main.html', error='Invalid username or password')


@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.main'))


@routes.route('/index')
def index():
    return render_template('index.html')

@routes.route('/books')
def books():
    books = db.session.query(Book).all()
    return render_template('books.html', books=books)

@routes.route('/search')
def search():
    return render_template('search.html')

@routes.route('/user_profiles')
def user_profiles():
    profiles = db.session.query(UserProfile).all()
    print(profiles)  # Add this line to print the profiles
    return render_template('user_profiles.html', profiles=profiles)

@routes.route('/create_profile', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':
        # Handle the form data and create a new user profile
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            error = 'Passwords do not match'
            return render_template('create_profile.html', error=error)

        if db.session.query(UserProfile).filter_by(username=username).first():
            error = 'Username already exists'
            return render_template('create_profile.html', error=error)

        if db.session.query(UserProfile).filter_by(email=email).first():
            error = 'Email already exists'
            return render_template('create_profile.html', error=error)

        user_profile = UserProfile(username=username, email=email, password=password)
        db.session.add(user_profile)
        db.session.commit()
        return redirect(url_for('routes.main'))
    else:
        return render_template('create_profile.html')

@routes.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        description = request.form['description']

        # Validate the form data
        if not title or not author or not genre or not description:
            error = 'All fields are required'
            return render_template('add_book.html', error=error)

        # Create a new Book object
        new_book = Book(title=title, author=author, genre=genre, description=description, user_id=current_user.id)
        # Add the new book to the database
        db.session.add(new_book)
        db.session.commit()

        # Redirect to the books page
        return redirect(url_for('routes.books'))
    return render_template('add_book.html')


@routes.route('/discussion_board', methods=['GET', 'POST'])
@login_required
def discussion_board():
    if request.method == 'POST':
        content = request.form['content']

        # Create a new DiscussionPost object
        discussion_post = DiscussionPost(content=content, user_id=current_user.id)

        # Add the new discussion post to the database
        db.session.add(discussion_post)
        db.session.commit()

        # Redirect to the discussion board page
        return redirect(url_for('routes.discussion_board'))
    else:
        discussion_posts = db.session.query(DiscussionPost).all()
        return render_template('discussion_board.html', discussion_posts=discussion_posts)