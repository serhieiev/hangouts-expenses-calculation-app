from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.app import models, utils
from src.app.schemas.user import UserResponse


# If you want to keep it synchronous
def get_user(db: AsyncSession, user_id: int):
    result = db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalars().first()


# Already async, just return the user directly
async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).filter_by(email=email))
    return result.scalars().first()


async def create_user(db: AsyncSession, user: models.User):
    print("create_user function called")
    hashed_password = utils.get_password_hash(user.password)
    db_user = models.User(
        email=user.email, password=hashed_password, avatar=user.avatar
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    print(db_user.id, db_user.created_at, db_user.modified_at)

    # Convert the database user object to your response model
    return UserResponse(
        id=db_user.id,
        email=db_user.email,
        avatar=db_user.avatar,
        created_at=db_user.created_at,
        modified_at=db_user.modified_at,
    )


async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user:
        return False
    if not utils.verify_password(password, user.hashed_password):
        return False
    return user
