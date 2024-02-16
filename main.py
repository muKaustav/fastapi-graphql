from fastapi import FastAPI
import graphene
from starlette_graphene3 import GraphQLApp, make_graphiql_handler
from graphQL.Query import Query
from graphQL.Mutations.aggregator import Mutation
from routes.author import author
from routes.game import game
from routes.review import review

app = FastAPI()

# GraphQL endpoint
app.mount(
    "/graphql",
    GraphQLApp(
        graphene.Schema(query=Query, mutation=Mutation), on_get=make_graphiql_handler()
    ),
)

# REST endpoints
app.include_router(author, prefix="/author", tags=["author"])
app.include_router(game, prefix="/game", tags=["game"])
app.include_router(review, prefix="/review", tags=["review"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
