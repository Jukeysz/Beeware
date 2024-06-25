from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from backend.database import get_session
from backend.models import User
from backend.schemas import Message, UserPublic, UserSchema
from backend.security import get_current_user, get_password_hash

router = APIRouter(prefix="/users", tags=["users"])
sessions = Annotated[Session, Depends(get_session)]
current_user = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=UserPublic)
def create_user(session: sessions, info: UserSchema):
    user = session.scalar(
        select(User).where(
            or_(
                User.username == info.username,
                User.email == info.email
            )
        )
    )

    if user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Username or Email already exists",
        )

    new_user = User(
        username=info.username,
        email=info.email,
        password=get_password_hash(info.password)
    )

    session.add(new_user)
    session.commit()

    return new_user


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    session: sessions,
    user: current_user,
    info: UserSchema
):
    if user_id != user.id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='user not authorized',
        )

    user.username = info.username
    user.email = info.email
    user.password = get_password_hash(info.password)

    session.refresh(user)
    session.commit()

    return user


@router.delete('/{user_id}', response_model=Message)
def delete_user(user_id: int, session: sessions, user: current_user):
    if user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Invalid user id'
        )

    session.delete(user)
    session.commit()

    return {'message': 'User succesfully deleted'}
