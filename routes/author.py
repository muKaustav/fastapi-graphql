from fastapi import APIRouter
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from config.db import conn
from models.tables import Author
from schemas.serializers import AuthorSchema

author = APIRouter()


@author.get("/")
async def get_authors():
    try:
        with Session(bind=conn) as db:
            authors = db.query(Author).all()

            result = [
                {
                    "id": author.id,
                    "name": author.name,
                    "verified": author.verified,
                }
                for author in authors
            ]

            response = {"data": result, "message": "Authors retrieved"}

            return JSONResponse(content=response, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@author.get("/{id}")
async def get_author(id: int):
    try:
        with Session(bind=conn) as db:
            author = db.query(Author).filter_by(id=id).first()

            if author:
                response = {
                    "data": {
                        "id": author.id,
                        "name": author.name,
                        "verified": author.verified,
                    },
                    "message": "Author retrieved",
                }

                return JSONResponse(content=response, status_code=200)

            return JSONResponse(
                content={"message": "Author not found"}, status_code=404
            )

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@author.post("/")
async def create_author(author: AuthorSchema):
    try:
        with Session(bind=conn) as db:
            db.add(Author(name=author.name, verified=author.verified))
            db.commit()

            return JSONResponse(content={"message": "Author created"}, status_code=201)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
