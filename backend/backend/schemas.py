from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserPublic(BaseModel):
    email: EmailStr
    username: str


class Message(BaseModel):
    message: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class ReviewData(BaseModel):
    title: str
    text: str
    rating: int
    game: str


class GameData(BaseModel):
    name: str


class ReviewResponse(BaseModel):
    id: int
    title: str
    text: str
    rating: int
    game: str
    user_id: int

    class Config:
        orm_mode = True
