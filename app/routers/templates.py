from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import Template
from app.schemas import TemplateCreate, TemplateResponse

router = APIRouter(prefix="/templates", tags=["Templates"])

@router.post("", response_model=TemplateResponse, status_code=201)
async def create_template(data: TemplateCreate, db: AsyncSession = Depends(get_db)):
    new_template = Template(text=data.text)
    db.add(new_template)
    await db.commit()
    await db.refresh(new_template)
    return new_template

@router.get("", response_model=list[TemplateResponse])
async def list_templates(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Template))
    return result.scalars().all()