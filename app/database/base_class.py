import re
from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr

pattern = re.compile(r"(?<!^)(?=[A-Z])")


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(self) -> str:
        return pattern.sub("_", self.__name__).lower()
