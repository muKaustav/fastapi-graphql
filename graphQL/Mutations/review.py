import graphene
from models.tables import Author, Game, Review
from graphQL.Types import ReviewType
from sqlalchemy.orm import Session
from config.db import conn


class ReviewInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    content = graphene.String(required=True)
    rating = graphene.Int(required=True)
    game_id = graphene.Int(required=True)
    author_id = graphene.Int(required=True)


class CreateReview(graphene.Mutation):
    class Arguments:
        review_data = ReviewInput(required=True)

    review = graphene.Field(lambda: ReviewType)

    def mutate(self, info, review_data):
        try:
            with Session(bind=conn) as db:
                game_id = review_data.pop("game_id")
                author_id = review_data.pop("author_id")

                game = db.query(Game).get(game_id)
                author = db.query(Author).get(author_id)

                review = Review(**review_data, game_id=game.id, author_id=author.id)

                db.add(review)
                db.commit()
                db.refresh(review)

                return CreateReview(review=review)

        except Exception as e:
            return e


class UpdateReview(graphene.Mutation):
    class Arguments:
        review_id = graphene.Int(required=True)
        review_data = ReviewInput(required=True)

    review = graphene.Field(lambda: ReviewType)

    @staticmethod
    def mutate(self, info, review_id, review_data):
        try:
            with Session(bind=conn) as db:
                review = db.query(Review).get(review_id)

                if not review:
                    raise Exception(f"Review with ID {review_id} not found")

                for key, value in review_data.items():
                    setattr(review, key, value)

                db.commit()
                db.refresh(review)

                return UpdateReview(review=review)

        except Exception as e:
            return e


class DeleteReview(graphene.Mutation):
    class Arguments:
        review_id = graphene.Int(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(self, info, review_id):
        try:
            with Session(bind=conn) as db:
                review = db.query(Review).get(review_id)

                if not review:
                    raise Exception(f"Review with ID {review_id} not found")

                db.delete(review)
                db.commit()

                return DeleteReview(success=True)

        except Exception as e:
            return e
