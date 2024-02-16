from fastapi import APIRouter
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from config.db import conn
from models.tables import Review
from schemas.serializers import ReviewSchema

review = APIRouter()


@review.get("/")
async def get_reviews():
    try:
        with Session(bind=conn) as db:
            reviews = db.query(Review).all()

            result = [
                {
                    "id": review.id,
                    "title": review.title,
                    "content": review.content,
                    "rating": review.rating,
                    "game_id": review.game_id,
                    "author_id": review.author_id,
                }
                for review in reviews
            ]

            response = {"data": result, "message": "Reviews retrieved"}

            return JSONResponse(content=response, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@review.get("/{id}")
async def get_review(id: int):
    try:
        with Session(bind=conn) as db:
            review = db.query(Review).filter_by(id=id).first()

            if review:
                response = {
                    "data": {
                        "id": review.id,
                        "title": review.title,
                        "content": review.content,
                        "rating": review.rating,
                        "game_id": review.game_id,
                        "author_id": review.author_id,
                    },
                    "message": "Review retrieved",
                }

                return JSONResponse(content=response, status_code=200)

            return JSONResponse(
                content={"message": "Review not found"}, status_code=404
            )

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@review.post("/")
async def create_review(review: ReviewSchema):
    try:
        with Session(bind=conn) as db:
            db.add(
                Review(
                    title=review.title,
                    content=review.content,
                    rating=review.rating,
                    game_id=review.game_id,
                    author_id=review.author_id,
                )
            )

            db.commit()

            return JSONResponse(content={"message": "Review created"}, status_code=201)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
