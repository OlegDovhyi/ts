from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Tag
from src.schemas import ImageTagModel


async def get_tags(skip: int, limit: int, db: AsyncSession) -> List[Tag]:
    return (await db.execute(select(Tag).offset(skip).limit(limit))).scalars().all()

async def get_tag_by_id(tag_id: int, db: AsyncSession) -> Tag:
    return (await db.execute(select(Tag).filter(Tag.id == tag_id))).scalar()

async def get_tags_by_list_values(
    values: List[ImageTagModel], db: AsyncSession
) -> List[Tag]:
    return (
        await db.execute(select(Tag).filter(Tag.tag_name.in_([value.tag_name for value in values])))
    ).scalars().all()

async def create_tag(values: List[ImageTagModel], db: AsyncSession) -> Tag:
    bd_tags = await get_tags_by_list_values(values, db)
    for value in values:
        if not any([tag.tag_name == value.tag_name for tag in bd_tags]):
            new_tag = Tag(tag_name=value.tag_name)
            db.add(new_tag)
            await db.commit()
    return await get_tags_by_list_values(values, db)

async def update_tag(tag_id: int, body: ImageTagModel, db: AsyncSession) -> Tag | None:
    tag = await get_tag_by_id(tag_id, db)
    if tag:
        tag.tag_name = body.tag_name
        await db.commit()
        await db.refresh(tag)
    return tag

async def remove_tag(tag_id: int, db: AsyncSession) -> Tag | None:
    tag = await get_tag_by_id(tag_id, db)
    if tag:
        db.delete(tag)
        await db.commit()
    return tag
