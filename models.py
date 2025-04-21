from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    username = Column(String(50), unique=True)
    email = Column(String(100))
    password = Column(String(100))
    role = Column(String(10))
    created_at = Column(DateTime, default=func.now())

    books = relationship("Book", back_populates="user")
    movies = relationship("Movie", back_populates="user")
    board_games = relationship("BoardGame", back_populates="user")
    comics = relationship("Comic", back_populates="user")

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=True)
    author = Column(String(50))
    genre = Column(String(50))
    published_date = Column(String(10))
    rating = Column(Integer)
    created_at = Column(DateTime, default=func.now())

    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="books")

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    director = Column(String(50))
    genre = Column(String(50))
    release_date = Column(String(10))
    rating = Column(Integer)
    created_at = Column(DateTime, default=func.now())

    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="movies")

class BoardGame(Base):
    __tablename__ = 'board_games'

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    designer = Column(String(50))
    genre = Column(String(50))
    release_date = Column(String(10))
    created_at = Column(DateTime, default=func.now())

    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="board_games")

class Comic(Base):
    __tablename__ = 'comics'

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    author = Column(String(50))
    genre = Column(String(50))
    published_date = Column(String(10))
    created_at = Column(DateTime, default=func.now())

    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="comics")