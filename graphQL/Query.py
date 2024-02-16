import graphene
from graphQL.Types import AuthorType, GameType, ReviewType
from models.tables import Author, Game, Review
from sqlalchemy.orm import Session
from config.db import conn


class Query(graphene.ObjectType):
    authors = graphene.List(AuthorType)
    games = graphene.List(GameType)
    reviews = graphene.List(ReviewType)

    author = graphene.Field(AuthorType, id=graphene.ID(required=True))
    game = graphene.Field(GameType, id=graphene.ID(required=True))
    review = graphene.Field(ReviewType, id=graphene.ID(required=True))

    def resolve_authors(self, info):
        try:
            with Session(bind=conn) as db:
                authors = db.query(Author).all()

                return authors if authors else None

        except Exception as e:
            return e

    def resolve_games(self, info):
        try:
            with Session(bind=conn) as db:
                games = db.query(Game).all()

                return games if games else None

        except Exception as e:
            return e

    def resolve_reviews(self, info):
        try:
            with Session(bind=conn) as db:
                reviews = db.query(Review).all()

                return reviews if reviews else None

        except Exception as e:
            return e

    def resolve_game(self, info, id):
        try:
            with Session(bind=conn) as db:
                return db.query(Game).filter_by(id=id).first()

        except Exception as e:
            return None

    def resolve_author(self, info, id):
        try:
            with Session(bind=conn) as db:
                return db.query(Author).filter_by(id=id).first()

        except Exception as e:
            return None

    def resolve_review(self, info, id):
        try:
            with Session(bind=conn) as db:
                return db.query(Review).filter_by(id=id).first()

        except Exception as e:
            return None
