from sqlalchemy.orm import Session
from schemas.schemas import UserRequest
from models.users_model import Users
from core.security import hash_password, password_verify, create_access_token
from repositories.users_db import add_user_to_db, get_user
from core.exceptions import InvalidCredentialsError
from datetime import timedelta


async def register_user(db: Session, user: UserRequest):
    new_user = Users(
        email = user.email,
        username = user.username,
        hashed_password = hash_password(user.password),
        role = user.role
    )
    await add_user_to_db(db, new_user)
    token = await create_access_token(new_user, timedelta(minutes=20))
    return {
        'access_token': token,
        'token_type': 'bearer'
    }

async def login_user(db: Session, user):
    current_user = await get_user(db, user.username)
    if not current_user or not password_verify(user.password, current_user.hashed_password):
        raise InvalidCredentialsError
    token = await create_access_token(current_user, timedelta(minutes=20))
    return {
        'access_token': token,
        'token_type': 'bearer'
    }
