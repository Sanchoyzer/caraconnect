from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app import __VERSION__
from app.routers import app_router
from app.settings import conf


app = FastAPI(
    title='API',
    version=__VERSION__,
    docs_url=conf.fastapi_docs_url(),
    openapi_url=conf.fastapi_openapi_url(),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(router=app_router)
