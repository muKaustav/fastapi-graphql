from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from config.db import engine

Base = declarative_base()


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(100))
    verified = Column(Integer, default=0)


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(100))
    platform = Column(String(100))


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    title = Column(String(100))
    content = Column(String(1000))
    rating = Column(Integer)
    game_id = Column(Integer, ForeignKey("games.id"))
    author_id = Column(Integer, ForeignKey("authors.id"))


Base.metadata.create_all(engine)
