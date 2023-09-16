from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from uuid import UUID
from src.app.services import hangout_service
from src.app import models, schemas
from src.database import get_db
from src.app.schemas import hangout
from src.app.models import User, Hangout, participants
from src.app.api.users import get_current_user

router = APIRouter()

@router.post("/hangouts/", response_model=hangout.Hangout)
async def create_new_hangout(hangout: hangout.HangoutCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await hangout_service.create_hangout(db=db, hangout=hangout, creator_id=current_user.id)

@router.get("/hangouts/", response_model=List[hangout.Hangout])
async def list_hangouts(skip: int = 0, limit: int = 100, _: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await hangout_service.get_all_hangouts(db, skip=skip, limit=limit)

# This function let a user join a hangout.
@router.post("/hangouts/{hangout_id}/join", response_model=hangout.Hangout)
async def join_hangout(hangout_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Hangout).where(Hangout.id == hangout_id))
    hangout = result.scalar_one_or_none()
    if not hangout:
        raise HTTPException(status_code=404, detail="Hangout not found")
    
    await db.execute(participants.insert().values(user_id=current_user.id, hangout_id=hangout.id, created_by=current_user.id, modified_by=current_user.id))
    await db.commit()
    
    return hangout

# This function return info about specific hangout.
@router.get("/hangouts/{hangout_id}/", response_model=hangout.HangoutDetails)
async def get_hangout_details(hangout_id: UUID, _: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    db_hangout = await hangout_service.get_hangout_details(db, hangout_id=hangout_id)
    if not db_hangout:
        raise HTTPException(status_code=404, detail="Hangout not found")
    return db_hangout
