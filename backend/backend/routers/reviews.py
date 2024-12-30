import logging
from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database import get_session
from backend.models import Review, User
from backend.schemas import ReviewData, ReviewResponse
from backend.security import get_current_user

router = APIRouter(prefix="/reviews", tags=["reviews"])
current_user = Annotated[User, Depends(get_current_user)]
sessions = Annotated[Session, Depends(get_session)]

# configure logging to write to a file
logging.basicConfig(
    level=logging.INFO, filename='app.log', filemode='a',
    format='%(asctime)s - %(name)s -%(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@router.post('/', response_model=ReviewResponse)
def create_review(
        info: ReviewData,
        user: current_user,
        session: sessions
    ):
    try:
        print(info)
        if info.text:
            new_review: Review = Review(
                text=info.text,
                title=info.title,
                game=info.game,
                rating=info.rating,
                user_id=user.id
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='invalid write',
            )
        session.add(new_review)
        session.commit()
        session.refresh(new_review)

        logger.info(f"Review created successfully: {new_review}")
        return new_review
    except Exception as e:
        logger.error(f"Error creating review: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail='An error occurred while creating the review.'
        )


@router.get('/', response_model=List[ReviewResponse])
def get_review(
        user: current_user,
        session: sessions
    ):
    try:
        reviews = session.scalars(select(Review).where(
            Review.user_id == user.id
        )).all()

        logger.info(
            f"Reviews retrieved successfully for user {user.id}: {reviews}"
        )
        return reviews
    except Exception as e:
        logger.error(f"Error retrieving reviews: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail='An error occurred while retrieving the reviews.'
        )
