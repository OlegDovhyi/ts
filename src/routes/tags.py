from typing import List

from fastapi import APIRouter, Body, Form, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import ImageTagModel, ImageTagResponse
from src.repository import tags as repository_tags
from src.services.auth import auth_service

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/all tags/", response_model=List[ImageTagResponse])
async def read_tags(
    skip: int = 0,
    limit: int = 25,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    return await repository_tags.get_tags(skip, limit, db)


@router.get("/get tag by id/{tag_id}", response_model=ImageTagResponse)
async def read_tag(
    tag_id: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    tag = await repository_tags.get_tag_by_id(tag_id, db)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return tag


@router.post("/", response_model=List[ImageTagResponse])
async def create_tag(
    tags: List[ImageTagModel],
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    return await repository_tags.create_tag(tags, db)


@router.put("/{tag_id}", response_model=ImageTagResponse)
async def update_tag(
    body: ImageTagModel,
    tag_id: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    tag = await repository_tags.update_tag(tag_id, body, db)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return tag


@router.delete("/{tag_id}", response_model=ImageTagResponse)
async def remove_tag(
    tag_id: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    tag = await repository_tags.remove_tag(tag_id, db)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return tag
