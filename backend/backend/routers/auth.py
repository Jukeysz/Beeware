from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database import get_session
from backend.models import User
from backend.schemas import Message
from backend.security import create_token, get_current_user, verify_password

router = APIRouter(prefix='/auth', tags=['auth'])
sessions = Annotated[Session, Depends(get_session)]
form = Annotated[OAuth2PasswordRequestForm, Depends()]
user = Annotated[User, Depends(get_current_user)]


@router.post('/token', response_model=Message)
def login_token(
    session: sessions,
    formdata: form,
    response: Response
):
    user = session.scalar(select(User).where(
        User.email == formdata.username
    ))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    if not verify_password(formdata.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    token = create_token(data={'sub': user.email})

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
    )
    return {'message': 'login successful'}


@router.post('/refresh_token', response_model=Message)
def refresh_token(user: user, response: Response):
    token = create_token(data={'sub': user.email})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
    )

    return {'message': 'token refreshed'}


@router.get("/verify")
def verify_token(
        usr: user
    ):
    return {"authenticated": True, "email": usr.email}
