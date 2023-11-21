import enum

from datetime import datetime, date

from sqlalchemy import Column, Integer, Text, String, Boolean, func, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from .db import Base



## ----Create ----#
photo_tags = Table(
    'photo_tags',
    Base.metadata,
    Column('photo_id', Integer, ForeignKey('photos.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)


class UserRole(Base):  #  Не змінювати!
    __tablename__ = "userroles"
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True, index=True)


class User(Base):  # Не змінювати!
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    role_id = Column('role_id', ForeignKey(
        'userroles.id', ondelete='CASCADE'), default=3)
   
    username = Column(String(50), nullable=False, unique=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
    ban = Column(Boolean, default=False)



class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    tag_name = Column(String(25), unique=True)
    photos = relationship("Photo", secondary=photo_tags, back_populates="tags")


class Photo(Base):
    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())

    user: Mapped[int] = relationship("User", backref="photos")
    tags: Mapped[list["Tag"]] = relationship("Tag", secondary=photo_tags, back_populates="photos")
    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="photo", cascade="all, delete-orphan"
    )


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[date] = mapped_column("created_at", DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column("updated_at", DateTime, default=func.now(), onupdate=func.now())
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    photo_id: Mapped[int] = mapped_column("photos_id", ForeignKey("photos.id", ondelete="CASCADE"), default=None)
    update_status: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped[int] = relationship("User", backref="comments")
    photo: Mapped["Photo"] = relationship("Photo", back_populates="comments")


class TransformPhotos(Base):
    __tablename__ = 'transform_photos'

    id = Column(Integer, primary_key=True)
    photo_url = Column(String, nullable=False)
    photo_id = Column(Integer, ForeignKey(Photo.id, ondelete="CASCADE"))
    created_at = Column('created_at', DateTime, default=func.now())

    photo = relationship('Photo', backref="transform_photos")