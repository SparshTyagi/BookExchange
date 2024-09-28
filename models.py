# models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    book_collection = Column(String, nullable=True)  # store book titles as a string
    preferences = Column(String, nullable=True)  # store book genres or preferences as a string

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    author = Column(String(50), nullable=False)
    description = Column(String, nullable=True)
    genre = Column(String(50), nullable=True)
    owner_id = Column(Integer, ForeignKey('user_profiles.id'))
    owner = relationship('UserProfile', backref='books')

class ExchangeRequest(Base):
    __tablename__ = 'exchange_requests'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    book = relationship('Book', backref='exchange_requests')
    user_id = Column(Integer, ForeignKey('user_profiles.id'))
    user = relationship('UserProfile', backref='exchange_requests')
    status = Column(String(50), nullable=False, default='pending')

class DiscussionPost(Base):
    __tablename__ = 'discussion_posts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profiles.id'))
    user = relationship('UserProfile', backref='discussion_posts')
    book_id = Column(Integer, ForeignKey('books.id'))
    book = relationship('Book', backref='discussion_posts')
    content = Column(String, nullable=False)