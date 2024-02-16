from pydantic import BaseModel


class AuthorSchema(BaseModel):
    name: str
    verified: int

    class Config:
        from_attributes = True


class GameSchema(BaseModel):
    name: str
    platform: str

    class Config:
        from_attributes = True


class ReviewSchema(BaseModel):
    title: str
    content: str
    rating: int
    game_id: int
    author_id: int

    class Config:
        from_attributes = True
