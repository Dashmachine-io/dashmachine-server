from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas, crud
from app.models.user import User
from app.api.deps import get_db

router = APIRouter()


@router.post("/create", response_model=schemas.Message)
def create_user(
    *, db: Session = Depends(get_db), user_in: schemas.user.UserCreate
) -> Any:
    """
    Create new users.
    """
    crud.user.create(db, obj_in=user_in)
    return {"message": "success"}


@router.post("/token", response_model=schemas.user.Token)
async def get_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Login user to get access token
    """
    phone = form_data.username
    user = crud.user.authenticate_user(db, phone, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = crud.user.create_access_token(phone)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/me",
    response_model=schemas.user.UserResponse,
)
def get_user(
    current_user: User = Depends(crud.user.get_current_user),
) -> Any:
    """
    Retrieve current user's data
    """
    return current_user


@router.post("/update", response_model=schemas.user.UserResponse)
def update_user(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(crud.user.get_current_user),
    user_in: schemas.user.UserUpdate,
) -> Any:
    """
    Update existing users.
    """
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user

