from fastapi import APIRouter

from app.routers.rand_gen import rand_gen_router


v1_router = APIRouter()

v1_router.include_router(rand_gen_router, prefix='/rand_gen', tags=['RandGen'])
