import os
import uuid
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import timedelta, timezone, datetime
from models.users_model import Users
from jose import jwt, JWTError
from core.exceptions import InvalidToken
from schemas.schemas import CurrentUser

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

bcrypt_context = CryptContext(schemes=['argon2'], deprecated='auto')
oauth_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')

def get_unique_name():
    return uuid.uuid4()

def hash_password(password: str) -> str:
    return bcrypt_context.hash(password)    

def password_verify(password: str, hashed_password: str):
    return bcrypt_context.verify(password, hashed_password)    

async def create_access_token(user: Users, expires_time: timedelta):
    encode = {'sub': user.username, 'user_id': user.id, 'role': user.role} 
    expires = datetime.now(timezone.utc) + expires_time
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('user_id')
        role: str = payload.get('role')

        if not role or not user_id or not username:
            raise InvalidToken
        
        return CurrentUser(username, user_id, role)
    except JWTError:
        raise InvalidToken