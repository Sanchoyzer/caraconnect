from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app import __VERSION__
from app.routers import app_router
from app.settings import conf


def get_app(*, testing: bool = False) -> FastAPI:  # noqa: ARG001
    app_ = FastAPI(
        title='API',
        version=__VERSION__,
        docs_url=conf.fastapi_docs_url(),
        openapi_url=conf.fastapi_openapi_url(),
    )

    app_.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app_.include_router(router=app_router)

    return app_


app = get_app()
