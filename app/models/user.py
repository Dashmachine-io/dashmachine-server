from sqlalchemy import (
    Column,
    Integer,
)

from app.database.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
