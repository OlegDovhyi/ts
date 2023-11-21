from typing import List

from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Photo, User
from src.repository.tags import create_tag
from src.schemas import ImageTagModel
from datetime import datetime

async def add_photo(
    description: str,
    tags: str,
    file: UploadFile,
    db: AsyncSession,
    current_user: User,
) -> Photo:

    photo = Photo(
        description=description,
        created_at=datetime.now(),
        user_id=current_user.id,
    )
    # Додаємо теги до фото
    if tags:
        result = []
        tags = tags.split(",")
        for tag in tags:
            tag.strip()
            current_tag = ImageTagModel(tag_name=tag)
            result.append(current_tag)
        photo.tags = await create_tag(result, db)

    db.add(photo)
    await db.flush()
    await db.refresh(photo)
    return photo


async def remove_photo(photo_id: int, current_user: User, db: AsyncSession) -> Photo:
    async with db.begin():
        photo = await db.execute(select(Photo).filter(Photo.id == photo_id, Photo.user_id == current_user.id))
        photo = photo.scalar_one_or_none()

        if not photo:
            return None

        await db.delete(photo)

    return photo


async def update_description(photo_id: int, body: Photo, current_user: User, db: AsyncSession) -> Photo:
    # Логіка для оновлення опису фото за ідентифікатором
    photo = await db.execute(select(Photo).filter(Photo.id == photo_id, Photo.user_id == current_user.id))
    photo = photo.scalar_one_or_none()

    if not photo:
        return None

    for key, value in body.dict().items():
        setattr(photo, key, value)

    await db.commit()
    await db.refresh(photo)
    return photo


async def see_photo(photo_id: int, current_user: User, db: AsyncSession) -> Photo:
    # Логіка для отримання фото за ідентифікатором
    photo = await db.execute(select(Photo).filter(Photo.id == photo_id))
    return photo.scalar_one_or_none()