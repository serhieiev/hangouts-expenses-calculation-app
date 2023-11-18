from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select
from typing import List, Optional
from uuid import UUID
from src.app.models import Hangout, participants, User
from src.app.schemas.user import UserResponse
from src.app.schemas.hangout import HangoutCreate, HangoutDetails


async def create_hangout(
    db: AsyncSession, hangout: HangoutCreate, creator_id: UUID
) -> Hangout:
    new_hangout = Hangout(
        location=hangout.location,
        time=hangout.time,
        notes=hangout.notes,
        organizer_id=creator_id,
        created_by=creator_id,
        modified_by=creator_id,
    )
    db.add(new_hangout)
    await db.flush()  # Flush first to ensure new_hangout gets an ID without committing
    if hangout.participants:
        for participant_id in hangout.participants:
            await db.execute(
                participants.insert().values(
                    user_id=participant_id,
                    hangout_id=new_hangout.id,
                    created_by=creator_id,
                    modified_by=creator_id,
                )
            )
    await db.commit()
    await db.refresh(new_hangout)
    return new_hangout


async def get_all_hangouts(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[Hangout]:
    result = await db.execute(select(Hangout).offset(skip).limit(limit))
    return result.scalars().all()


async def get_hangout_details(
    db: AsyncSession, hangout_id: UUID
) -> Optional[HangoutDetails]:
    result = await db.execute(
        select(Hangout)
        .filter(Hangout.id == hangout_id)
        .options(joinedload(Hangout.users))
    )

    hangout = result.unique().scalar_one_or_none()

    if not hangout:
        return None

    organizer_result = await db.execute(
        select(User).filter(User.id == hangout.organizer_id)
    )
    organizer = organizer_result.scalar_one_or_none()

    # Convert ORM User objects to Pydantic UserResponse models manually
    participants_list = [
        UserResponse(
            id=user.id,
            email=user.email,
            avatar=user.avatar,
            created_at=user.created_at,
            modified_at=user.modified_at,
        )
        for user in hangout.users
    ]

    # Return the serialized HangoutDetails object
    return HangoutDetails(
        id=hangout.id,
        location=hangout.location,
        time=hangout.time,
        notes=hangout.notes,
        organizer=UserResponse(
            id=organizer.id,
            email=organizer.email,
            avatar=organizer.avatar,
            created_at=organizer.created_at,
            modified_at=organizer.modified_at,
        ),
        participants=participants_list,
    )
