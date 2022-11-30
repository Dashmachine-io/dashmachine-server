import reverse_geocoder
from datetime import datetime, timedelta
from typing import Optional, Union, Dict, Any
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.core.utils import get_coord_distance
from app.crud.base import CRUDBase
from app.models.user import User, UserPronoun
from app.api.deps import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token")

    def get_by_phone(self, db: Session, phone: str) -> Optional[User]:
        return db.query(self.model).filter_by(phone=phone).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        # hash user password
        obj_in.password = self.get_password_hash(obj_in.password)

        # create user
        return super().create(db, obj_in=obj_in)

    def update(
        self,
        db: Session,
        *,
        db_obj: UserUpdate,
        obj_in: Union[UserUpdate, Dict[str, Any]],
    ) -> User:

        # hash user password if present
        if obj_in.password:
            obj_in.password = self.get_password_hash(obj_in.password)

        # combine first_name/last_name
        if obj_in.first_name:
            obj_in.first_name = obj_in.first_name.title()
            obj_in.last_name = obj_in.last_name.title()
            obj_in.name = f"{obj_in.first_name} {obj_in.last_name}"

        # pronouns
        if obj_in.pronouns:
            for db_pronoun in db_obj.pronouns:
                db.delete(db_pronoun)
            for pronoun in obj_in.pronouns:
                p = UserPronoun(name=pronoun.name, user_id=db_obj.id)
                db.add(p)
                db.commit()
            delattr(obj_in, "pronouns")

        # location
        if obj_in.location:
            obj_in.lng = obj_in.location[0]
            obj_in.lat = obj_in.location[1]
            if (
                not db_obj.location
                or get_coord_distance(
                    lng1=db_obj.lng, lat1=db_obj.lat, lng2=obj_in.lng, lat2=obj_in.lat
                )
                > 1.5
            ):
                loc = reverse_geocoder.search((obj_in.lat, obj_in.lng))[0]
                obj_in.city = loc["name"]
                obj_in.state = loc["admin1"]
            obj_in.location = None

        # update user
        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(
        self, db: Session, phone: str, password: str
    ) -> Optional[User]:
        db_user = self.get_by_phone(db, phone)
        if not db_user:
            return None
        if not self.verify_password(password, db_user.password):
            return None
        else:
            return db_user

    @staticmethod
    def create_access_token(phone: str) -> str:
        to_encode = {
            "sub": phone,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow()
            + timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS),
        }
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.HASH_ALGORITHM
        )
        return encoded_jwt

    async def get_current_user(
        self, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
    ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.HASH_ALGORITHM]
            )
            phone: str = payload.get("sub")
            if phone is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        db_user = self.get_by_phone(db, phone)
        if db_user is None:
            raise credentials_exception
        return db_user


user = CRUDUser(User)
