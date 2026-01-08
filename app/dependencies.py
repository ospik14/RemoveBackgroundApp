from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from core.database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.schemas import CurrentUser
from core.security import oauth_bearer, decode_token


async def get_db():
    async with AsyncSessionLocal() as db_session:
        yield db_session

def get_current_user(token: Annotated[str, Depends(oauth_bearer)]):
    return decode_token(token)

user_dep = Annotated[CurrentUser, Depends(get_current_user)]
db_dep = Annotated[AsyncSession, Depends(get_db)]
requestform_dep = Annotated[OAuth2PasswordRequestForm, Depends()]