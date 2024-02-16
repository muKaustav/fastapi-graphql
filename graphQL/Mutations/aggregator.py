import graphene
from .author import CreateAuthor, UpdateAuthor, DeleteAuthor
from .game import CreateGame, UpdateGame, DeleteGame
from .review import CreateReview, UpdateReview, DeleteReview


class Mutation(graphene.ObjectType):
    create_author = CreateAuthor.Field()
    update_author = UpdateAuthor.Field()
    delete_author = DeleteAuthor.Field()

    create_game = CreateGame.Field()
    update_game = UpdateGame.Field()
    delete_game = DeleteGame.Field()

    create_review = CreateReview.Field()
    update_review = UpdateReview.Field()
    delete_review = DeleteReview.Field()
