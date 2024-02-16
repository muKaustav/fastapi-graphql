import graphene
from models.tables import Author
from graphQL.Types import AuthorType
from sqlalchemy.orm import Session
from config.db import conn


class AuthorInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    verified = graphene.Int()


class CreateAuthor(graphene.Mutation):
    class Arguments:
        author_data = AuthorInput(required=True)

    author = graphene.Field(lambda: AuthorType)

    @staticmethod
    def mutate(self, info, author_data):
        try:
            with Session(bind=conn) as db:
                author = Author(**author_data)

                db.add(author)
                db.commit()
                db.refresh(author)

                return CreateAuthor(author=author)

        except Exception as e:
            return e


class UpdateAuthor(graphene.Mutation):
    class Arguments:
        author_id = graphene.Int(required=True)
        author_data = AuthorInput(required=True)

    author = graphene.Field(lambda: AuthorType)

    @staticmethod
    def mutate(self, info, author_id, author_data):
        try:
            with Session(bind=conn) as db:
                author = db.query(Author).get(author_id)

                if not author:
                    raise Exception(f"Author with ID {author_id} not found")

                for key, value in author_data.items():
                    setattr(author, key, value)

                db.commit()
                db.refresh(author)

                return UpdateAuthor(author=author)

        except Exception as e:
            return e


class DeleteAuthor(graphene.Mutation):
    class Arguments:
        author_id = graphene.Int(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(self, info, author_id):
        try:
            with Session(bind=conn) as db:
                author = db.query(Author).get(author_id)

                if not author:
                    raise Exception(f"Author with ID {author_id} not found")

                db.delete(author)
                db.commit()

                return DeleteAuthor(success=True)

        except Exception as e:
            return e
