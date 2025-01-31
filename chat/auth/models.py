import reflex as rx
from datetime import datetime
from reflex_local_auth.user import LocalUser

import sqlalchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlmodel import SQLModel, Field, Relationship, Table
from typing import Optional, List
from datetime import datetime, timezone

def my_time() -> datetime:
    return datetime.now(timezone.utc)

post_members = Table(
    "post_members",
    SQLModel.metadata,  # Use SQLModel's metadata
    Column("userinfo_id", Integer, ForeignKey("userinfo.id"), primary_key=True),
    Column("post_id", Integer, ForeignKey("postmodel.id"), primary_key=True)
)

class UserInfo(rx.Model, table=True):
    """ Model for user information """
    email: str
    user_id: int = Field(foreign_key='localuser.id')
    user: LocalUser | None = Relationship() 
    profile_photo: Optional[bytes] = Field(default=None)
    posts: List['PostModel'] = Relationship(
        back_populates="userinfo"
    )
    joined_posts: List['PostModel'] = Relationship(
        back_populates="members",
        sa_relationship_kwargs={"secondary": post_members}
    )
    created_at: datetime = Field(
        default_factory=my_time,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'server_default': sqlalchemy.func.now()
        },
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=my_time,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'onupdate': sqlalchemy.func.now(),
            'server_default': sqlalchemy.func.now()
        },
        nullable=False
    )

class PostModel(rx.Model, table=True):
    """ Model for posts about missing/found people, pets or items. """
    userinfo_id: int = Field(default=None, foreign_key="userinfo.id")
    userinfo: Optional['UserInfo'] = Relationship(back_populates="posts")
    title: str
    content: str
    category: str # "missing_person", "found_item", "lost_pet" ...
    members: List['UserInfo'] = Relationship(
        back_populates='joined_posts',
        sa_relationship_kwargs={"secondary": post_members}
    )
    created_at: datetime = Field(
        default_factory=my_time,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={'server_default': sqlalchemy.func.now()},
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=my_time,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={'onupdate': sqlalchemy.func.now(), 'server_default': sqlalchemy.func.now()},
        nullable=False
    )
    publish_active: bool = False
    publish_date: datetime = Field(
        default=None,
        sa_type=sqlalchemy.DateTime(timezone=True),
        nullable=True
    )
