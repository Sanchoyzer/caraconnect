from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from app.exceptions.rand_gen import RandGenNotFoundError
from app.models.rand_gen import GetValuesResponse, SetParamsRequest, SetParamsResponse
from app.services.rand_gen import RandGenService


rand_gen_router: APIRouter = APIRouter()


@rand_gen_router.post('', response_model=SetParamsResponse)
async def set_params(params: SetParamsRequest) -> SetParamsResponse:
    return await RandGenService.set_params(params=params)


@rand_gen_router.get('/{uid}', response_model=GetValuesResponse)
async def get_values(uid: UUID, amount: Annotated[int, Query(ge=1)] = 1) -> GetValuesResponse:
    try:
        return await RandGenService.get_values(uid=uid, amount=amount)
    except RandGenNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
