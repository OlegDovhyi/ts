from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.database.models import User, Photo, Tag
from src.services.auth import auth_service
import src.repository.photo as repository_photo
from src.conf.config import settings
from src.schemas import PhotoModels, PhotoBase

router = APIRouter(prefix='/photos', tags=["photos"])

# ...

@router.post(
    "/new/", response_model=PhotoModels, status_code=status.HTTP_201_CREATED
)
async def create_photo(
    description: str = Form(),
    tags: str = Form(None),
    file: UploadFile = File(),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    
    return await repository_photo.add_photo(
        description, tags, file, db, current_user
    )




@router.delete("/{photo_id}", response_model=PhotoModels)
async def delete_photo(
    photo_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return await repository_photo.remove_photo(photo_id, current_user, db)

@router.put("/{photo_id}", response_model=PhotoModels)
async def put_description(
    body: PhotoBase,
    photo_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return await repository_photo.update_description(photo_id, body, current_user, db)

@router.get("/{photo_id}", response_model=PhotoModels)
async def get_photo(
    photo_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return await repository_photo.see_photo(photo_id, current_user, db)
