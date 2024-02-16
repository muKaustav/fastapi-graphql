import graphene
from models.tables import Game
from graphQL.Types import GameType
from sqlalchemy.orm import Session
from config.db import conn


class GameInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    platform = graphene.String(required=True)


class CreateGame(graphene.Mutation):
    class Arguments:
        game_data = GameInput(required=True)

    game = graphene.Field(lambda: GameType)

    def mutate(self, info, game_data):
        try:
            with Session(bind=conn) as db:
                game = Game(**game_data)

                db.add(game)
                db.commit()
                db.refresh(game)

                return CreateGame(game=game)

        except Exception as e:
            return e


class UpdateGame(graphene.Mutation):
    class Arguments:
        game_id = graphene.Int(required=True)
        game_data = GameInput(required=True)

    game = graphene.Field(lambda: GameType)

    @staticmethod
    def mutate(self, info, game_id, game_data):
        try:
            with Session(bind=conn) as db:
                game = db.query(Game).get(game_id)

                if not game:
                    raise Exception(f"Game with ID {game_id} not found")

                for key, value in game_data.items():
                    setattr(game, key, value)

                db.commit()
                db.refresh(game)

                return UpdateGame(game=game)

        except Exception as e:
            return e


class DeleteGame(graphene.Mutation):
    class Arguments:
        game_id = graphene.Int(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(self, info, game_id):
        try:
            with Session(bind=conn) as db:
                game = db.query(Game).get(game_id)

                if not game:
                    raise Exception(f"Game with ID {game_id} not found")

                db.delete(game)
                db.commit()

                return DeleteGame(success=True)

        except Exception as e:
            return DeleteGame(success=False)
