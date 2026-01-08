from fastapi import APIRouter, HTTPException
from dependencies import db_dep, requestform_dep
from schemas.schemas import UserRequest
from services.auth_se import register_user, login_user
from starlette import status

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(db: db_dep, user_request: UserRequest):
    return await register_user(db, user_request)
              
@router.post('/login')
async def login(db: db_dep, login_form: requestform_dep):
    return await login_user(db, login_form)