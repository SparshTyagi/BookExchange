from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from models import *
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
    return render_template('books.html', books=books)

@routes.route('/search', methods=['GET', 'POST'])
def search():
    search_query = ''
    search_results = []
    filter_by = ''
    if request.method == 'POST':
        search_query = request.form['search_query']
        filter_by = request.form['filter_by']
        if filter_by == 'book':
            books = db.session.query(Book).filter(Book.title.like(f'%{search_query}%') | Book.author.like(f'%{search_query}%')).all()
            search_results = books
        elif filter_by == 'user':
            users = db.session.query(UserProfile).filter(UserProfile.username.like(f'%{search_query}%')).all()
            search_results = users
            if len(search_results) <= 3:
                books_list = []
                for user in search_results:
                    user_books = db.session.query(Book).filter(Book.user_id == user.id).all()
                    books_list.append((user, user_books))
                return render_template('search.html', search_results=search_results, books_list=books_list, search_query=search_query, filter_by=filter_by)
    return render_template('search.html', search_results=search_results, search_query=search_query, filter_by=filter_by)

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
        review = request.form['review']
        rating = request.form.get('rating', None)

        # Validate the form data
        if not title or not author or not genre or not description:
            error = 'All fields are required'
            return render_template('add_book.html', error=error)

        # Create a new Book object
        new_book = Book(title=title, author=author, genre=genre, description=description, review=review, rating=rating, user_id=current_user.id)
        # Add the new book to the database
        db.session.add(new_book)
        db.session.commit()

        # Redirect to the books page
        return redirect(url_for('routes.books'))
    return render_template('add_book.html')


@routes.route('/discussion_board', methods=['GET', 'POST'])
def discussion_board():
    discussion_posts = db.session.query(DiscussionPost).order_by(DiscussionPost.created_at.desc()).all()
    error = None
    if request.method == 'POST':
        if current_user.is_authenticated:
            content = request.form['content'].strip()
            if content == '':
                error = 'Please enter a message before posting.'
            else:
                discussion_post = DiscussionPost(content=content, user_id=current_user.id)
                db.session.add(discussion_post)
                db.session.commit()
                return redirect(url_for('routes.discussion_board'))  # Redirect to the discussion board page
        else:
            error = 'You must be logged in to post to the discussion board.'
    return render_template('discussion_board.html', discussion_posts=discussion_posts, error=error)

@routes.route('/exchange_board', methods=['GET', 'POST'])
def exchange_board():
    exchange_posts = db.session.query(ExchangePost).order_by(ExchangePost.created_at.desc()).all()
    error = None
    if request.method == 'POST':
        if current_user.is_authenticated:
            offering = request.form['offering'].strip()
            looking_for = request.form['looking_for'].strip()
            if offering == "" or looking_for == "":
                error = 'Please enter both offering and looking for books.'
            else:
                exchange_post = ExchangePost(offering=offering, looking_for=looking_for, user_id=current_user.id)
                db.session.add(exchange_post)  # Corrected here
                db.session.commit()
                return redirect(url_for('routes.exchange_board'))
        else:
            error = 'Please login to post.'
    return render_template('exchange_board.html', exchange_posts=exchange_posts, error=error)