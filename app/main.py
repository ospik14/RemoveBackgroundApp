from fastapi import FastAPI, Request
from routers import images, auth
from fastapi.responses import FileResponse, JSONResponse
from core.exceptions import UserAlredyExistsError, InvalidCredentialsError, InvalidToken
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.database import engine, Base
from models.users_model import Users
from models.images_model import Images

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created (if not existed)")
    yield

app = FastAPI(lifespan=lifespan) 

app.include_router(router=images.router)
app.include_router(router=auth.router)

app.mount('/media', StaticFiles(directory='media'), name='media')
app.mount('/static', StaticFiles(directory='static'), name='static')

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.exception_handler(UserAlredyExistsError)
async def user_exists_handler(request: Request, exc: UserAlredyExistsError):
    return JSONResponse(
        status_code=409,
        content={'message': 'Conflict'}
    )

@app.exception_handler(InvalidCredentialsError)
async def invalid_credantials(request: Request, exc: InvalidCredentialsError):
    return JSONResponse(
        status_code=401,
        content={'message': 'WWW-Authenticate'}
    )

@app.exception_handler(InvalidToken)
async def invalid_token(request: Request, exc: InvalidToken):
    return JSONResponse(
        status_code=401,
        content={'message': 'Invalid token'}
    )