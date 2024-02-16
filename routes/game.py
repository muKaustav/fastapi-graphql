from fastapi import APIRouter
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from config.db import conn
from models.tables import Game
from schemas.serializers import GameSchema

game = APIRouter()


@game.get("/")
async def get_games():
    try:
        with Session(bind=conn) as db:
            games = db.query(Game).all()

            result = [
                {
                    "id": game.id,
                    "name": game.name,
                    "platform": game.platform,
                }
                for game in games
            ]

            response = {"data": result, "message": "Games retrieved"}

            return JSONResponse(content=response, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@game.get("/{id}")
async def get_game(id: int):
    try:
        with Session(bind=conn) as db:
            game = db.query(Game).filter_by(id=id).first()

            if game:
                response = {
                    "data": {
                        "id": game.id,
                        "name": game.name,
                        "platform": game.platform,
                    },
                    "message": "Game retrieved",
                }

                return JSONResponse(content=response, status_code=200)

            return JSONResponse(content={"message": "Game not found"}, status_code=404)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@game.post("/")
async def create_game(game: GameSchema):
    try:
        with Session(bind=conn) as db:
            db.add(Game(name=game.name, platform=game.platform))
            db.commit()

            return JSONResponse(content={"message": "Game created"}, status_code=201)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
