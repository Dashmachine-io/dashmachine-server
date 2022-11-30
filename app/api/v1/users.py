from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas, crud
from app.core import recommendations
from app.models.user import User
from app.api.deps import get_db

router = APIRouter()


@router.get("/check_phone", response_model=schemas.user.CheckPhoneResponse)
def check_phone(
    phone: str,
    db: Session = Depends(get_db),
) -> Any:
    """
    Check if phone number is registered to user, returns 'login' or 'register'
    """
    user = crud.user.get_by_phone(db, phone)
    if user:
        return {"message": "login"}
    else:
        return {"message": "register"}


@router.post(
    "/create_sms_verification",
    response_model=schemas.user_verification_code.CodeCreateResponse,
)
def create_sms_verification(
    *, db: Session = Depends(get_db), obj_in: schemas.user_verification_code.CodeCreate
) -> Any:
    """
    Create SMS verification record for user by phone number.
    """
    crud.user_verification_code.create(db, obj_in=obj_in)
    return {"message": "sent"}


@router.post(
    "/verify_sms_verification",
    response_model=schemas.user_verification_code.CodeVerifyOut,
)
def create_sms_verification(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.user_verification_code.CodeVerifyIn,
) -> Any:
    """
    Check to see if verification matching phone and code exist
    """
    response = crud.user_verification_code.verify_code(db, obj_in=obj_in)
    return {"message": response}


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


@router.get(
    "/recommended",
    response_model=List[schemas.user.UserResponse],
)
def recommended(
    age_min: Optional[int] = Query(None),
    age_max: Optional[int] = Query(None),
    activities: Optional[List[int]] = Query(None),
    current_user: User = Depends(crud.user.get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Retrieve recommended list of users for the current user
    """
    return recommendations.users.get(
        db, current_user, age_max=age_max, age_min=age_min, activities=activities
    )
