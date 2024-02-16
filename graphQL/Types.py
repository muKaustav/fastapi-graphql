import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models.tables import Author, Game, Review
from sqlalchemy.orm import Session
from config.db import conn


class AuthorType(SQLAlchemyObjectType):
    class Meta:
        model = Author


class GameType(SQLAlchemyObjectType):
    class Meta:
        model = Game

    reviews = graphene.List(lambda: ReviewType)

    def resolve_reviews(self, info):
        try:
            with Session(bind=conn) as db:
                return db.query(Review).filter_by(game_id=self.id).all()

        except Exception as e:
            return None


class ReviewType(SQLAlchemyObjectType):
    class Meta:
        model = Review

    author = graphene.Field(AuthorType)
    game = graphene.Field(GameType)

    def resolve_author(self, info):
        try:
            with Session(bind=conn) as db:
                return db.query(Author).get(self.author_id)

        except Exception as e:
            return None

    def resolve_game(self, info):
        try:
            with Session(bind=conn) as db:
                return db.query(Game).get(self.game_id)

        except Exception as e:
            return None
