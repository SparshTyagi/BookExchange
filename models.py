from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import DateTime
from flask_login import UserMixin
from datetime import datetime


Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    author = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    genre = Column(String(50), nullable=True)
    user_id = Column(Integer, ForeignKey('user_profiles.id'))
    user = relationship("UserProfile", backref="books")

    def __repr__(self):
        return f"Book('{self.title}', '{self.author}')"

class UserProfile(Base, UserMixin):
    __tablename__ = 'user_profiles'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    book_collection = Column(String(100), nullable=True)
    preferences = Column(String(100), nullable=True)

    def __repr__(self):
        return f"UserProfile('{self.username}', '{self.email}')"

class ExchangeRequest(Base):
    __tablename__ = 'exchange_requests'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    user_id = Column(Integer, ForeignKey('user_profiles.id'))
    status = Column(String(50), nullable=True)

    def __repr__(self):
        return f"ExchangeRequest('{self.book_id}', '{self.user_id}')"

class DiscussionPost(Base):
    __tablename__ = 'discussion_posts'
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user_profiles.id'))
    user = relationship("UserProfile", backref="discussion_posts")
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"DiscussionPost('{self.content}')"