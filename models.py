from database import db

class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class UserProfile(Base):
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    book_collection = db.Column(db.Text, nullable=True)
    preferences = db.Column(db.Text, nullable=True)

class Book(Base):
    title = db.Column(db.String(128), nullable=False)
    author = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    genre = db.Column(db.String(64), nullable=True)

class ExchangeRequest(Base):
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    status = db.Column(db.String(64), nullable=False)

class DiscussionPost(Base):
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)