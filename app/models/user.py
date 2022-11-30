from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey,
    Boolean,
    Float,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app.database.base_class import Base
from .chat import chats_users
from .group import groups_users, groups_admins


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    name = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    birthday = Column(DateTime)
    bio = Column(Text)
    gender = Column(String)
    pronouns = relationship(
        "UserPronoun", back_populates="user", cascade="all, delete-orphan"
    )
    relationship_status = Column(String)
    sexuality = Column(String)
    ethnicity = Column(String)
    job_title = Column(String)

    gender_hidden = Column(Boolean, default=False)
    relationship_status_hidden = Column(Boolean, default=False)
    sexuality_hidden = Column(Boolean, default=False)
    ethnicity_hidden = Column(Boolean, default=False)
    job_title_hidden = Column(Boolean, default=False)
    pronouns_hidden = Column(Boolean, default=False)

    age_min = Column(Integer, default=18)
    age_max = Column(Integer, default=100)

    auto_detect_location = Column(Boolean, default=False)
    lat = Column(Float)
    lng = Column(Float)
    city = Column(String)
    state = Column(String)
    radius = Column(Integer, default=30)

    schedule_notes = Column(Text)
    schedule_mon = Column(String)
    schedule_tues = Column(String)
    schedule_wed = Column(String)
    schedule_thurs = Column(String)
    schedule_fri = Column(String)
    schedule_sat = Column(String)
    schedule_sun = Column(String)

    files = relationship("File", back_populates="user")
    activities = relationship(
        "Activity", back_populates="user", cascade="all, delete-orphan"
    )
    chats = relationship("Chat", secondary=chats_users, back_populates="users")
    chat_messages = relationship(
        "ChatMessage", back_populates="user", cascade="all, delete-orphan"
    )
    chat_message_reactions = relationship("ChatMessageReaction", back_populates="user")
    groups = relationship("Group", secondary=groups_users, back_populates="users")
    group_messages = relationship("GroupMessage", back_populates="user")
    group_message_reactions = relationship(
        "GroupMessageReaction", back_populates="user"
    )
    group_invites = relationship("GroupInvite", back_populates="user")
    admin_for = relationship("Group", secondary=groups_admins, back_populates="admins")
    group_events_created = relationship("GroupEvent", back_populates="creator")
    notifications = relationship("Notification", back_populates="user")

    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow)

    @hybrid_property
    def profile_complete(self):
        if not self.birthday or not self.phone or not self.username or not self.name:
            return False
        else:
            return True

    @hybrid_property
    def files_sorted(self):
        return sorted(
            [a for a in self.files],
            key=lambda x: x.sort_index,
        )

    @hybrid_property
    def main_image(self):
        return self.files[0] if len(self.files) > 0 else None

    @hybrid_property
    def location(self):
        return [self.lng, self.lat] if self.lng and self.lat else None


class UserPronoun(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="pronouns")
