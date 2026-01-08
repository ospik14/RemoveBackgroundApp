from models.users_model import Users
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from core.exceptions import UserAlredyExistsError
from sqlalchemy.ext.asyncio import AsyncSession

async def add_user_to_db(db: AsyncSession, user: Users):
    try:
        db.add(user)       
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise UserAlredyExistsError

async def get_user(db: AsyncSession, email: str):
    query = select(Users).filter(Users.email == email)
    user = await db.execute(query)

    return user.scalars().first()